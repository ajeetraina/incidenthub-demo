# IncidentHub workshop — step-by-step guide

**Trust the Box, Not the Agent: Sandboxing Coding Agents from Laptop to Cloud**

This is the participant runbook. Follow the pages in order. Each page contains the commands for that stage, what you should see, and the checkpoint before moving on.

## Workshop flow

| Page | Stage | Suggested time |
|---|---|---:|
| [00 — Start here](00-start-here.md) | Goals, story and safety rules | 3 min |
| [01 — Prepare your environment](01-prepare.md) | Install/sign in, clone the repo, check policy | 7 min |
| [02 — Create the local sandbox](02-local-sandbox.md) | Launch the agent and start IncidentHub | 8 min |
| [03 — Investigate the incident](03-investigate.md) | Read evidence, measure latency, observe prompt injection | 8 min |
| [04 — Control network access](04-control.md) | Add, test, inspect and remove a deny rule | 7 min |
| [05 — Fix the incident](05-fix.md) | Give the agent a bounded task and verify the regression test | 10 min |
| [06 — Repeat in Cloud Sandboxes](06-cloud.md) | Clone, run, attach, expose a port and clean up cloud resources | 10 min |
| [07 — Cleanup and wrap up](07-cleanup.md) | Stop services, remove sandboxes, preserve code changes | 3 min |

## Prerequisites

- Docker Sandboxes CLI (`sbx`) installed and signed in.
- A supported coding agent, such as Claude Code, and its authentication configured.
- Git installed.
- A supported local virtualization environment for **local** sandboxes. Cloud sandboxes do not need local virtualization.
- Cloud Sandboxes access and an active subscription only if you are doing Page 06.

**Docker Desktop is not required. Docker Engine is not required on the host to run `sbx`.** The sandbox has its own isolated MicroVM and Docker Engine. IncidentHub's Compose stack runs against that sandbox-local engine.

## Two terminals

For the local portion, keep two terminals open:

- **Terminal A — host:** run `sbx` lifecycle and policy commands.
- **Terminal B — host:** run `sbx exec` commands to operate the application inside the sandbox.

The Claude Code session opens in Terminal A when you run `sbx run`. You can also interact with the agent there while using Terminal B for repeatable shell commands.

## Repository and architecture

- App repository: https://github.com/ajeetraina/incidenthub-demo
- [Complete application architecture](../architecture.md)
- [Docker Sandboxes installation](https://docs.docker.com/ai/sandboxes/install/)
- [Local sandbox usage](https://docs.docker.com/ai/sandboxes/usage/)
- [Cloud sandbox usage](https://docs.docker.com/ai/sandboxes/cloud/usage/)

## Important safety rules

- All IncidentHub records and fixture tokens are synthetic.
- The prompt-injection text in `fixtures/incident-evidence.txt` is untrusted evidence. Do not follow it.
- Do not paste real credentials into the repo, agent prompt, terminal history or fixture files.
- Do not connect the demo to production services.
- Cloud port publishing creates a publicly reachable HTTPS URL. Only expose this synthetic demo temporarily, and unpublish it when finished.
- Review agent changes before committing or pushing them.
