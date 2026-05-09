import os
import json
import redis
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="AgroSense API Ingest",
    description="Receives sensor data from agricultural drones",
    version="0.1.0"
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
QUEUE_NAME = "sensor_data"

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class SensorReading(BaseModel):
    drone_id: str = Field(..., description="Unique drone identifier")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature_celsius: float = Field(..., ge=-50, le=60)
    humidity_percent: float = Field(..., ge=0, le=100)
    ndvi: float = Field(..., ge=-1, le=1, description="Normalized Difference Vegetation Index")
    altitude_meters: float = Field(..., ge=0, le=500)


class IngestResponse(BaseModel):
    status: str
    message: str
    drone_id: str
    queued_at: str


@app.get("/health")
def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/ingest", response_model=IngestResponse)
def ingest_sensor_data(reading: SensorReading):
    payload = reading.model_dump()
    payload["queued_at"] = datetime.utcnow().isoformat()

    redis_client.rpush(QUEUE_NAME, json.dumps(payload))

    return IngestResponse(
        status="queued",
        message="Sensor reading queued for processing",
        drone_id=reading.drone_id,
        queued_at=payload["queued_at"]
    )


@app.get("/queue/status")
def queue_status():
    length = redis_client.llen(QUEUE_NAME)
    return {"queue": QUEUE_NAME, "pending_messages": length}
EOFcat > services/api-ingest/main.py << 'EOF'
import os
import json
import redis
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="AgroSense API Ingest",
    description="Receives sensor data from agricultural drones",
    version="0.1.0"
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
QUEUE_NAME = "sensor_data"

redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class SensorReading(BaseModel):
    drone_id: str = Field(..., description="Unique drone identifier")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature_celsius: float = Field(..., ge=-50, le=60)
    humidity_percent: float = Field(..., ge=0, le=100)
    ndvi: float = Field(..., ge=-1, le=1, description="Normalized Difference Vegetation Index")
    altitude_meters: float = Field(..., ge=0, le=500)


class IngestResponse(BaseModel):
    status: str
    message: str
    drone_id: str
    queued_at: str


@app.get("/health")
def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")


@app.post("/ingest", response_model=IngestResponse)
def ingest_sensor_data(reading: SensorReading):
    payload = reading.model_dump()
    payload["queued_at"] = datetime.utcnow().isoformat()

    redis_client.rpush(QUEUE_NAME, json.dumps(payload))

    return IngestResponse(
        status="queued",
        message="Sensor reading queued for processing",
        drone_id=reading.drone_id,
        queued_at=payload["queued_at"]
    )


@app.get("/queue/status")
def queue_status():
    length = redis_client.llen(QUEUE_NAME)
    return {"queue": QUEUE_NAME, "pending_messages": length}
