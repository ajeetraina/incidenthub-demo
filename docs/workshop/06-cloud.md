# 06 — Repeat in Cloud Sandboxes

This is the Capacity exercise. A Cloud Sandbox runs on Docker-managed infrastructure. It has its own workspace, credentials, network policy and lifecycle. It does not mount your laptop's project directory.

> Cloud Sandboxes require `sbx` 0.45.0 or later and an active Docker Agentic Platform subscription. Cloud compute is billed separately. The default cloud sandbox TTL is one hour.

## 1. Check cloud access

```bash
sbx version
sbx --cloud diagnose
sbx --cloud ls
```

## 2. Configure the cloud agent credential

Local credentials are not automatically available in cloud sandboxes. For Claude Code with an API key:

```bash
sbx --cloud secret set anthropic
```

Follow the prompt to enter the key securely. Never put the key in a command argument, Git repository or workshop notes.

## 3. Create the cloud sandbox

Create a named sandbox and allow the destinations needed to clone the public GitHub repository, reach the model provider and pull the application images:

```bash
sbx --cloud create \
  --name incidenthub-cloud \
  --allow-network github.com:443 \
  --allow-network api.anthropic.com:443 \
  --allow-network registry-1.docker.io:443 \
  --allow-network auth.docker.io:443 \
  --allow-network production.cloudflare.docker.com:443 \
  claude
```

If your account's policy or image registry setup requires additional destinations, inspect the cloud policy and add only the necessary hosts. Do not replace the allowlist with an allow-all rule.

## 4. Clone the repository inside the cloud sandbox

```bash
sbx --cloud exec incidenthub-cloud git clone \
  https://github.com/ajeetraina/incidenthub-demo.git \
  /home/agent/workspace/incidenthub-demo
```

Confirm the checkout:

```bash
sbx --cloud exec incidenthub-cloud ls -la /home/agent/workspace/incidenthub-demo
```

## 5. Start the application in the cloud sandbox

```bash
sbx --cloud exec incidenthub-cloud docker compose \
  -f /home/agent/workspace/incidenthub-demo/docker-compose.yml \
  up --build -d
```

Check the services and health endpoint:

```bash
sbx --cloud exec incidenthub-cloud docker compose \
  -f /home/agent/workspace/incidenthub-demo/docker-compose.yml ps

sbx --cloud exec incidenthub-cloud curl -fsS http://localhost:8000/api/health
```

## 6. Attach the coding agent

```bash
sbx --cloud attach incidenthub-cloud
```

In the agent session, ask it to work in:

`/home/agent/workspace/incidenthub-demo`

Repeat the diagnosis and fix task from [Page 05](05-fix.md). If you need to run a command without attaching, use `sbx --cloud exec` from the host terminal.

## 7. Optional: open the dashboard through a cloud URL

Cloud port publishing returns a public HTTPS URL. Only do this with the synthetic workshop app; this demo has no user authentication.

```bash
sbx --cloud ports incidenthub-cloud --publish 8000
sbx --cloud ports incidenthub-cloud
```

Open the URL returned by the CLI. When finished, unpublish the port:

```bash
sbx --cloud ports incidenthub-cloud --unpublish 8000
```

## 8. Inspect cloud state and expiry

```bash
sbx --cloud ls
sbx --cloud inspect incidenthub-cloud
sbx --cloud ttl incidenthub-cloud
sbx --cloud policy ls
sbx --cloud policy log incidenthub-cloud --limit 20
```

Cloud sandboxes expire after one hour by default. Check the TTL and timeout action before relying on the sandbox to preserve work.

**Checkpoint:** explain why the repository had to be cloned again and why local credentials and policies did not automatically transfer.

Continue to [07 — Cleanup and wrap up](07-cleanup.md).
