# Safety Monitoring

Course SLO 5.5. Explained in my own words, using the technical/system health tracking built for Corroborate as the example.

## The concept

Once an app is deployed and running, safety monitoring means automatically tracking a few "vital signs" of the running app, so problems get noticed without having to check manually.

## Technical health vs. answer quality

A technical fault happens when the API call breaks (e.g., a network error, a bad key) or a Python error occurs. These can be detected by the system, since it can recognize that something crashed.

A quality fault happens when there's no visible technical error to the system — a smooth answer, no crash — but the answer itself is wrong, incomplete, or cites the wrong paper. This cannot be detected by the system, and there's no way to check whether it was actually correct without external verification.

## The decision: technical monitoring now, quality checking later

Checking answer quality would require another LLM to fact-check the answer (LLM-as-judge) — but that's a whole separate thing to build: not easy, not a small step, and not even a guarantee of correctness even once built. I chose to save it for v2.

Instead, we built code that detects how many times the answer came back as "I don't know based on the uploaded papers" — a detectable text pattern that gives a cheap, trackable signal, even though it isn't the same as verifying correctness.

## Why a dashboard, not just the raw data

Three reasons:
1. So I don't need to remember to go check manually.
2. Ease of use — no need to query the `question_log` table directly; the numbers are visible right on the page.
3. It's the demonstrable dashboard artifact the SLO actually asks for.

Honestly, for this app at its current low-traffic, solo-demo scale, the urgency of live visibility versus occasionally querying by hand is low — reason 3 is doing more real work here than reasons 1 and 2. The value of "don't have to remember to check" scales up a lot more once something is running autonomously with real, ongoing traffic.
