.PHONY: up down logs ps build clean help

help:
	@echo "Comandos disponibles:"
	@echo "  make up      - Levanta todos los servicios"
	@echo "  make down    - Baja todos los servicios"
	@echo "  make logs    - Muestra logs de todos los servicios"
	@echo "  make ps      - Muestra el estado de los contenedores"
	@echo "  make build   - Reconstruye las imágenes"
	@echo "  make clean   - Baja servicios y elimina volúmenes"

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

build:
	docker compose build

clean:
	docker compose down -v
