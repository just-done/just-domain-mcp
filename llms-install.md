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

2. That's the entire installation. Verify by listing tools — you should see `search_domains`.
3. To use: call `search_domains` with one or more domain names. It returns availability,
   first-year and renewal pricing, and a registration URL for available names. It is
   read-only — no order is placed and no payment is taken in the chat; the user opens the
   returned URL in a browser to register on justdomain.ai.
