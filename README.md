# Just Domain — MCP Server

**Search domain availability and pricing, straight from chat — then open a link to register.**

Ask your AI assistant whether a domain is free and what it costs. The Just Domain MCP
server checks availability and first-year + renewal pricing and hands back a link to
register the name on justdomain.ai — without leaving the conversation. It's read-only:
nothing is bought or charged in the chat.

- **Website:** https://justdomain.ai
- **MCP endpoint:** `https://mcp.justdomain.ai/mcp`
- **Registry name:** `ai.justdomain/just-domain`
- **Transport:** Streamable HTTP (remote — nothing to install)

## Connecting

```json
{
  "mcpServers": {
    "just-domain": {
      "type": "streamable-http",
      "url": "https://mcp.justdomain.ai/mcp"
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

## Who it's for

Anyone naming a project, business, or idea in a chat — and AI agents that need a real
domain-availability lookup with a clean handoff to registration.

## About this repository

Public metadata + registry listing for the Just Domain MCP server: `server.json`,
`.mcp.json`, icons, and this README. The server runs at `https://mcp.justdomain.ai/mcp`;
its source is not part of this repo.

## License

MIT — see [LICENSE](./LICENSE).
