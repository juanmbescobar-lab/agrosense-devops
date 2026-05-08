# AgroSense DevOps Platform

Plataforma de ingesta y procesamiento de datos de sensores de drones agrícolas.

## Stack

- **API Ingest:** FastAPI + Python 3.12
- **Queue:** Redis (local) / AWS ElastiCache (prod)
- **Worker:** Python consumer
- **Database:** PostgreSQL (local) / AWS RDS (prod)
- **Orquestación:** Docker Compose (local) / Kubernetes EKS (prod)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Monitoreo:** Grafana

## Estructura del proyecto
agrosense-devops/
├── services/          # Microservicios de la aplicación
├── infra/terraform/   # Infraestructura como código
├── k8s/               # Manifiestos Kubernetes
├── monitoring/        # Configuración Grafana
├── docs/adr/          # Architecture Decision Records
└── docker-compose.yml

## Cómo correr localmente

```bash
cp .env.example .env
# Editá .env con tus valores
docker compose up
```

## Documentación

- [ADR-001: Selección de stack](docs/adr/ADR-001-stack-selection.md)
