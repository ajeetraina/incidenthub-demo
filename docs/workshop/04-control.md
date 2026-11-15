# 04 — Control network access

The sandbox provides an outbound network proxy and policy controls. In this exercise, add a deny rule scoped to the IncidentHub sandbox, check the decision, attempt a request, and inspect the policy log.

> Run these policy commands in the host terminal. They control the sandbox; they are not Docker Compose commands.

## 1. Inspect current rules

```bash
sbx policy ls
sbx policy ls incidenthub-local --wide
```

## 2. Deny one test destination for this sandbox

```bash
sbx policy deny network --sandbox incidenthub-local example.com
```

This is a sandbox-scoped rule. It does not change the policy for every sandbox on your machine.

## 3. Check the policy decision

```bash
sbx policy check network --sandbox incidenthub-local example.com
```

Expected result:

```text
Denied: example.com
```

## 4. Verify from inside the sandbox

```bash
sbx exec incidenthub-local -- curl -sI --max-time 5 https://example.com
```

The request should be blocked by the sandbox policy. If your organization centrally manages sandbox policy, its rules may also apply.

## 5. Inspect the policy log

```bash
sbx policy log incidenthub-local --limit 20
```

Find the denied request and identify the matching rule.

## 6. Remove the test rule

```bash
sbx policy rm network --sandbox incidenthub-local --resource example.com
sbx policy ls incidenthub-local --wide
```

The app itself does not need access to `example.com`; this is only a controlled demonstration of outbound policy enforcement.

**Checkpoint:** explain the difference between isolating a process (Contain) and controlling where it can connect (Control).

Continue to [05 — Fix the incident](05-fix.md).
