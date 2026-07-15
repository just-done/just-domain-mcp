---
name: just-domain
description: Check whether a domain name is available and what it costs, straight from the chat, with Just Domain. Use when the user wants to know if a domain is available or taken, compares names, asks "is example.com available", "what would this domain cost", "find me a domain for my project/business/idea", or wants a link to register a specific name. Returns, per domain, availability, whether it's a premium name, the first-year price, the renewal price, and — for available names — a URL to open in a browser to register on justdomain.ai. Read-only: it looks up information only. Do NOT use it to buy, purchase, pay for, or complete registration of a domain in the chat (no order or payment happens here — the user opens the returned link to register); do NOT use it to transfer, renew, manage, or edit DNS on a domain the user already owns; do NOT use it to auto-suggest alternative TLDs (it checks exactly the domains you pass); do NOT use it for anything beyond availability and pricing lookup.
---

# Just Domain — check domain availability and pricing, straight from the chat

Just Domain (https://justdomain.ai) lets you check whether a domain name is
available and what it costs without leaving the conversation. You call one
read-only tool, `search_domains`, on the Just Domain MCP server. It looks up
information only — no order is created and no payment is taken in the chat.
When a name is available, the tool hands back a link the user opens in a
browser to register it on justdomain.ai.

## When to use this skill

The user says things like:

- "is acme.com available?" / "check acme.io and acme.ai"
- "what would acme.com cost?" / "how much is this domain?"
- "find me a domain for <project/business/idea>" (propose specific names, then check them)
- "give me a link to register acme.com"

## When NOT to use it

- **Buying / paying / completing a purchase in the chat.** This skill never
  registers a domain and never takes payment. Registration happens only when
  the user opens the `checkout_url` in a browser on justdomain.ai and completes
  checkout there. Do not tell the user you bought or reserved a name.
- **Managing a domain the user already owns** — transfers, renewals, DNS edits,
  nameserver changes. This tool is availability + pricing lookup only.
- **Auto-expanding TLDs.** The tool checks exactly the domains you pass. If the
  user wants alternatives, YOU propose the names and pass them explicitly.

## How it works

1. **Decide the exact names to check.** Each must be a fully-qualified domain
   including its TLD (e.g. `acme.com`, `acme.io`, `acme.ai`). If the user gave a
   bare word ("acme"), propose specific full domains and check those.
2. **Call `search_domains`** on `https://mcp.justdomain.ai/` (Streamable HTTP,
   no auth required to connect):
   - `domains`: an array of 1–200 fully-qualified domain strings.
   - The tool checks exactly those names — it does not suggest or add TLDs.
3. **Read the results.** Each entry carries: `available` (bool), `premium`
   (bool), the first-year price, the renewal price, and — for available names —
   a `checkout_url`.
4. **Present them clearly** (see below), and for names the user wants, hand over
   the `checkout_url` to open in a browser.

If no MCP client is available, the same endpoint accepts raw JSON-RPC 2.0 over
POST — read `references/mcp-api.md` for the exact request and how to parse the
response.

## Presenting results

- Group into **Available** and **Taken**.
- For each available name, state the **first-year price and the renewal price**
  (both are real product prices the tool returns — quote them as facts, not
  rounded or embellished). Flag `premium` names as premium.
- Do not editorialize the pricing ("cheap", "a steal") — just report it.

## Registering an available name

Registration is a browser step, never a chat step:

1. Give the user the exact name and its first-year + renewal price.
2. Hand them the `checkout_url` for that name and tell them to open it in a
   browser to complete registration on justdomain.ai. They sign in and pay
   there — not here.
3. Do not claim the domain is reserved, held, or purchased until the user tells
   you they finished checkout. The tool only reported availability at lookup
   time; availability can change.

## Optional extra context

A skill-aware agent can also use, when the client supports them:

- Resource `domain://faq` — the Just Domain FAQ (pricing, transfers, WHOIS
  privacy, refunds, DNS, support). Read it to answer common questions without a
  tool call.
- Prompt `jd-check` — bootstraps an availability check for a list of names.
- Prompt `jd-transfer-help` — walks the user through transferring an existing
  domain into Just Domain (grounded in the FAQ). Note: the transfer itself is
  done by the user on justdomain.ai, not by this tool.

## Constraints

- Each entry must be a fully-qualified domain **including its TLD**. Bare words
  are rejected — add the TLD yourself before calling.
- **At most 200 domains per request.**
- The tool checks **exactly** the domains you pass — it never suggests alternate
  TLDs or expands the list.
- Read-only: no order, no payment, no registration happens in the chat.

Full product answers for agents: the `domain://faq` resource and
https://justdomain.ai.
