# Observability

Course SLO 5.15. Explained in my own words, using the real cost tracking built for this project as the example.

## Observability vs. safety monitoring

The safety monitor (SLO 5.5) is like a warning light in a car — it tells you something might be wrong, using a few selected vital signs. Observability is a diagnostic scanner: it shows the underlying detail — an engine temperature record, which sensor tripped, and so on. This helps in understanding exactly what's happening to cause a problem, instead of just getting a superficial alert.

## The three parameters: cost, latency, startup

**Latency** — already built. Average response time already shows on the System health dashboard.

**Startup** — has the same underlying limitation as the uptime idea that was built and then reverted. We can't distinguish "this response was slow because the app just woke up from sleep" from "this response was slow for some ordinary reason" — the same blind spot as not being able to observe what happened before a process was running, just applied to a single request instead of a whole session.

**Cost** — built today. There was no cap on cost and no cost visibility at all until now. Claude's API responses include token counts, which we turned into a dollar estimate per question, using the real Claude Opus 4.8 pricing ($5 per million input tokens, $25 per million output tokens). This is useful regardless of how many users the app has.
