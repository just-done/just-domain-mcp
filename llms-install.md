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

2. That's the entire installation. Verify by listing tools: you should see
   `search_domains` and `check_domain_transfer`.

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

5. Two things neither tool does. Moving a domain IN is not a self-service function
   yet: report the check, then hand over to support@just-done.ai. And no authorization
   (EPP) code is ever returned, accepted or hinted at, with no agent path to unlocking
   a domain or to having a code issued. Moving a domain OUT is self-service for the
   human owner, signed in on justdomain.ai in a browser, and for nobody else.

## Agent Skill (optional)

This repo also ships a SKILL.md-format Agent Skill at `skills/just-domain/` that
teaches an agent when and how to use both tools. Codex-style installers can pull it
from the GitHub tree
`https://github.com/just-done/just-domain-mcp/tree/main/skills/just-domain`, or copy
the folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/`). It is also served at
`https://mcp.justdomain.ai/.well-known/agent-skills/index.json`. The skill still
requires the MCP server above to be connected.
