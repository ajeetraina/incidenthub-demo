# 00 , Start here

## The story

You are the on-call engineer for IncidentHub. Checkout API latency has increased after a recent release. You ask a coding agent to investigate and fix the problem.

The application is deliberately small but realistic enough to demonstrate the full workflow:

- FastAPI serves the dashboard and incident API.
- PostgreSQL stores synthetic incident records.
- Redis carries acknowledgement events.
- A worker consumes those events.
- The checkout summary endpoint contains an intentional 1.25-second blocking delay.

The incident evidence also includes a prompt-injection attempt. It asks the agent to read local configuration and send it to an external destination. That text is part of the incident record; it is not an instruction.

## What you will learn , the Four Cs

1. **Contain:** run the coding agent inside an isolated MicroVM with its own Docker Engine.
2. **Control:** govern the destinations the agent can reach through network policy.
3. **Choice:** give the agent only the tools and permissions needed for the task.
4. **Capacity:** reproduce the workflow in a Cloud Sandbox.

## The task

By the end of the workshop, you should be able to:

- Explain why an agent's prompt is not a security boundary.
- Find the deliberate checkout latency regression.
- Add a regression test and remove the artificial delay.
- Demonstrate a scoped network deny rule and inspect the policy log.
- Explain what changes between local and cloud sandboxes.

Continue to [01 , Prepare your environment](01-prepare.md).
