# 08 , Protect MCP with Cedar and audit the decisions

This optional governance module extends the Four Cs with **MCP protection**, **Cedar authorization**, and **auditability**. It requires an organization with Docker AI Governance and an administrator who can create organization policies. It is not a local-only feature toggle.

> Important scope distinctions
>
> - MCP Cedar policies are organization policies. Developers cannot create local Cedar MCP policies with `sbx policy`.
> - Governance applies to MCP servers and calls routed through the Docker MCP gateway. It does not govern an agent's direct MCP connection from inside the VM. Pair MCP policy with network policy to block direct network access to the same server.
> - Organization governance and audit logs cover governed local sandboxes. Audit logs do not cover cloud sandboxes. Cloud network decisions have separate cloud policy logs.
> - A governed MCP request is default-deny unless a matching Cedar `permit` allows it. A matching `forbid` overrides a permit.

## 1. Register only the MCP server the exercise needs

For a real workshop, use an approved, read-only IncidentHub MCP server endpoint supplied by the instructor. Do not point the agent at a production MCP server.

Example registration syntax (replace the URL with the instructor-provided endpoint):

```bash
sbx mcp add incidenthub-readonly --url https://mcp.example.org/incidenthub/mcp
sbx mcp ls
sbx mcp inspect incidenthub-readonly
```

The example URL is a placeholder, not a live service. Prefer static MCP mode so the agent receives only the explicitly selected server:

```bash
sbx run claude --name incidenthub-governed --static-mcp incidenthub-readonly .
```

For an already-running sandbox, register the server on the host and attach it:

```bash
sbx mcp load incidenthub-readonly --sandbox incidenthub-local
```

Do not register a host stdio server unless you trust the command and understand that local stdio servers run on the host, outside the MicroVM boundary.

## 2. Add an organization MCP policy written in Cedar

An organization administrator creates an MCP access policy in Docker Home under **AI Platform > Policies**, scopes it to the workshop team, and publishes it to licensed members.

The following is an illustrative allowlist policy. Adapt the server identity and tool names to the instructor's actual MCP server and validate it in the policy editor before enforcing it:

```cedar
// Permit registration only under the expected name and endpoint identity.
permit (
  principal,
  action == MCP::Action::"register",
  resource
)
when {
  resource in MCP::Server::"incidenthub-readonly" &&
  resource.identityURL == "https://mcp.example.org/incidenthub/mcp"
};

// Permit only tools marked read-only on this registered server.
permit (
  principal,
  action == MCP::Action::"invokeTool",
  resource
)
when {
  resource in MCP::Server::"incidenthub-readonly" &&
  resource.readOnly == true
};

// Require in-session confirmation for non-read-only tools on this server.
@requireApproval("Confirm IncidentHub write operation")
permit (
  principal,
  action == MCP::Action::"invokeTool",
  resource
)
when {
  resource in MCP::Server::"incidenthub-readonly" &&
  resource.readOnly == false
};
```

Cedar evaluates the MCP gateway request using principal, action, resource and context. The organization/team policy scope supplies the principal, so do not add principal role or team attribute checks to the Cedar statement. Tool names are bare names, not display-prefixed names. For a production policy, scope tool permits to the intended server identity as well as the tool name, and add explicit rules for resources, prompts and built-in gateway tools where needed.

The `readOnly` annotation is supplied by the MCP server and is advisory. Tools without a read-only annotation default to `false`, so this policy treats them as write-capable and requires confirmation. A matching `forbid` overrides the approval-gated permit.

```cedar
@requireApproval("Confirm incident acknowledgement")
permit (
  principal,
  action == MCP::Action::"invokeTool",
  resource
)
when {
  resource.name == "acknowledge_incident"
};
```

A matching `forbid` still overrides an approval-gated permit. Approval is an in-session confirmation, not an out-of-band approval workflow. Tool listings may still show tools that will be denied when invoked.

## 3. Verify the MCP boundary

Ask the agent to call the read-only incident lookup tool. Confirm that it succeeds.

Then ask it to call a write tool, or another tool not explicitly permitted. Confirm that the gateway denies the request. Capture the server name, tool name, action, policy scope and decision. Do not treat a visible tool in a tool list as proof that it is authorized.

Also verify the network policy blocks the MCP server's hostname for direct connections from the sandbox. MCP Cedar policy governs gateway traffic; network policy is the complementary control for direct outbound traffic.

## 4. Enable and inspect audit logs

An organization owner or administrator with audit permissions opens Docker Home:

1. Select the organization.
2. Go to **AI Platform > Audit logs**.
3. Open **Audit delivery** and enable local disk, Docker Cloud, or both.
4. Run the governed MCP allow and deny tests again.
5. Return to **Audit logs** and inspect the resulting policy decision records.

Audit records include policy decisions and sandbox session lifecycle events. They contain metadata such as who made the request, the target and the decision. They do not contain prompts, agent output or tool argument values.

With cloud delivery enabled, administrators can search and export records, forward them to a SIEM, and use the Audit Logs API. Hosted audit views and exports require cloud delivery. Docker Cloud retains audit records for 90 days.

For local disk delivery, collect completed `.jsonl` files from each developer host. Default locations:

| OS | Audit directory |
|---|---|
| macOS | `~/Library/Logs/com.docker.sandboxes/sandboxes/auditkit/` |
| Linux | `${XDG_STATE_HOME:-~/.local/state}/sandboxes/sandboxes/auditkit/` |
| Windows | `%LOCALAPPDATA%\\DockerSandboxes\\sandboxes\\logs\\auditkit\\` |

Collect only completed `.jsonl` files, not temporary `.tmp` files. Docker does not delete the JSONL files, so configure retention and cleanup in your log collection process.

## 5. Compare the control planes

| Control | What it protects | Scope |
|---|---|---|
| MicroVM isolation | Host boundary and shared workspace | Local and cloud, with environment-specific behavior |
| Network policy | Outbound destinations | Local organization policy or cloud network policy |
| MCP gateway + Cedar | Server registration, tool calls, resources, prompts and gateway tools | Organization-governed local sandboxes |
| Audit logs | Policy decisions and sandbox lifecycle metadata | Governed local sandboxes |
| Cloud policy logs | Cloud sandbox policy decisions | Cloud sandboxes |

**Checkpoint:** demonstrate one allowed read-only MCP call, one denied write call, the Cedar statement responsible for the decision, and the corresponding audit event. Explain why MCP policy and network policy are both needed.

## References

- [Docker MCP gateway](https://docs.docker.com/ai/sandboxes/mcp-gateway/)
- [Organization MCP access policies](https://docs.docker.com/ai/governance/organization/policies/mcp/)
- [MCP Cedar policy reference](https://docs.docker.com/ai/governance/reference/mcp-policy/)
- [Audit logs](https://docs.docker.com/ai/governance/organization/audit/)
- [Configure audit delivery](https://docs.docker.com/ai/governance/organization/audit/configure/)
