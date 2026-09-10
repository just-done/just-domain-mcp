# Just Domain - MCP API reference

Endpoint: `https://mcp.justdomain.ai/`, MCP over Streamable HTTP
(JSON-RPC 2.0 over POST). No auth is required to connect. The server is
read-only: no order is created and no payment is taken through it.

## Tools

### `search_domains` - availability and pricing lookup

| Argument | Type | Required | Notes |
|---|---|---|---|
| `domains` | array of strings | preferred | 1-200 fully-qualified domain names, each including its TLD (e.g. `["acme.com", "acme.io"]`). The tool checks exactly these names. It does NOT suggest or add alternative TLDs, and it does NOT expand the list. |
| `query` | string | fallback | Free text: one or more names, comma- or space-separated. Names given without a TLD are expanded to com/io/ai/co/net. Ignored when `domains` is supplied. |

Returns (in `structuredContent`) a `results` array with one entry per requested
domain. Each entry carries:

| Field | Type | Notes |
|---|---|---|
| `fqdn` | string | The fully-qualified name as checked. |
| `name` | string | The second-level label (the part before the TLD). |
| `tld` | string | The TLD, without a leading dot. |
| `available` | boolean | Whether the domain can be registered right now. |
| `status` | string | Raw provider status, e.g. `free`, `active`, `premium`. |
| `premium` | boolean | Whether it is a premium (registry-priced) name. Just Domain does not register these yet. |
| `term_years` | integer | Length of ONE registration term for this ending, and the period `price` and `renewal_price` each cover. `1` on almost every ending; `2` on `.ai`. |
| `price` | object or null | Registration price for one full term. `{ amount_minor, currency, formatted }`. |
| `renewal_price` | object or null | Price of one further term, same basis as `price`. |
| `checkout_url` | string or null | Present only on available names Just Domain can register: a URL the user opens in a browser to register on justdomain.ai. Absent on premium names. |
| `warnings` | array of strings | Per-row machine codes, most important first, e.g. `premium_not_supported`, `renewal_price_unavailable`. |

**Prices are term totals, not annual rates.** `price` and `renewal_price` each
cover exactly `term_years` years. On `.ai` the registry mandates a two-year
minimum term with no one-year option, so a quoted `.ai` figure is a two-year
total. Do not divide or multiply a returned price by a number of years.

The tool is read-only (`readOnlyHint`): it reports information and never places
an order or takes payment. To register a name, the user opens its `checkout_url`
in a browser and completes checkout on justdomain.ai. The agent does not, and
cannot, buy the domain from the chat.

### `check_domain_transfer` - transfer precheck

| Argument | Type | Required | Notes |
|---|---|---|---|
| `domain` | string | yes | ONE fully-qualified domain the user already owns at another registrar, e.g. `acme.com`. One per call: each call reads a third-party registry. |

Read-only and unauthenticated, like `search_domains`, and answered from two
public sources only: the registry's own RDAP record and our registrar's price
list. It reads no database, so it returns the same answer for a domain Just
Domain sponsors and one it has never heard of.

Returns (in `structuredContent`):

| Field | Type | Notes |
|---|---|---|
| `domain` / `tld` | string | The name as checked. |
| `supported` | boolean | Whether Just Domain can accept this ENDING at all. Says nothing about this particular domain. |
| `ready` | boolean | True only when `blockers` is empty. Derived from that list and never able to disagree with it. |
| `checked_at` | string | ISO-8601 instant the facts were read. |
| `blockers` | array | `{ code, detail, eligible_at }`. **An empty array is the only thing that means ready.** |
| `registrar` | object | `{ name, iana_id }` - who sponsors the domain today, as the registry reports it. |
| `nameservers` | array of strings | The current delegation. |
| `dns_continuity` | object | `{ case, provider, detail }`, case = `independent` / `losing_registrar` / `unknown`. |
| `price` | object or null | `{ amount, currency, term_years, term_note, expected_new_expiry, is_premium }`. Null when the price could not be read - which is not the same as free. |
| `source` | object | `{ rdap, registrar_pricing }` - which sources actually answered. |
| `transfer_url` | string | The page a PERSON opens to take this further. |
| `next_step` | string | One sentence about what happens next, already matched to this domain's state. |
| `auth_code_policy` | string | The authorization-code rule, restated in every payload. |

Blocker codes: `locked`, `within_60_days`, `redemption`, `expired`,
`tld_unsupported`, `premium`, `not_registered`, `pending_transfer`,
`pending_delete`, `unknown`. **Render `detail` for any code you do not
recognise** - dropping a blocker you have no wording for is how a domain in
pendingDelete gets reported as ready. `source.rdap: false` means the registry
did not answer at all, so nothing was established: report that, never "ready".

**The transfer price is a term total, not an annual rate.** `amount` covers
`term_years` years. A `.ai` transfer adds and charges TWO years because its
registry works in two-year units, so halving that figure produces a price no
registry will honour. Quote `term_note` beside the amount.
`expected_new_expiry` is a projection (the registry's current expiry plus the
term), not a date any registry has confirmed.

**Moving a domain IN is not a self-service function yet**; the route is
support@just-done.ai. This tool reports whether a domain is eligible to move
and what one full term would cost; the move itself is arranged by a person,
starting at `transfer_url`. Do not describe a payment step for that page or
promise what it will do.

**No authorization (EPP) code, ever.** This tool never returns, accepts or
hints at one, and there is no agent path to unlocking a domain or to having a
code issued - not here, and not through any other Just Domain surface. An auth
code is a bearer credential for the domain. Do not ask the user for one, do
not offer to hold or relay one, and never claim you can unlock or move a
domain yourself.

Note what that refusal survives. Just Domain DOES let the owner of a domain
held here switch its transfer lock off and issue its authorization code
without contacting support. "Self-service" there means a human owner, signed
in on justdomain.ai, in a browser, and nothing else: those actions live on the
authenticated website surface, no MCP tool reaches them, and none ever will.
A structural test parses this server module's imports to keep it that way.

The same FACTS are published over plain HTTP for agents with no MCP client:
`GET https://mcp.justdomain.ai/api/transfer/precheck?domain=example.com`
(also POST, with `{"domain": "..."}`). It is served by the MCP host, the same
origin as the transport above, and NOT by the `justdomain.ai` website, which
answers 404 for that path. The shape is NOT identical to the tool's, and the
differences matter:

- the projected date is called `new_expiry` there, not `expected_new_expiry`;
- the HTTP payload carries **no `ready`, `transfer_url`, `next_step` or
  `auth_code_policy`**. So read `blockers` and apply the rule yourself: an
  EMPTY list is the only thing that means ready, and the authorization-code
  refusal above still binds even though that payload does not restate it.

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

- Resource `domain://faq`: the Just Domain FAQ (registration terms, pricing,
  WHOIS privacy, DNS, refunds, support, and an explicit list of what Just
  Domain does not support yet).
- Prompt `jd-check`: bootstraps an availability check for a list of names.
- Prompt `jd-transfer-check`: bootstraps a transfer check for one domain.

## Limits

- **At most 200 domains per request** to `search_domains`; exactly ONE domain
  per `check_domain_transfer` call.
- Each entry must be a fully-qualified domain including its TLD; bare labels are
  rejected on the `domains` argument.
- `search_domains` checks exactly the domains passed: no alternate-TLD
  suggestions, no list expansion.
- Every price on this server is a total for one full term, never a per-year
  rate. Never divide one.

## Not available through this server

`search_domains` and `check_domain_transfer` are the only tools, and both are
read-only. There is no registration, renewal, transfer, unlock, DNS or account
tool, and none is reachable by any other method here.

Beyond them, in the product as a whole: renewing a domain IS available, as an
owner action in a browser on justdomain.ai, and Just Domain does send order,
registration and expiry-reminder email. Auto-renew is a per-domain setting on
the same dashboard, and a charge on that setting really happens. Whether one
is scheduled for a given domain, on what date, for how much, and what mail has
already gone out are per-domain and per-account: that domain's page at
https://justdomain.ai/dashboard is the authoritative answer and this server
cannot know it. Never state a renewal date, a charge, or a reminder schedule
on your own - send the owner to the dashboard.

**Moving a domain IN is not a self-service function yet**; the route is
support@just-done.ai. What IS available is the check: `check_domain_transfer`
reports whether a domain is eligible to move, what is blocking it, and what
one full transfer term would cost. Report that answer and hand over the route.
Do not tell a user they can start a transfer, and never quote a price the tool
did not return.

Moving a domain OUT is available, and it is an OWNER action on justdomain.ai
behind a sign-in: the owner switches the transfer lock off and gets the
authorization (EPP) code from their own account, free, with no survey and no
retention offer. It is not reachable from this server. **No authorization
(EPP) code is ever issued to an agent or an API caller, and there is no agent
path to unlocking a domain.** That does not change when the product gains
something later.

Full product docs for humans: https://justdomain.ai
Source and issues: https://github.com/just-done/just-domain-mcp
