# Just Domain — MCP API reference

Endpoint: `https://mcp.justdomain.ai/` — MCP over Streamable HTTP
(JSON-RPC 2.0 over POST). No auth is required to connect. The server is
read-only: no order is created and no payment is taken through it.

## Tool

### `search_domains` — availability + pricing lookup

| Argument | Type | Required | Notes |
|---|---|---|---|
| `domains` | array of strings | yes | 1–200 fully-qualified domain names, each including its TLD (e.g. `["acme.com", "acme.io"]`). The tool checks exactly these names — it does NOT suggest or add alternative TLDs, and it does NOT expand the list. |

Returns (in `structuredContent`) a `results` array with one entry per requested
domain. Each entry carries:

| Field | Type | Notes |
|---|---|---|
| `name` | string | The second-level label (the part before the TLD). |
| `tld` | string | The TLD. |
| `available` | boolean | Whether the domain can be registered right now. |
| `premium` | boolean | Whether it is a premium (higher-priced) name. |
| `price_first_year` | number | First-year registration price. |
| `price_renewal` | number | Annual renewal price. |
| `checkout_url` | string | Present on available names only — a URL the user opens in a browser to register on justdomain.ai. |

The tool is read-only (`readOnlyHint`): it reports information and never places
an order or takes payment. To register a name, the user opens its `checkout_url`
in a browser and completes checkout on justdomain.ai — the agent does not (and
cannot) buy the domain from the chat.

## Raw JSON-RPC (no MCP client available)

The endpoint accepts plain JSON-RPC 2.0 over POST. The `accept` header must
name BOTH `application/json` and `text/event-stream` (a bare `*/*` is rejected
by spec):

```
curl -s https://mcp.justdomain.ai/ \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{
    "jsonrpc": "2.0", "id": 1, "method": "tools/call",
    "params": {
      "name": "search_domains",
      "arguments": { "domains": ["acme.com", "acme.io"] }
    }
  }'
```

The response is SSE-framed: take the first `data:` line and parse it as JSON.
The per-domain results are in `result.structuredContent.results`; for an
available name, `checkout_url` is the browser link to register it.

## Optional extras

The server also exposes, for clients that support them:

- Resource `domain://faq` — the Just Domain FAQ (pricing, transfers, WHOIS
  privacy, refunds, DNS, support).
- Prompt `jd-check` — bootstraps an availability check for a list of names.
- Prompt `jd-transfer-help` — walks the user through transferring an existing
  domain into Just Domain.

## Limits

- **At most 200 domains per request.**
- Each entry must be a fully-qualified domain including its TLD; bare labels are
  rejected.
- The tool checks exactly the domains passed — no alternate-TLD suggestions, no
  list expansion.

Full product docs for humans: https://justdomain.ai
Source and issues: https://github.com/just-done/just-domain-mcp
