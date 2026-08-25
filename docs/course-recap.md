# Corroborate — What You Actually Learned (a recap, not a quiz)

This covers the 40 already-satisfied SLOs from `docs/course-alignment.md`, grouped into five stories instead of a 40-item checklist — grouping into a few meaningful clusters, tying ideas to things you actually lived through in this project, and using concrete comparisons instead of jargon are the strongest evidence-based memory techniques that don't rely on self-testing.

**One cheap thing worth doing on your own:** reread this once in a few days, and once more a week after that. Even passive rereading spaced out over time sticks far better than reading it once and never again — spacing is the second-strongest evidenced technique, right behind the self-testing you're skipping.

---

## Chapter 1 — How you actually talk to an AI coding assistant

**The big idea:** Claude doesn't have a real memory like a person — it only "remembers" whatever fits on the whiteboard in front of it right now (its *context window*). Everything from this session — `text_cleaner.py`, the heading-orphan bug, choosing Haiku over Opus — sits on that whiteboard for *this* conversation only. In a brand-new conversation, none of it exists unless it's written down somewhere Claude can read again — which is the entire reason `CLAUDE.md` exists, and honestly, the entire reason RAG (the thing Corroborate is built around) exists too: it's a workaround for exactly this limitation, not a fancy buzzword. *(SLO 1.1)*

That same limitation is why you were taught early to think like a **producer, not a consumer** *(1.5)* — someone who actively directs the whiteboard, not someone who just reads whatever gets written on it. It's why detailed, specific prompts work better than vague ones *(2.5)*, why giving feedback and asking for another pass is normal, not a failure *(2.6)*, and why you deliberately start fresh Claude Code sessions at natural boundaries instead of dragging one giant conversation on forever *(2.8)*. Patience through iteration *(1.8)* isn't abstract either — you lived it today: the chunking fix took three real attempts (blind slicing → one-paragraph lookahead → the actual working fix) before it was right. That's not failure, that's what real iteration looks like.

*(Same family, also covered: agent-loop diagram, chat-vs-agent distinction, fire-fighting vs. system-building, the 90/10 planning rule, zero/few-shot/chain-of-thought prompting, verifying your dev setup works — 1.2, 1.3, 1.4, 1.6, 1.7, 2.1, 2.3, 2.7, 2.9, 2.10.)*

---

## Chapter 2 — How the project remembers things across sessions

**The big idea:** if Claude's memory resets every conversation, something has to carry the important state forward — real files, not magic. `CLAUDE.md` is the compressed, always-loaded summary (kept under 100 lines on purpose, *3.4*; updated for real over time, verified via actual `git log`, *3.3*). `docs/decisions.md` is the longer memory — every real decision, dated, with the reasoning behind it, so a future session doesn't have to re-derive *why* something was done a certain way *(3.5)*. That's the **"close the loop" pattern** *(3.7)*: don't just decide something, write down why, so the reasoning doesn't silently get lost.

`.claude/skills/` is a sharper kind of memory — not "what we decided" but "how to actually do this recurring thing," like the `launch-app` skill that remembers the exact command and the real gotchas already hit, so nobody rediscovers them from scratch *(3.9)*. Together — CLAUDE.md, decisions.md, skills, docs — these form a **memory continuum** *(3.16)*: some things live in the current conversation, some in always-loaded files, some in on-demand files you only open when relevant. That's the same shape as this very recap, and the same shape as your own assistant's cross-session memory system.

*(Also covered here: initial CLAUDE.md structure, organized docs/skills/context folders, lazy-loading memory instead of dumping everything into context — 3.1, 3.6, 3.8.)*

---

## Chapter 3 — How the app talks to the real world (databases, APIs, deployment)

**The big idea:** an app isn't just code — it's code plus real infrastructure: a database, secret keys, other services, and eventually a real URL real users hit. Secrets (your Claude API key) never live in code — they live in `.env` (real value, never committed) with `.env.example` as the public placeholder template *(4.2)*, and that split was actually verified to work, not just written down. You learned to describe your own database in plain words before trusting any tool's description of it *(4.5)*, and to actually push back when something looked wrong — the DB review log has five real, dated instances of you catching a mistake (an invented column, a mismatched pattern, even a mismarked SLO) instead of just accepting it *(4.7)*. That's not a nice-to-have — that's the actual skill of not blindly trusting an AI's claims about your own system.

You also learned the difference between data shaped like a spreadsheet (flat) and data shaped like linked tables referencing each other (relational) *(4.8)* — exactly why Corroborate has a `papers` table plus a separate chunks-in-Chroma setup, not one giant table. And you learned *why* you deployed the way you did, after real comparison, not just the default choice *(4.17)*; what the frontend/backend split actually looks like here (mostly there isn't one — Streamlit calls everything directly) *(4.19)*; what an API actually is in concrete terms *(4.20)*; and why environment variables matter *(4.21)*.

---

## Chapter 4 — RAG: the actual centerpiece, and the richest story of all

**The big idea:** RAG means don't hand the AI a giant pile of raw text and hope — search for the *specific* relevant pieces first, then hand the AI only those. This is Corroborate's whole reason for existing, and you have real, hard-won proof of where it works and where it breaks *(4.22)*: 10 real test questions, 6 that worked and 4 that genuinely failed — and critically, you didn't just accept "it failed," you dug into *why*. Three real root causes came out of that digging: a fixed `n_results=5` limit crowding out relevant papers when one paper had lots of similar-sounding chunks, naive fixed-size chunking slicing sentences in half, and one PDF's broken font encoding quietly poisoning its embeddings.

Every one of those three causes is something you personally watched go from *documented failure* → *diagnosed cause* → *verified fix* in this exact session: the messy-PDF cleanup step, the paragraph-aware chunker (including the real detour where the first fix wasn't actually enough), and the per-paper diversity cap. That's no longer abstract knowledge you read about — you watched the whole arc happen twice.

---

## Chapter 5 — Running it like a real, responsible product

**The big idea:** shipping code isn't the finish line — a real app needs to know if it's healthy, know when to escalate a problem to a human, and have a safe way to test changes before they hit real users. The System Health dashboard tracks real numbers (questions asked, response time, errors, "I don't know" rate) from a real logging table, not invented metrics *(5.5)*. The escalation protocol honestly distinguishes what Corroborate does today (tell the end user "I don't know") from what a *real* escalation system would do (alert a human operator when error rates, cost, or "I don't know" rates spike) — naming the gap instead of pretending it's solved *(5.6)*. The SLA doc states Corroborate's actual, honest uptime promise instead of fabricating data that doesn't exist — you can't promise real uptime numbers for a solo demo app, and pretending otherwise would be worse than saying so plainly *(5.13)*.

Staging vs. production *(5.14)* has the sharpest real lesson attached: it got adopted *after* several pushes had already gone straight to production, including one real incident — a genuine process miss, not a hypothetical one. The fix (a `staging` branch, a second deployed app, real code changes go through staging first) is real and working now, and the lesson outlives this one project: some rules need to exist *before* the risk happens, not just get written up after. Observability *(5.15)* rounds this chapter out — real cost tracking computed from actual API usage, not guessed numbers.

---

## Quick reference (for lookup, not for reading top to bottom)

| Chapter | Theme | SLOs |
|---|---|---|
| 1 | Working with an AI agent | 1.1–1.8, 2.1, 2.3, 2.5–2.10 |
| 2 | Project memory across sessions | 3.1, 3.3–3.9, 3.16 |
| 3 | Databases, APIs, deployment | 4.2, 4.5, 4.7, 4.8, 4.17, 4.19–4.21 |
| 4 | RAG (the centerpiece) | 4.22 |
| 5 | Running it responsibly | 5.5, 5.6, 5.13–5.15 |
