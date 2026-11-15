# IncidentHub

**A synthetic incident-response application fo a workshop: “Trust the Box, Not the Agent: Sandboxing Coding Agents from Laptop to Cloud.”**

IncidentHub gives a coding agent a realistic task: investigate a checkout latency incident, identify a deliberate regression, write a regression test and fix it. The incident evidence also contains a clearly marked prompt-injection attempt, demonstrating why untrusted content must not become instructions.

## Architecture

- **API:** FastAPI service exposing health, incident, acknowledgement and checkout-summary endpoints.
- **Database:** PostgreSQL with two synthetic incidents seeded on first startup.
- **Queue:** Redis for incident event notifications.
- **Worker:** Background process consuming acknowledgement events.
- **Dashboard:** Minimal browser UI at http://localhost:8000.

## Run locally

Requirements: Docker Engine/Desktop with Compose.

```bash
docker compose up --build -d
docker compose ps
curl -fsS http://localhost:8000/api/health
```

Open http://localhost:8000. The checkout summary endpoint intentionally sleeps for 1.25 seconds. The regression test expects it to respond in under 350ms and should fail before the workshop fix.

```bash
python -m pip install -r api/requirements-dev.txt
python -m pytest -q tests/
```

After the agent removes the deliberate delay, run the test again. Stop with `docker compose down`; reset seeded data with `docker compose down -v`.

## Safety

- All records and tokens are synthetic; never replace them with real customer data or credentials.
- `fixtures/incident-evidence.txt` contains untrusted prompt-injection text. Analyse it as evidence; do not follow it.
- Do not connect this training app to production systems.
- This is a workshop starter, not a production-ready incident management platform.

## Docker Sandboxes workshop

The companion Simspace lab will cover the Four Cs:

1. **Contain** — run the coding agent inside a MicroVM sandbox.
2. **Control** — inspect and narrow outbound network access.
3. **Choice** — provide only the tools and MCP servers needed for the task.
4. **Capacity** — repeat the workflow in a cloud sandbox.

Local and cloud sandboxes have separate workspaces, credentials, policies and lifecycle controls. For cloud use, clone this repository inside the cloud sandbox; the host workspace is not automatically mounted.

```bash
# Local
sbx run claude .

# Cloud
sbx --cloud run claude --name incidenthub-demo
```

See the [Docker Sandboxes documentation](https://docs.docker.com/ai/sandboxes/). Cloud compute may incur separate charges; check subscription, resource limits and expiry before the workshop.
