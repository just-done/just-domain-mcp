# Just Domain - MCP Server

**Check whether a domain is available and what it costs, and whether a domain you
already own somewhere else could move here. Straight from chat.**

Ask your AI assistant whether a name is free and what it costs, and it hands back a
link to register it on justdomain.ai without leaving the conversation. Ask it about a
domain you already own at another registrar and it reports what would block a
transfer, whether your DNS survives the move, and the full-term transfer price. Both
tools are read-only: nothing is bought, charged or changed in the chat.

- **Website:** https://justdomain.ai
- **MCP endpoint:** `https://mcp.justdomain.ai/`
- **Registry name:** `ai.justdomain/just-domain`
- **Transport:** Streamable HTTP (remote, nothing to install)
- **Auth:** none. Both tools are read-only and unauthenticated.

## Connecting

```json
{
  "mcpServers": {
    "just-domain": {
      "type": "streamable-http",
      "url": "https://mcp.justdomain.ai/"
    }
  }
}
```

Then ask your assistant to check a domain.

## Tools

| Tool | What it does |
| --- | --- |
| `search_domains` | Check one or more domain names: returns availability, the registration price, the renewal price, and for available names a URL to open and register on justdomain.ai. Both prices are totals for one full registration term of that ending, not per-year rates: one year on most endings, two years on `.ai`, whose registry mandates a two-year term. Read-only; no order or payment in chat. |
| `check_domain_transfer` | Precheck ONE domain you already own at another registrar: what would block a transfer, who sponsors it today, whether its DNS keeps working through the move, and the full-term transfer price. Answered from the registry's own public RDAP record plus our registrar's price list, so it reads no account and no database. An empty `blockers` list is the only thing that means ready. |

The same transfer facts are published over plain HTTP for agents with no MCP client:

```
GET https://mcp.justdomain.ai/api/transfer/precheck?domain=example.com
```

Unauthenticated, read-only, no key. It is served by the MCP host above, not by the
justdomain.ai website.

### What these tools will not do

- No purchase, no payment and no order is created by either tool. A registration is
  completed by a person in a browser on justdomain.ai.
- Moving a domain **in** is not a self-service function yet. `check_domain_transfer`
  reports whether a domain is eligible and what it would cost; the move itself is
  arranged by a person, and the route is support@just-done.ai.
- No authorization (EPP) code is ever returned, accepted or hinted at, and there is no
  agent path to unlocking a domain or to having a code issued. Moving a domain **out**
  is self-service, and self-service there means a human owner signed in on
  justdomain.ai in a browser: they switch the transfer lock off and get the code from
  their own account. An auth code is a bearer credential for the domain, and a chat
  transcript is not a place to put one.
- Premium names are reported but cannot be registered or transferred through Just
  Domain yet.

## Agent Skill (ChatGPT / Codex / any SKILL.md runtime)

This repo also ships a **[SKILL.md](https://learn.chatgpt.com/docs/build-skills)-format
Agent Skill** for Just Domain: a small package that teaches an agent *when* and *how*
to use the two tools, and where to stop. It lives at
[`skills/just-domain/`](./skills/just-domain).

**Install (Codex / any GitHub-tree installer):** point the skill installer at the
GitHub tree URL:

```
https://github.com/just-done/just-domain-mcp/tree/main/skills/just-domain
```

**Manual install:** copy the `skills/just-domain/` folder into your runtime's skills
directory: `$CODEX_HOME/skills/` (or `~/.codex/skills/`) for Codex, `~/.claude/skills/`
for Claude.

The same package is served for discovery on the MCP host, for other runtimes and
`/.well-known` scanners:

- Index: `https://mcp.justdomain.ai/.well-known/agent-skills/index.json`
- Skill: `https://mcp.justdomain.ai/.well-known/agent-skills/just-domain/SKILL.md`

The skill still needs the MCP server connected (see **Connecting** above). It declares
that dependency in [`agents/openai.yaml`](./skills/just-domain/agents/openai.yaml).

## Who it's for

Anyone naming a project, business or idea in a chat, anyone wondering whether the
domain they already own could move somewhere better, and AI agents that need a real
availability lookup with a clean handoff to registration.

## About this repository

Public metadata and registry listing for the Just Domain MCP server: `server.json`,
`.mcp.json`, icons, the [`skills/just-domain/`](./skills/just-domain) Agent Skill
package, and this README. The server runs at `https://mcp.justdomain.ai/`; its source
is not part of this repo.

## License

MIT, see [LICENSE](./LICENSE).
