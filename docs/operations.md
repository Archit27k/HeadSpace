# Operations & Troubleshooting Manual

## Disaster Recovery & Backups

### PostgreSQL Backup
Run this cron job daily to snapshot the database:
```bash
pg_dump -U postgres -h localhost headspace > headspace_backup_$(date +%F).sql
```

### Qdrant Vector Backup
The Qdrant volume is mapped to `qdrant_data`. Ensure this persistent volume is backed up using your cloud provider's snapshot tooling (e.g., EBS snapshots).

## Troubleshooting Runbook

### High Latency on API Requests
1. **Check Grafana**: Look at the `/metrics` dashboard. Are LLM calls taking too long?
2. **Check Rate Limits**: SlowAPI might be throttling requests if the burst limit is exceeded.
3. **Database Locks**: Check PostgreSQL for long-running transactions.

### HPA Scaling Issues
If pods are continually crashing (CrashLoopBackOff) after scaling:
1. **Check memory limits**: The ML inference or LangGraph states might be exceeding 512Mi. Increase limits in `backend-deployment.yaml`.
2. **Check Liveness Probes**: Ensure the `/health` endpoint is returning 200 OK within 5 seconds.

### OpenTelemetry Missing Traces
Ensure the `FastAPIInstrumentor` is properly initialized before the app starts serving traffic. Check if Jaeger/Zipkin environment variables are set if exporting traces outside of console logs.
