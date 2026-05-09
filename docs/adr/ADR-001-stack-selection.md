# ADR-001: Selección del stack tecnológico

**Fecha:** 2025-01-01  
**Estado:** Aceptado  
**Autor:** Juan Manuel Bermúdez

## Contexto

Se necesita una plataforma que simule la ingesta y procesamiento de datos
de sensores de drones agrícolas. El proyecto tiene dos objetivos:

1. Simular un sistema real de monitoreo ambiental
2. Servir como portfolio DevOps demostrando CI/CD, containerización,
   orquestación y cloud infrastructure

## Decisión

Stack seleccionado:

- **Lenguaje:** Python 3.12
- **API:** FastAPI
- **Queue:** Redis (local) / AWS ElastiCache (producción)
- **Base de datos:** PostgreSQL (local) / AWS RDS (producción)
- **Containerización:** Docker + Docker Compose (local)
- **Orquestación:** Kubernetes / AWS EKS (producción)
- **IaC:** Terraform
- **CI/CD:** GitHub Actions
- **Monitoreo:** Grafana

## Alternativas consideradas

| Componente | Alternativa descartada | Razón |
|------------|----------------------|-------|
| FastAPI | Flask | FastAPI tiene validación automática con Pydantic, documentación OpenAPI integrada y soporte async nativo |
| Redis | Kafka | Kafka añade complejidad operacional innecesaria para el volumen simulado. Redis Streams es suficiente |
| PostgreSQL | MySQL | PostgreSQL tiene mejor soporte para datos JSON y extensiones GIS, relevante para datos geoespaciales de drones |
| GitHub Actions | Jenkins | GitHub Actions está integrado al repositorio, no requiere infraestructura adicional para CI/CD |
| Terraform | CloudFormation | Terraform es cloud-agnostic y es el estándar de la industria en roles DevOps |

## Consecuencias

- Todo el stack es containerizable desde el día 1
- Cada componente local tiene un equivalente managed en AWS
- El desarrollo es progresivo: local → CI/CD → Kubernetes → cloud
