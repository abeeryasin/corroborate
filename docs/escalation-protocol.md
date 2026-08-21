# Escalation Protocol

Course SLO 5.6. Explained in my own words, kept conceptual for v1 since nothing here needed to be built to demonstrate the idea.

## Definition

An escalation protocol is a pre-defined set of thresholds, decided in advance, that specify exactly when an autonomous system should stop continuing on its own and require a human to intervene.

## Why it needs to be decided in advance

It should be written ahead of time, in a calm environment — not while the system is live and something's already going wrong — so that the system knows exactly when to alert a human, instead of a human having to improvise the judgment call under pressure in the moment.

## Corroborate's current behavior vs. a true escalation protocol

Corroborate informs the end user when it's incapable of answering a given question due to lack of relevant context, instead of guessing or making something up. (Stops rather than pushing forward while unsure.)

It's not a full escalation protocol, though, because it doesn't actually alert a human operator when something is wrong — it only stops and tells the end user, not me.

## What would be missing to make it a real escalation, not just a stop

A real escalation would send an alert to me when there's a problem in the system — e.g., if the error rate crosses a set number, if spending crosses a set limit, or if there's a spike in "I don't know" answers.

## Decision for v1

For now, this version of the app — a solo-user demo with limited traffic — doesn't need the escalation protocol described above. Deferred to v3, if it turns out to actually be needed once the project's scope grows.
