# IncidentHub architecture

This diagram shows the complete workshop topology, including the Docker Sandbox boundary and the application services running inside it.

## Runtime architecture

```mermaid
flowchart TB
    Dev["Developer / Workshop participant"]
    CLI["Docker Sandboxes CLI (sbx)"]
    Gateway["Host-managed MCP gateway"]
    Admin["Organization admin\nDocker AI Governance"]
    Cedar["Cedar MCP policy\n(default deny + permits)"]
    Audit["Audit logs\n(policy decisions + lifecycle)"]
    Browser["Browser on developer host"]

    subgraph Boundary["Docker Sandbox , isolated MicroVM"]
      Agent["Coding agent\nClaude Code"]
      Engine["Sandbox-local Docker Engine\n(not the host Docker socket)"]
      Compose["Docker Compose"]

      subgraph App["IncidentHub application network"]
        UI["IncidentHub dashboard\nStatic HTML"]
        API["FastAPI service\n:8000"]
        DB[("PostgreSQL\nincidents table")]
        Redis[("Redis\nevent queue")]
        Worker["Background worker"]
      MCP["FastMCP server\n:8001 /mcp"]
      end

      Agent -->|"inspect / edit code\nrun tests"| Workspace["IncidentHub workspace"]
      Workspace --> Compose
      Compose --> Engine
      Engine --> UI
      Engine --> API
      Engine --> DB
      Engine --> Redis
      Engine --> Worker
      UI -->|"HTTP API calls"| API
      API -->|"read / update incidents"| DB
      MCP -->|"HTTP API requests"| API
      API -->|"enqueue acknowledgement event"| Redis
      Redis -->|"BRPOP event"| Worker
    end

    Admin --> Cedar
    Admin --> Audit
    Dev --> CLI
    CLI -->|"create / attach / manage"| Boundary
    Agent -->|"MCP tool calls"| Gateway
    Gateway -->|"route to registered endpoint"| MCP
    Cedar -->|"authorize registration and calls"| Gateway
    Gateway -->|"decision metadata"| Audit
    Browser -->|"HTTP :8000 via sandbox-published port"| UI
    Dev -->|"review changes / test results"| Browser

    classDef actor fill:#14243a,stroke:#6ea8fe,color:#f4f8ff
    classDef service fill:#17372f,stroke:#58c99a,color:#f4fff9
    classDef data fill:#3b2d18,stroke:#e5b45e,color:#fff8e8
    class Dev,CLI,Browser,Agent,Workspace actor
    class Engine,Compose,UI,API,Worker,MCP service
    class DB,Redis data
```

## Request and event flows

1. The participant starts a local sandbox with `sbx run claude .` or provisions a Cloud Sandbox with the supported `sbx --cloud` workflow.
2. The coding agent works on the checked-out IncidentHub workspace from inside the MicroVM. The sandbox has its own Docker Engine; it does not need access to the host Docker socket.
3. Docker Compose starts the API, PostgreSQL, Redis and worker services on the application network.
4. The participant opens the dashboard through the sandbox's published application port. The dashboard calls the FastAPI endpoints.
5. The API reads incident records from PostgreSQL. Acknowledging an incident writes its status to PostgreSQL and pushes an event to Redis; the worker consumes that event.
6. The agent investigates the intentionally slow checkout-summary endpoint, adds a regression test and removes the deliberate blocking delay.

## Security boundaries

- **Contain:** the coding agent and its commands execute inside the MicroVM boundary. The sandbox uses its own Docker Engine rather than mounting the host Docker socket.
- **Control:** outbound agent traffic is governed by the sandbox network policy/proxy. The Compose application network is separate from the agent's outbound network path.
- **Choice:** the FastMCP service exposes three read-only incident lookup tools and one write tool. The Docker Sandboxes MCP gateway registers and loads the remote endpoint for the sandbox.
- **MCP governance:** organization Cedar policy controls registration and gateway-mediated calls. The write tool is marked non-read-only and destructive, so a policy can require in-session confirmation or forbid it. Direct MCP connections bypass gateway Cedar policy and must be controlled by network policy.
- **Audit:** audit logs record policy decisions and sandbox lifecycle metadata for governed local sandboxes. They do not capture prompts, agent output or tool argument values. Cloud sandboxes use separate cloud policy logs.
- **Capacity:** local and cloud sandboxes are separate environments. A cloud sandbox does not automatically inherit the local workspace, credentials or policy; clone the repository and configure required resources there.

## Components

| Component | Responsibility |
|---|---|
| `sbx` CLI | Creates, attaches to and manages local or cloud sandboxes |
| Coding agent | Reads the project, diagnoses the incident, edits code and runs tests |
| Docker Engine + Compose | Runs the application stack inside the sandbox |
| Dashboard | Browser UI served by the API container |
| FastAPI | Health, incident listing, acknowledgement and checkout summary endpoints |
| PostgreSQL | Stores the seeded synthetic incident records |
| Redis | Buffers acknowledgement events |
| Worker | Consumes events from Redis |
| FastMCP server | Exposes incident lookup and acknowledgement tools over Streamable HTTP |
| Docker Sandboxes MCP gateway | Routes registered MCP tools to the sandboxed agent |
| Cedar policy and audit | Governs MCP registration/tool use and records policy decisions where AI Governance is enabled |
| Regression test | Checks that checkout summary responds in under 350ms |

> **Prerequisites:** Docker Sandboxes CLI (`sbx`) and a supported agent. Docker Desktop is not required to run `sbx`. The application stack uses Docker Engine and Docker Compose inside the sandbox.
