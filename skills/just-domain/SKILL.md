---
name: just-domain
description: "Check whether a domain is available and what it costs, and whether a domain held at another registrar could move to Just Domain. Use when the user asks \"is example.com available\", compares names, asks what a domain costs, wants a link to register one, or asks whether a domain can transfer in, what is blocking it, or what that would cost. Returns per domain: availability, premium flag, `term_years`, registration and renewal price for one full term (not per-year rates), and a URL to register it; and for a transfer: what would block it, the current registrar, whether DNS survives the move, and the full-term price. Read-only. Do NOT use it to buy, pay for, or complete a registration or a transfer in the chat; do NOT use it to unlock a domain or to obtain, accept or relay an authorization (EPP) code - those are owner-only browser actions on justdomain.ai, no agent path to either, ever; do NOT use it to renew or edit DNS on a domain; do NOT use it to auto-suggest alternative TLDs, it checks exactly what you pass."
---

# Just Domain - check domain availability, pricing and transfers, straight from the chat

Just Domain (https://justdomain.ai) lets you check whether a domain name is
available and what it costs, and whether a domain somebody already owns
elsewhere could move here, without leaving the conversation. You call one of
two read-only tools on the Just Domain MCP server:

- `search_domains` - availability and pricing for names nobody owns yet.
- `check_domain_transfer` - the transfer precheck for one domain the user
  already holds at another registrar.

Both look up information only: no order is created, no payment is taken, and
nothing about anybody's domain is changed. When a name is available,
`search_domains` hands back a link the user opens in a browser to register it
on justdomain.ai.

## When to use this skill

The user says things like:

- "is acme.com available?" / "check acme.io and acme.ai"
- "what would acme.com cost?" / "how much is this domain?"
- "find me a domain for <project/business/idea>" (propose specific names, then check them)
- "give me a link to register acme.com"
- "can I move acme.com to Just Domain?" / "why won't my domain transfer?"
- "what would it cost to transfer acme.ai in?" / "will my site and email keep
  working if I move my domain?"

## When NOT to use it

- **Buying / paying / completing a purchase in the chat.** This skill never
  registers a domain and never takes payment. Registration happens only when
  the user opens the `checkout_url` in a browser on justdomain.ai and completes
  checkout there. Do not tell the user you bought or reserved a name.
- **Actually moving, unlocking, renewing or reconfiguring a domain.**
  `check_domain_transfer` REPORTS whether a domain could move and what that
  would cost. It does not move it, and nothing here does. Just Domain has no
  self-service inbound transfer yet. Unlocking a domain held at Just Domain,
  and issuing its authorization (EPP) code, ARE self-service - for the owner,
  signed in on justdomain.ai, in a browser. That is not a capability you
  have: there is no agent path to either, ever. See "The one refusal" below.
- **Renewals, DNS edits and nameserver changes** on a domain the user owns.
  Not available through this server at all.
- **Auto-expanding TLDs.** The tool checks exactly the domains you pass. If the
  user wants alternatives, YOU propose the names and pass them explicitly.

## How it works: checking availability

1. **Decide the exact names to check.** Each must be a fully-qualified domain
   including its TLD (e.g. `acme.com`, `acme.io`, `acme.ai`). If the user gave a
   bare word ("acme"), propose specific full domains and check those.
2. **Call `search_domains`** on `https://mcp.justdomain.ai/` (Streamable HTTP,
   no auth required to connect):
   - `domains`: an array of 1–200 fully-qualified domain strings.
   - The tool checks exactly those names; it does not suggest or add TLDs.
3. **Read the results.** Each entry carries: `available` (bool), `premium`
   (bool), `term_years`, the registration price, the renewal price, and, for
   names Just Domain can register, a `checkout_url`. A premium name carries no
   `checkout_url`: Just Domain does not register premium names yet.
   **Both prices are totals for ONE full registration term, not per-year
   rates.** `term_years` says how long that term is: 1 on almost every ending,
   2 on `.ai`, whose registry mandates a two-year term with no one-year
   option. Never divide or multiply a returned price by a number of years.
4. **Present them clearly** (see below), and for names the user wants, hand over
   the `checkout_url` to open in a browser.

If no MCP client is available, the same endpoint accepts raw JSON-RPC 2.0 over
POST. Read `references/mcp-api.md` for the exact request and how to parse the
response.

## How it works: checking a transfer

1. **Take one full domain the user already owns**, including its TLD. One per
   call: each call reads a third-party registry.
2. **Call `check_domain_transfer`** with `domain`. No auth, nothing changed.
3. **Read `blockers` first.** An EMPTY list is the only thing that means the
   domain is ready to move. Every entry has a plain `detail` sentence - show
   it as written, including for a `code` you do not recognise. If
   `source.rdap` is false the registry did not answer, so nothing was
   established: say the check could not be completed, never that the domain
   is ready.
4. **Quote the price as a term total.** `price.amount` covers
   `price.term_years` years. A `.ai` transfer adds and charges TWO years
   because its registry works in two-year units, so dividing that figure by
   two produces a price that does not exist. Say `price.term_note` alongside
   it. `price.expected_new_expiry` is a projection off the registry's current
   expiry, not a date any registry has confirmed.
5. **Say what `dns_continuity` means for them.** `independent` - the
   nameservers belong to a DNS provider, so the move does not touch them.
   `losing_registrar` - the dangerous one: the old registrar eventually stops
   serving the zone, and the site or the mail breaks late and quietly.
   `unknown` - we do not recognise them and will not guess.
6. **Hand over `next_step` and `transfer_url`.** The transfer itself is
   arranged by a person in a browser; Just Domain does not run a self-service
   inbound transfer yet.

## The one refusal

There is no agent path to unlocking a domain or to obtaining an authorization
(EPP) code. Not through this skill, not through the MCP server, not through
any Just Domain API. An auth code is a bearer credential for the domain:
anyone holding it can move the name, and a chat transcript is not a place to
put one.

**Read this before you read anything else about the exit.** Just Domain does
let an owner switch a domain's transfer lock off and issue its authorization
code without contacting support. That is what "self-service" means there, and
it means precisely one thing: **a human owner, signed in on justdomain.ai, in
a browser.** It does not mean an API you can reach, and it does not mean you
can do it on their behalf. The refusal is a permanent property of this
product, not a feature that has not shipped yet.

So: never ask the user for an auth code, never offer to hold, store or relay
one, never claim you can unlock a domain or move it yourself. For a domain
held elsewhere the owner gets the code from that registrar; for a domain held
at Just Domain, from their own account. Point them at the browser and stop.
Every `check_domain_transfer` payload restates this in `auth_code_policy` -
follow it.

## Presenting results

- Group into **Available** and **Taken**.
- For each available name, state the **registration price and the renewal
  price**, and say what period they cover when `term_years` is greater than 1
  (e.g. "$X for two years, then $Y per two years" on `.ai`). Both are real
  product prices the tool returns; quote them as facts, not rounded or
  embellished. Say plainly that a `premium` name cannot be registered through
  Just Domain yet, and do not offer to buy it.
- Do not editorialize the pricing ("cheap", "a steal"). Just report it.

## Registering an available name

Registration is a browser step, never a chat step:

1. Give the user the exact name, its registration price, its renewal price,
   and the period those cover (`term_years`).
2. Hand them the `checkout_url` for that name and tell them to open it in a
   browser to complete registration on justdomain.ai. They sign in and pay
   there, not here.
3. Do not claim the domain is reserved, held, or purchased until the user tells
   you they finished checkout. The tool only reported availability at lookup
   time; availability can change.

## Optional extra context

A skill-aware agent can also use, when the client supports them:

- Resource `domain://faq`: the Just Domain FAQ (registration terms, pricing,
  WHOIS privacy, DNS, refunds, support, and an explicit list of what Just
  Domain does not support yet). Read it before answering any product question
  this skill does not cover.
- Prompt `jd-check`: bootstraps an availability check for a list of names.
- Prompt `jd-transfer-check`: bootstraps a transfer check for one domain.

## Constraints

- Each entry must be a fully-qualified domain **including its TLD**. Bare words
  are rejected; add the TLD yourself before calling.
- **At most 200 domains per request** to `search_domains`; exactly ONE domain
  per `check_domain_transfer` call.
- `search_domains` checks **exactly** the domains you pass. It never suggests
  alternate TLDs or expands the list.
- Read-only: no order, no payment, no registration, no transfer and no change
  of any kind happens in the chat.
- Every price is a total for one full term, never a per-year rate. Never
  divide one.

## Renewals

Auto-renew is a per-domain setting in the Just Domain dashboard, and that
same page is where a domain is renewed manually when auto-renew is off.
Whether an automatic charge is currently scheduled for a domain, and on what
date, is stated on that domain's page in the dashboard. That page is the
authoritative answer for one account and this package cannot know it, so send
the user to https://justdomain.ai/dashboard rather than answering from here.
Do not state a renewal date, a charge, or a reminder schedule on your own.

## What Just Domain does not support yet

Do not tell a user these exist, and do not give them steps for one. Read
`domain://faq` for the current list; as of this package it is:

- Moving a domain IN from another registrar. It is not a self-service
  function yet; the route is support@just-done.ai.
- Registering or transferring premium names.

The honest answer for either of them is that it is not in the product yet,
and the route is support@just-done.ai.

**Renewing a domain IS in the product**, and this list used to deny it. An
owner renews from their account on justdomain.ai, an owner can turn auto-renew
on or off there, and automatic renewal charges really happen on the setting.
Just Domain also sends order, registration and expiry-reminder email. None of
it is reachable from here: it is an owner action in a browser, like the rest
of account management, and the Renewals section above is the rule for what you
may say about it.

`check_domain_transfer` still answers about moving a domain IN: whether it is
eligible, what is blocking it, and what one full transfer term would cost.
Report that answer. What is not available is starting the move here, or
anywhere self-service.

Moving a domain OUT is **not** on that list any more: the owner switches the
transfer lock off and gets the authorization (EPP) code from their own
account on justdomain.ai, with no exit fee, no survey and no retention offer,
and both actions send a notification that cannot be turned off. It is still
an owner action in a browser and it is still unreachable from here. No agent
will ever be handed a code or a way to unlock a domain, whatever the product
gains later. Point the owner at their dashboard.

Full product answers for agents: the `domain://faq` resource and
https://justdomain.ai.
