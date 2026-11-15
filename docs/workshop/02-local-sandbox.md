# 02 , Create the local sandbox

This page starts the agent and the IncidentHub services in a local MicroVM sandbox.

## 1. Start the sandbox

From the root of the cloned `incidenthub-demo` repository, run this in **Terminal A**:

```bash
sbx run --name incidenthub-local --publish 8000:8000 claude .
```

This creates a named sandbox, shares the current project workspace with it, publishes sandbox port 8000 on host port 8000, and starts Claude Code.

If you already created the sandbox and are reattaching, run:

```bash
sbx run --name incidenthub-local
```

For an existing sandbox, publish the port separately if it is not already published:

```bash
sbx ports incidenthub-local --publish 8000:8000
sbx ports incidenthub-local
```

## 2. Start the application stack

Open **Terminal B** on the host. These commands execute inside the sandbox; they do not use a host Docker Engine:

```bash
sbx exec incidenthub-local -- docker compose up --build -d
sbx exec incidenthub-local -- docker compose ps
```

Wait until the database and Redis health checks pass and the API and worker are running.

## 3. Check the API

```bash
sbx exec incidenthub-local -- curl -fsS http://localhost:8000/api/health
sbx exec incidenthub-local -- curl -fsS http://localhost:8000/api/incidents
```

Expected health response:

```json
{"status":"ok","database":"ok","queue":"ok"}
```

## 4. Open the dashboard

On the host, open:

http://localhost:8000

The dashboard should show the seeded synthetic incidents.

## Troubleshooting

Check sandbox state and published ports:

```bash
sbx ls
sbx ports incidenthub-local
```

Check application logs:

```bash
sbx exec incidenthub-local -- docker compose logs --tail=100 api
sbx exec incidenthub-local -- docker compose logs --tail=100 db
sbx exec incidenthub-local -- docker compose logs --tail=100 redis
sbx exec incidenthub-local -- docker compose logs --tail=100 worker
```

If port 8000 is already in use on your host, publish the sandbox port to another host port, for example:

```bash
sbx ports incidenthub-local --unpublish 8000:8000
sbx ports incidenthub-local --publish 8080:8000
```

Then open http://localhost:8080.

**Checkpoint:** dashboard loads and the health endpoint returns `ok`.

Continue to [03 , Investigate the incident](03-investigate.md).
