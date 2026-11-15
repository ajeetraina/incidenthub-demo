import os
import time
from pathlib import Path
import psycopg2
import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.environ["REDIS_URL"]
queue = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI(title="IncidentHub", version="0.1.0")

def db_connect():
    return psycopg2.connect(DATABASE_URL)

@app.get("/api/health")
def health():
    try:
        with db_connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        queue.ping()
    except Exception as exc:
        raise HTTPException(status_code=503, detail="dependency unavailable") from exc
    return {"status": "ok", "database": "ok", "queue": "ok"}

@app.get("/api/incidents")
def list_incidents():
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,title,service,severity,status,summary,created_at FROM incidents ORDER BY created_at DESC")
            rows = cur.fetchall()
    return [{"id":r[0],"title":r[1],"service":r[2],"severity":r[3],"status":r[4],"summary":r[5],"created_at":r[6].isoformat()} for r in rows]

@app.get("/api/checkout/summary")
def checkout_summary():
    # INTENTIONAL WORKSHOP BUG: remove this blocking delay in the lab.
    time.sleep(1.25)
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM incidents WHERE service = %s", ("checkout",))
            count = cur.fetchone()[0]
    return {"service": "checkout", "open_incidents": count}

@app.post("/api/incidents/{incident_id}/ack")
def acknowledge_incident(incident_id: str):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE incidents SET status='acknowledged' WHERE id=%s RETURNING id", (incident_id,))
            row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="incident not found")
    queue.lpush("incidenthub:events", f"ack:{incident_id}")
    return {"id": incident_id, "status": "acknowledged"}

@app.get("/")
def dashboard():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
