import os
import json
import time
import redis
import psycopg2
from datetime import datetime

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
DATABASE_URL = os.getenv("DATABASE_URL", "")
QUEUE_NAME = "sensor_data"
SLEEP_SECONDS = 1


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def ensure_table_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id          SERIAL PRIMARY KEY,
                drone_id    VARCHAR(100) NOT NULL,
                latitude    DOUBLE PRECISION NOT NULL,
                longitude   DOUBLE PRECISION NOT NULL,
                temperature_celsius  DOUBLE PRECISION NOT NULL,
                humidity_percent     DOUBLE PRECISION NOT NULL,
                ndvi                 DOUBLE PRECISION NOT NULL,
                altitude_meters      DOUBLE PRECISION NOT NULL,
                queued_at   TIMESTAMP NOT NULL,
                processed_at TIMESTAMP NOT NULL
            )
        """)
        conn.commit()
    print("[worker] Table sensor_readings ready")


def process_message(conn, raw_message):
    data = json.loads(raw_message)

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO sensor_readings (
                drone_id, latitude, longitude,
                temperature_celsius, humidity_percent,
                ndvi, altitude_meters,
                queued_at, processed_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["drone_id"],
            data["latitude"],
            data["longitude"],
            data["temperature_celsius"],
            data["humidity_percent"],
            data["ndvi"],
            data["altitude_meters"],
            data["queued_at"],
            datetime.utcnow().isoformat()
        ))
        conn.commit()

    print(f"[worker] Processed reading from drone {data['drone_id']}")


def main():
    print("[worker] Starting processor worker...")

    redis_client = redis.from_url(REDIS_URL, decode_responses=True)

    conn = None
    while conn is None:
        try:
            conn = get_db_connection()
            print("[worker] Connected to PostgreSQL")
        except Exception as e:
            print(f"[worker] Waiting for database... {e}")
            time.sleep(2)

    ensure_table_exists(conn)

    print(f"[worker] Listening on queue '{QUEUE_NAME}'...")

    while True:
        try:
            message = redis_client.blpop(QUEUE_NAME, timeout=5)

            if message is None:
                continue

            _, raw_message = message
            process_message(conn, raw_message)

        except psycopg2.OperationalError as e:
            print(f"[worker] DB connection lost, reconnecting... {e}")
            time.sleep(2)
            conn = get_db_connection()

        except Exception as e:
            print(f"[worker] Error processing message: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
