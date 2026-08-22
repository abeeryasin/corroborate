# Staging vs. Production

Course SLO 5.14. Explained in my own words, using the real staging setup built for this project.

## What staging vs. production actually means

Staging can be compared to a dress rehearsal before a play — it's the actual app as it's been built so far, but only deployed for me to see, without a public audience. Same as a dress rehearsal: the same play, without an audience. This allows testing and making changes without them being seen by users or the public.

Production is when the URL goes live — the actual app, the opening night in front of an audience — so anyone clicking the link can see exactly what's there.

## The actual workflow

This uses git branches: every change gets committed onto the `staging` branch first, which is a parallel branch of the same project. Staging then gets pushed, the staging app redeploys, and shows the changes on a separate URL. From there, I can test and make further changes, going through the same chain — commit, push, verify — until the app looks good and the changes are verified. Only then does staging get merged into the `main` branch, and `main` gets pushed. That's what makes the changes live on the real URL.

This allows testing for failure without it showing up on the live, production app.

## When staging is skipped

Changes like writing documents — such as the one I'm writing right now — don't need to go through the staging → merge process. Only real code that could affect the live app's behavior should use this workflow.

## Why this wasn't set up before the first deploy

The other SLOs in this module were treated as documentation to write after the deploy — but this wasn't caught in time: staging is a workflow habit that only has real value if adopted before the actual risky changes happen, not something that can be meaningfully written up afterward the way SLA definition or escalation protocol can.

**The broader lesson:** course SLOs aren't all meant to be done after a step is completed — some are prospective rather than retrospective. Check which kind a given SLO actually is before deciding when to sequence it, rather than just batching everything mapped to the same step together.
