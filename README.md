# Just Domain — MCP Server

**Search domain availability and pricing, straight from chat — then open a link to register.**

Ask your AI assistant whether a domain is free and what it costs. The Just Domain MCP
server checks availability and first-year + renewal pricing and hands back a link to
register the name on justdomain.ai — without leaving the conversation. It's read-only:
nothing is bought or charged in the chat.

- **Website:** https://justdomain.ai
- **MCP endpoint:** `https://mcp.justdomain.ai/`
- **Registry name:** `ai.justdomain/just-domain`
- **Transport:** Streamable HTTP (remote — nothing to install)

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

Then ask your assistant to check a domain. It returns availability, pricing, and a
registration link.

## Tools

| Tool | What it does |
| --- | --- |
| `search_domains` | Check one or more domain names: returns availability, first-year price, renewal price, and — for available names — a URL to open and register on justdomain.ai. Read-only; no order or payment in chat. |

## Agent Skill (ChatGPT / Codex / any SKILL.md runtime)

This repo also ships a **[SKILL.md](https://learn.chatgpt.com/docs/build-skills)-format
Agent Skill** for Just Domain — a small package that teaches an agent *when* and *how*
to use the `search_domains` tool (check availability + pricing, then hand the user a
link to register — never buying in the chat). It lives at
[`skills/just-domain/`](./skills/just-domain).

**Install (Codex / any GitHub-tree installer):** point the skill installer at the
GitHub tree URL —

```
https://github.com/just-done/just-domain-mcp/tree/main/skills/just-domain
```

**Manual install:** copy the `skills/just-domain/` folder into your runtime's skills
directory — `$CODEX_HOME/skills/` (or `~/.codex/skills/`) for Codex, `~/.claude/skills/`
for Claude.

The same package is also served for discovery on the MCP host, for other runtimes and
`/.well-known` scanners:

- Index: `https://mcp.justdomain.ai/.well-known/agent-skills/index.json`
- Skill: `https://mcp.justdomain.ai/.well-known/agent-skills/just-domain/SKILL.md`

The skill still needs the MCP server connected (see **Connecting** above) — it declares
that dependency in [`agents/openai.yaml`](./skills/just-domain/agents/openai.yaml).

## Who it's for

Anyone naming a project, business, or idea in a chat — and AI agents that need a real
domain-availability lookup with a clean handoff to registration.

## About this repository

Public metadata + registry listing for the Just Domain MCP server: `server.json`,
`.mcp.json`, icons, the [`skills/just-domain/`](./skills/just-domain) Agent Skill
package, and this README. The server runs at `https://mcp.justdomain.ai/`; its source
is not part of this repo.

## License

MIT — see [LICENSE](./LICENSE).
