import os
import redis

queue = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True)
print("IncidentHub event worker ready", flush=True)
while True:
    item = queue.brpop("incidenthub:events", timeout=0)
    if item:
        print(f"processed event: {item[1]}", flush=True)
