# SLA Definition

Course SLO 5.13. Explained in my own words, using the reasoning behind a real decision made while building this feature — the code was written, then deliberately reverted before being pushed.

## What SLA mindset means

SLA stands for Service Level Agreement — a commitment or claim by the creator about how reliable or available something is.

Analogy: if a corner store has a sign that says "Open 9AM–5PM," a customer showing up at 6PM and finding it closed isn't surprised — that's exactly what the owner already claimed. But if that same customer found it closed at 2PM, that's a problem — a broken promise, not just limited availability.

The same principle applies to building a product: a creator should honestly tell users about its limitations, scope, and availability upfront, rather than letting people run into surprises later.

## Corroborate's actual SLA

The honest SLA for Corroborate is roughly: available on demand, but may take around 15+ seconds to wake up if it's been sleeping; data resets on waking or redeployment; no uptime guarantee. This is because of Streamlit Community Cloud's sleep behavior on the free tier.

## Why real uptime tracking got built, then deliberately reverted

Two reasons:

1. **We can only observe uptime, never downtime.** When the app is asleep, there's no code running to record anything — nobody's "home" to log when it went down or for how long. The only thing observable is: someone opened the app, at this timestamp. Gaps between those timestamps could be used to infer possible downtime, but that would be an inference, not an accurate calculation — and even a logged "uptime" moment can't distinguish between a session where the app worked perfectly and one where the user hit real lag.

2. **SLAs exist to promise people who aren't part of the development team what to expect.** Since I'm the sole user of this app, building it as an MVP demo for my portfolio, I don't need a log of uptime/downtime — I already know from my own firsthand experience whether it worked when I used it.

Given those two, the real fix wasn't worth building for a project at this scale.
