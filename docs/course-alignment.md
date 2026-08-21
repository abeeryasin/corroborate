# Course Alignment

**This project exists to be the vehicle for learning the course — it is not primarily a CV/portfolio piece.** When project progress and genuine course understanding are ever in tension, course understanding wins.

Tracks how the Corroborate build satisfies the AI-native engineer curriculum written by the author's brother. He's reviewing informally, not officially grading; he's confirmed genuinely team/organization-dependent SLOs don't apply to a solo learner. Everything else — even material outside this app's direct feature set — is meant to be genuinely understood, not skipped for convenience.

**The course's Phase 1–7B numbering is a separate, complete curriculum arc from this project's own Step 1–9 roadmap — they are not synchronized.** A shared number (e.g. "Phase 4" vs. "Step 4") is coincidental, not structural. All phases must genuinely be covered eventually, regardless of which project step is active when the opportunity arises.

**Status key:** Satisfied (artifact exists and matches the requirement) · Partial (concept genuinely covered, dedicated artifact not yet made) · Not started · Deferred (explicit, agreed reason) · Skip (team/org-dependent, confirmed N/A for a solo learner).

---

**Phases 1–3 were already completed in a prior project, before this repo existed (confirmed 2026-08-03; this was actually first decided back on 2026-07-20, but the rows below never got updated to reflect it — corrected now).** No dedicated artifacts for those phases are planned in *this* repo. Going forward, `CLAUDE.md` carries a standing rule to proactively call out, in the moment, whenever current work genuinely applies a Phase 1–3 concept (closing the loop, context window awareness, producer vs. consumer mindset, this project's own memory architecture, etc.) — ongoing awareness instead of a checklist.

---

## Phase 1: First Contact (Week 1)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.1 | Mental Models | Context window limits | `CLAUDE.md` "Context Window" section, 2+ examples | **Satisfied** — done in prior project, and independently done again here, in this project's own CLAUDE.md |
| 1.2 | Mental Models | Goldfish analogy | `docs/onboarding/` video or 1-pager | **Satisfied in prior project** — same underlying concept as 1.1 (context window limits), different explanatory device; no separate artifact in this repo |
| 1.3 | Mental Models | Agent loop diagram | `agent-loop-diagram.md` | **Satisfied in prior project** |
| 1.4 | Mental Models | Chat vs. agent systems | `comparison-table.md` | **Satisfied in prior project** |
| 2.1 | Agent Fundamentals | Editor + Claude Code setup | `setup-verification.md` | **Satisfied in prior project** |
| 2.2 | Agent Fundamentals | Project folder structure | README explaining folders | **Satisfied** — `docs/project-structure.md` |
| 2.3 | Agent Fundamentals | Verify Claude Code works | `examples/first-task/` | **Satisfied in prior project** — and continuously re-demonstrated by every session in this repo |
| 2.4 | Agent Fundamentals | Voice typing | Demo | Not started / optional — no confirmation this was done in the prior project either |
| 2.9 | Agent Fundamentals | File formats guide | `file-formats-guide.md` | **Satisfied in prior project** |

## Phase 2: The Mindset Shift (Week 2)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.5 | Mental Models | Producer vs. consumer mindset | `producer-mindset.md` | **Satisfied in prior project** |
| 1.6 | Mental Models | Fire-fighting vs. system-building | `time-audit.md` | **Satisfied in prior project** |
| 1.7 | Mental Models | 90/10 planning rule | plan.md before each implementation, ×3 | **Satisfied in prior project** |
| 1.8 | Mental Models | Patience through iteration | `iterations-log.md` | **Satisfied in prior project** |
| 2.5 | Agent Fundamentals | Detailed prompts | `prompt-comparison.md` | **Satisfied in prior project** |
| 2.6 | Agent Fundamentals | Feedback for refinement | `iteration-log.md` | **Satisfied in prior project** |
| 2.7 | Agent Fundamentals | Context window awareness | `session-management.md` | **Satisfied in prior project** |
| 2.10 | Agent Fundamentals | Zero/few-shot/CoT prompting | `technique-comparison.md` | **Satisfied in prior project** |
| 3.1 | Memory Engineering | Initial CLAUDE.md | CLAUDE.md w/ required sections | **Satisfied** |
| 3.5 | Memory Engineering | decisions.md / learning log | 10+ dated entries | **Satisfied** — `docs/decisions.md` |

## Phase 3: Memory Architecture (Week 3)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 3.3 | Memory Engineering | Update CLAUDE.md over time | git log, 5+ real updates | **Satisfied** — verified via real `git log --follow -- CLAUDE.md` (2026-08-03): 5 real commits, each a genuine content change (not busywork) |
| 3.6 | Memory Engineering | skills/docs/context folders | `structure.md` | **Satisfied** — `docs/` well organized, `.claude/skills/` now exists too (`.claude/skills/launch-app/SKILL.md`, 2026-08-03) |
| 3.7 | Memory Engineering | "Close the loop" pattern | `loop-closures.md` | **Satisfied in prior project — and genuinely practiced in this repo too**, every entry in `docs/decisions.md` (13+ and counting) is a real loop closure; no dedicated `loop-closures.md` file yet |
| 3.9 | Memory Engineering | Skill files | `.claude/skills/` | **Satisfied** — `.claude/skills/launch-app/SKILL.md` (2026-08-03), a real reusable skill (not a checkbox one): captures the exact launch command, the sentence-transformers cold-start gotcha, and three real Playwright quirks hit while testing Steps 5–6, so a future session doesn't re-derive them from scratch |
| 3.12 | Memory Engineering | Beads issue tracking | `.beads/` | Not started — using TodoWrite as a lighter substitute (this is a project-specific tooling choice, not something "already done" elsewhere) |
| 3.14 | Memory Engineering | Weekly maintenance | 4-week maintenance log | Not started — project isn't 4 weeks old yet (timing-dependent on this project specifically) |
| 3.16 | Memory Engineering | Memory continuum diagram | `memory-hierarchy.md` | **Satisfied in prior project — and genuinely practiced in this repo too**, real dual-memory-system (this repo's own docs vs. the assistant's persistent cross-session memory) discussed live 2026-08-03; no diagram file yet |
| 2.8 | Agent Fundamentals | Strategic fresh sessions | `context-strategy.md` | **Satisfied in prior project** |
| 3.4 | Memory Engineering | CLAUDE.md under 100 lines | `refactoring-notes.md` | **Satisfied** — verified 2026-08-03, `CLAUDE.md` is 48 lines, no refactoring needed |
| 3.8 | Memory Engineering | Lazy loading for memory | `memory-map.md` | **Satisfied in prior project** |

## Phase 4: Connecting to the Real World (Week 4)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 4.1 | External Integration | What MCP is | `mcp-explainer.md` | Not started — optional per earlier agreement |
| 4.2 | External Integration | Secure DB credentials | `.env` + `.env.example` | **Satisfied, with a naming caveat** — `.env` (real key, gitignored) / `.env.example` (placeholder, committed) both exist and were verified working; the secret being protected is the Claude API key, not a literal DB credential, since SQLite has no login — same underlying skill (secrets never in code, real/placeholder file split), title doesn't quite fit this project's shape |
| 4.5 | External Integration | DB vocabulary | `db-vocabulary.md` | **Satisfied** — 12 terms defined in the user's own words, fact-checked against the real schema, committed |
| 4.3 | External Integration | MCP → DB connection | `mcp-setup.md` | Not started — optional |
| 4.4 | External Integration | READ-ONLY access | Permission proof | Not started |
| 4.6 | External Integration | Schema-first habit | `schema-first-checklist.md` | Not started — corrected 2026-07-28, not yet genuinely practiced |
| 4.9 | External Integration | Data analysis + viz | Analysis script, 2+ charts | Not started |
| 4.17 | External Integration | Why deployment | `deployment-rationale.md` | **Satisfied (2026-08-21)** — `docs/deployment-rationale.md`, written by the user after a 3-question recall quiz on the real deploy just completed, assistant fact-checked (caught: the analogy contradicting the concept explanation on 24/7 availability, the "12-hour deletion timer" framing vs. the real sleep/wake mechanism, and an inaccurate claim that refreshing the page wipes data) |
| 4.18 | External Integration | Cron jobs | `cron-candidates.md` | Deferred — optional, not required for MVP |
| 4.19 | External Integration | Frontend vs. backend | `system-architecture.md` | **Satisfied** — `docs/system-architecture.md`, written by the user after a 5-question recall quiz, assistant fact-checked (caught one inaccuracy: described a "search tab" that doesn't exist in the actual UI, which is one continuous page, not `st.tabs`) |
| 4.20 | External Integration | What an API is | `api-test.md` | **Satisfied** — `docs/api-test.md`, written by the user after a 4-question recall quiz, assistant fact-checked (caught one inaccuracy: described "code" as being shared between machines, corrected to "a message/data," not a program) |
| 4.21 | External Integration | Env variables | `env-security.md` | **Satisfied** — `docs/env-security.md`, written by the user after a 3-question recall quiz, assistant fact-checked (sharpened one point: "the mistake was fixed" vs. "we confirmed via `git status` that nothing had leaked" are different claims) |

## Phase 5: Sharpening the Blade (Week 5)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.9–1.17, 1.20 | Mental Models | Advanced reflective practices (tab tax, friction maxxing, map vs. territory, ELI5 audit, scout mindset, stakes, biomimetic patterns, identity shift) | Various journals/docs | Not started |
| 4.7 | External Integration | Critically evaluate agent's DB decisions | `db-review-log.md` | **Satisfied** — `docs/db-review-log.md`, 5 dated entries: the workspace-column pushback (Step 2), catching an invented `topic` column in db-vocabulary.md, catching a relational-pattern mismatch in data-modeling.md, catching the SLO 4.6 mismarking itself, and a live-questioned review of two Step 5 decisions (`lastrowid`, `sqlite3.Row`) |
| 4.8 | External Integration | Relational vs. flat data | `data-modeling.md` | **Satisfied** — written by the user, committed — **corrected: this is Phase 5, not Phase 4** |
| 4.10 | External Integration | Iterate on analysis | `analysis-iterations.md` | Not started |
| 4.11 | External Integration | Reusable analysis skill | Skill file | Not started |
| 5.22 | Autonomous Operations | Worktrees for parallel tasks | Demo | Not started |
| 5.21 | Autonomous Operations | Structured output rubrics | `quality-rubric.md` | Not started |

## Phase 6: Systems Thinking (Week 6)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 3.10 | Memory Engineering | Share skills with colleagues | — | **Skip** — team-dependent |
| 3.13 | Memory Engineering | Task continuity across resets | `handoff.md` | Not started (though this whole project is arguably doing this across sessions already) |
| 3.15 | Memory Engineering | Diagnose memory/context issues | `troubleshooting-log.md` | Not started |
| 3.17 | Memory Engineering | Detect context poisoning | `context-poisoning-investigation.md` | Not started |
| 3.18 | Memory Engineering | Start-stop session hooks | Shell scripts / CLAUDE.md rules | Not started |
| 4.12 | External Integration | Emergent vs. traditional schema | `schema-philosophy.md` | Not started |
| 4.14 | External Integration | When KG vs. flat files vs. RAG | `data-structure-decision.md` | Not started — relevant once we've built RAG for real |
| 4.22 | External Integration | **RAG for document Q&A** | `rag-evaluation.md`, 10+ docs, 5 working + 3 failing queries documented | **Satisfied (2026-08-19)** — `docs/rag-evaluation.md`, 10 real questions run against the `abeer-test` workspace, 6 working + 4 failing (exceeds the 5+3 minimum), every claim independently re-verified against the actual PDF text before being written up. Confirmed the `n_results=5` crowding risk flagged on 2026-08-03 is real, and surfaced two more root causes: naive fixed-size chunking splitting sentences mid-word, and PDF font-encoding corruption degrading embeddings for one source file. Directly justified the structure-aware-ingestion v2 item now in `CLAUDE.md`. |
| 5.1 | Autonomous Operations | Autonomy spectrum | `autonomy-map.md` | Not started |
| 5.2 | Autonomous Operations | Guardrail design | `guardrails.md` | Not started |
| 5.4 | Autonomous Operations | Safety risk identification | `risk-assessment.md` | Not started |
| 5.16 | Autonomous Operations | Autonomy Slider (1–10) | `autonomy-slider.md` | Not started |
| 5.10 | Autonomous Operations | Onboard a colleague | — | **Skip** — team-dependent |
| 5.20 | Autonomous Operations | Responsible AI audit | `ethics-audit.md` | Not started |

## Phase 7A: Production Foundations (Weeks 7–9)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 4.13 | External Integration | Procrustean bed risks | `procrustean-audit.md` | Deferred — standalone exercise, agreed earlier |
| 4.15 | External Integration | Basic knowledge graph | Working KG, 50+ entities | Deferred — needs Neo4j/Graphiti, no natural fit in this app; standalone exercise |
| 4.16 | External Integration | Multi-hop KG queries | Query demo | Deferred — same as above |
| 3.11 | Memory Engineering | Team skill library | — | **Skip** — team-dependent |
| 5.3 | Autonomous Operations | Cost/comm/approval guardrails | Working code + test logs | Not started — mapped to Step 6 (Claude API cost cap) |
| 5.5 | Autonomous Operations | Safety monitoring | Dashboard, 3+ metrics, 1wk data | **Satisfied (2026-08-21)** — real "System health" dashboard in the app (4 metrics: questions asked, avg response time, errors, "I don't know" rate), backed by a real `question_log` table logging every question. `docs/safety-monitoring.md` written by the user after a 2-question recall quiz, fact-checked (content was fully accurate — only grammar/formatting needed cleanup). Adapted honestly for a solo low-traffic app: covers technical/system health only, not answer-quality checking (that's LLM-as-judge, explicitly deferred to v2), and the doc itself names that the SLO-demonstration reason carries more weight right now than genuine operational urgency at this scale |
| 5.6 | Autonomous Operations | Escalation protocol | `escalation-protocol.md` | Not started — mapped to Step 8, adapted solo |
| 5.7 | Autonomous Operations | Agent specialization | `agent-specialization.md` | Not started |
| 5.8 | Autonomous Operations | Agent handoff protocol | `handoff-demo.md` | Not started — adapt via subagent-to-subagent handoff when a real occasion fits |
| 5.9 | Autonomous Operations | Parallel agents | Demo, 2+ concurrent | Not started — directly demonstrable via Claude Code subagents when useful |

## Phase 7B: Scaling & Mastery (Weeks 10–12) — **incomplete, paste cut off again**

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.18 | Mental Models | Deliberate thinking before prompting | `deliberation-log.md`, 2wk | Not started — ongoing practice, not tied to one step |
| 1.19 | Mental Models | Study what masters actually do | `shadow-session-report.md` | Not started — adapt to studying a real workflow/repo instead of a literal colleague |
| 5.11 | Autonomous Operations | Team adoption docs | `team-playbook.md` | **Skip** — team-dependent |
| 5.12 | Autonomous Operations | AI ROI calculation | `roi-analysis.md` | **Skip** — team-dependent (no organization to report to) |
| 5.13 | Autonomous Operations | Production infra / SLA mindset | `sla-definition.md`, 2wk uptime log | Not started — mapped to Step 8 |
| 5.14 | Autonomous Operations | Staging vs. production | Working staging env | Not started — mapped to Step 8 |
| 5.15 | Autonomous Operations | Observability | Dashboard, cost/latency/startup | Not started — mapped to Step 8/9 |
| 5.17 | Autonomous Operations | Review queue w/ confidence scoring — low-confidence AI decisions get flagged for human review; queue volume shrinking over time *is* the measure of growing autonomy | `review-queue-report.md`, working queue run 2 weeks, daily volume tracked | Not started |
| 5.18 | Autonomous Operations | Micro-feedback loops — find the "2-minute win," small data-driven insights instead of long coaching conversations | `micro-feedback-results.md`, 5 insights tested with 3 users, >70% approval | Not started — the "3 users" requirement could lean on the friend/dengue-workspace scenario from earlier if it happens for real |
| 5.19 | Autonomous Operations | Evaluation harnesses — structured test cases (input, expected output, grading criteria) across 3 tiers: deterministic, LLM-as-judge, quality gate | `eval-results.md`, 10 benchmark tasks, baseline vs. improved score, target 8/10 | Not started — **this maps directly onto our own roadmap Step 9 ("Light eval")**, closest natural fit of anything in Phase 7B |

**Curriculum confirmed complete as of 2026-07-28** — this document now covers the entire course, Phase 1 through 7B, accurately grouped by real phase (not by domain-number coincidence). This is the authoritative source of truth for course progress going forward.
