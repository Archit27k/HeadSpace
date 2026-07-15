# Deployment Guide

HeadSpace AI supports both local development via Docker Compose and enterprise production deployment via Kubernetes.

## Local Deployment (Docker Compose)

1. Clone the repository and configure `.env`:
   ```bash
   cp .env.example .env
   # Populate GEMINI_API_KEY and JWT_SECRET
   ```
2. Build and start the stack:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```
3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/docs
   - Grafana: http://localhost:3001

## Production Deployment (Kubernetes)

The `k8s/` directory contains all necessary manifests.

1. Apply the secrets (ensure base64 encoded strings are used in production):
   ```bash
   kubectl apply -f k8s/secrets-template.yaml
   ```
2. Apply the services and deployments:
   ```bash
   kubectl apply -f k8s/services.yaml
   kubectl apply -f k8s/backend-deployment.yaml
   kubectl apply -f k8s/frontend-deployment.yaml
   ```
3. Configure Auto-scaling:
   ```bash
   kubectl apply -f k8s/hpa.yaml
   ```
4. Expose via Ingress:
   ```bash
   kubectl apply -f k8s/ingress.yaml
   ```

Verify deployment status with `kubectl get pods`.
