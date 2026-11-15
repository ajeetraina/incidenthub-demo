# 07 , Cleanup and wrap up

Clean up the application stack, sandbox resources, temporary network rules and any cloud resources.

## 1. Detach and remove the MCP registration

If you completed Page 08, remove the server from the sandbox gateway and the host registration, then close the forwarded port:

```bash
sbx mcp unload incidenthub-readonly --sandbox incidenthub-local
sbx mcp rm incidenthub-readonly
sbx ports incidenthub-local --unpublish 18001:8001
```

## 2. Stop the local application stack

From the host terminal:

```bash
sbx exec incidenthub-local -- docker compose down
```

If you want to reset the PostgreSQL data volume as well:

```bash
sbx exec incidenthub-local -- docker compose down -v
```

The `-v` option deletes the database volume and its workshop data. Use it only when you are happy to reset the demo.

## 3. Stop and remove the local sandbox

```bash
sbx stop incidenthub-local
sbx ls
sbx rm incidenthub-local
```

Removing a sandbox deletes its MicroVM filesystem. The default local workspace is a shared host working tree, so your project files remain in the cloned repository.

## 4. Remove any leftover test policy

If you did not remove the example.com rule on Page 04:

```bash
sbx policy rm network --sandbox incidenthub-local --resource example.com
```

If the sandbox has already been removed, its sandbox-scoped rules are removed with it.

## 5. Remove the cloud sandbox

If you completed Page 06:

```bash
sbx --cloud ports incidenthub-cloud --unpublish 8000
sbx --cloud rm incidenthub-cloud
sbx --cloud ls
```

Cloud removal is permanent for that sandbox. Do not rely on the default one-hour TTL as your cleanup plan.

## 6. Review and preserve your code changes

Back in your host checkout:

```bash
git status --short
git diff
```

If you want to keep the agent's fix, review it, then commit and push it:

```bash
git add api/main.py tests/test_checkout_latency.py
git commit -m "Fix checkout summary latency"
git push
```

Do not commit credentials, local environment files or real incident/customer data.

## Wrap-up questions

1. What did the MicroVM isolate from the host?
2. Why is a container alone not the same security boundary as a sandboxed agent?
3. Which network rule did you add, and how did you verify it?
4. What was the prompt-injection attempt, and why was it treated as untrusted data?
5. What had to be configured again when moving from local to cloud?

**Workshop complete.** Return to the [workshop index](README.md) or the [full architecture diagram](../architecture.md).
