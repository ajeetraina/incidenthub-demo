# 01 , Prepare your environment

## 1. Install and sign in to Docker Sandboxes

Follow the official [installation guide](https://docs.docker.com/ai/sandboxes/install/) for your operating system. Docker Desktop and a host Docker Engine are **not** prerequisites for the `sbx` CLI. Local sandboxes do require supported hardware virtualization; Cloud Sandboxes run on Docker-managed infrastructure.

Sign in:

```bash
sbx login
```

Check the CLI:

```bash
sbx version
sbx --help
```

For the cloud exercise, use `sbx` 0.45.0 or later and confirm account access:

```bash
sbx --cloud diagnose
```

Cloud compute is billed separately. Review your account access and subscription before Page 06.

## 2. Configure your coding agent

For Claude Code with a supported Claude subscription, you can authenticate from inside the agent session using its `/login` flow. If you use an API key, configure it using the supported `sbx secret` workflow; do not put it in this repository.

For the cloud exercise, local credentials are not inherited by Cloud Sandboxes. Page 06 shows the cloud-specific credential command.

## 3. Initialize local network policy

Check the current policy:

```bash
sbx policy ls
```

If this machine has not been given a network preset yet, initialize Balanced:

```bash
sbx policy init balanced
```

Run `sbx policy init balanced` only when no preset has been initialized. If the CLI prompts you during the first sandbox launch, choose **Balanced**.

Balanced is a practical workshop starting point: common development destinations are allowed, and other destinations require approval or an explicit rule. An organization-managed policy may further restrict what local rules can allow.

## 4. Clone IncidentHub

```bash
git clone https://github.com/ajeetraina/incidenthub-demo.git
cd incidenthub-demo
git status --short
```

Confirm that the expected files exist:

```bash
ls
ls api
ls db
ls fixtures
ls tests
```

Expected top-level items include `api/`, `db/`, `fixtures/`, `tests/`, `worker/`, and `docker-compose.yml`.

## 5. Review the application architecture

Open [the architecture diagram](../architecture.md). The important distinction is that the agent runs inside the sandbox, and the application's containers run on the Docker Engine **inside that sandbox**. The host Docker socket is not mounted into the agent.

**Checkpoint:** `sbx version` works, you are signed in, the repo is cloned, and you can explain why Docker Desktop is not a prerequisite.

Continue to [02 , Create the local sandbox](02-local-sandbox.md).
