# Installing Just Domain (for AI agents)

Just Domain is a remote MCP server. There is nothing to download, build, or run
locally, and no API key is required.

1. Add this entry to the user's MCP settings file:

   {
     "mcpServers": {
       "just-domain": {
         "type": "streamableHttp",
         "url": "https://mcp.justdomain.ai/"
       }
     }
   }

2. That's the entire installation. Verify by listing tools: you should see three,
   `search_domains`, `check_domain_transfer` and `check_trademark`.

3. `search_domains` takes one or more domain names and returns availability, the
   registration and renewal price, and a registration URL for available names. Both
   prices are totals for one full registration term of that ending, not per-year
   rates: one year on most endings, but two years on `.ai`, whose registry mandates a
   two-year term. Do not divide or multiply a returned price by a number of years. It
   is read-only: no order is placed and no payment is taken in the chat, and the user
   opens the returned URL in a browser to register on justdomain.ai.

4. `check_domain_transfer` takes ONE domain the user already owns at another
   registrar and returns what would block a transfer, who sponsors it today, whether
   its DNS survives the move, and the full-term transfer price. It is answered from
   the registry's public RDAP record and our registrar's price list, so it reads no
   account and no database. An empty `blockers` list is the only thing that means
   ready; `source.rdap: false` means the registry did not answer, so nothing was
   established. The same answer is published over plain HTTP, no MCP client needed:
   `GET https://mcp.justdomain.ai/api/transfer/precheck?domain=example.com` (served by
   the MCP host, not by the justdomain.ai website).

   It also hands back a `transfer_url`: moving a domain IN is self-service in a
   browser, where the owner checks it and pays at https://justdomain.ai/transfer,
   pasting the authorization code there.

5. `check_trademark` takes ONE proposed name and checks it against the trademark
   registers Open Trademarks (https://opentrademarks.org) covers (US, EU and Israel),
   answered by Open Trademarks. It returns a `verdict` (`exact_live_mark`,
   `similar_live_marks`, `no_live_match`, or `not_checked`, which is no verdict), the
   conflicting marks, and each register's read date; a register with no read date in
   the answer was not checked. Optional `goods`, `classes` (Nice 1 to 45) and
   `registers` narrow it. A register search is not legal advice, and no answer clears
   a name.

6. What no tool does. No authorization (EPP) code is ever returned, accepted or
   hinted at, with no agent path to unlocking a domain or to having a code issued.
   Moving a domain OUT is self-service for the human owner, signed in on
   justdomain.ai in a browser, and for nobody else.

## Agent Skill (optional)

This repo also ships a SKILL.md-format Agent Skill at `skills/just-domain/` that
teaches an agent when and how to use the tools. Codex-style installers can pull it
from the GitHub tree
`https://github.com/just-done/just-domain-mcp/tree/main/skills/just-domain`, or copy
the folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/`). It is also served at
`https://mcp.justdomain.ai/.well-known/agent-skills/index.json`. The skill still
requires the MCP server above to be connected.
