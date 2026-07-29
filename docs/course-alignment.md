# Course Alignment

**This project exists to be the vehicle for learning the course — it is not primarily a CV/portfolio piece.** When project progress and genuine course understanding are ever in tension, course understanding wins.

Tracks how the Evidence Intelligence Platform build satisfies the AI-native engineer curriculum written by the author's brother. He's reviewing informally, not officially grading; he's confirmed genuinely team/organization-dependent SLOs don't apply to a solo learner. Everything else — even material outside this app's direct feature set — is meant to be genuinely understood, not skipped for convenience.

**The course's Phase 1–7B numbering is a separate, complete curriculum arc from this project's own Step 1–9 roadmap — they are not synchronized.** A shared number (e.g. "Phase 4" vs. "Step 4") is coincidental, not structural. All phases must genuinely be covered eventually, regardless of which project step is active when the opportunity arises.

**Status key:** Satisfied (artifact exists and matches the requirement) · Partial (concept genuinely covered, dedicated artifact not yet made) · Not started · Deferred (explicit, agreed reason) · Skip (team/org-dependent, confirmed N/A for a solo learner).

---

## Phase 1: First Contact (Week 1)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.1 | Mental Models | Context window limits | `CLAUDE.md` "Context Window" section, 2+ examples | **Satisfied** — done, in this project's own CLAUDE.md |
| 1.2 | Mental Models | Goldfish analogy | `docs/onboarding/` video or 1-pager | Not started (concept from prior project; this artifact not in this repo) |
| 1.3 | Mental Models | Agent loop diagram | `agent-loop-diagram.md` | Not started |
| 1.4 | Mental Models | Chat vs. agent systems | `comparison-table.md` | Not started |
| 2.1 | Agent Fundamentals | Editor + Claude Code setup | `setup-verification.md` | Not started |
| 2.2 | Agent Fundamentals | Project folder structure | README explaining folders | **Satisfied** — `docs/project-structure.md` |
| 2.3 | Agent Fundamentals | Verify Claude Code works | `examples/first-task/` | Not started |
| 2.4 | Agent Fundamentals | Voice typing | Demo | Not started / optional |
| 2.9 | Agent Fundamentals | File formats guide | `file-formats-guide.md` | Not started (touched conceptually, no dedicated file) |

## Phase 2: The Mindset Shift (Week 2)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.5 | Mental Models | Producer vs. consumer mindset | `producer-mindset.md` | Not started |
| 1.6 | Mental Models | Fire-fighting vs. system-building | `time-audit.md` | Not started |
| 1.7 | Mental Models | 90/10 planning rule | plan.md before each implementation, ×3 | Not started |
| 1.8 | Mental Models | Patience through iteration | `iterations-log.md` | Not started |
| 2.5 | Agent Fundamentals | Detailed prompts | `prompt-comparison.md` | Not started |
| 2.6 | Agent Fundamentals | Feedback for refinement | `iteration-log.md` | Not started |
| 2.7 | Agent Fundamentals | Context window awareness | `session-management.md` | Not started |
| 2.10 | Agent Fundamentals | Zero/few-shot/CoT prompting | `technique-comparison.md` | Not started |
| 3.1 | Memory Engineering | Initial CLAUDE.md | CLAUDE.md w/ required sections | **Satisfied** |
| 3.5 | Memory Engineering | decisions.md / learning log | 10+ dated entries | **Satisfied** — `docs/decisions.md` |

## Phase 3: Memory Architecture (Week 3)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 3.3 | Memory Engineering | Update CLAUDE.md over time | git log, 5+ real updates | **Likely satisfied** — multiple real CLAUDE.md updates in git history |
| 3.6 | Memory Engineering | skills/docs/context folders | `structure.md` | Partial — `docs/` well organized, no `skills/` yet |
| 3.7 | Memory Engineering | "Close the loop" pattern | `loop-closures.md` | Partial — practiced informally throughout, no dedicated file |
| 3.9 | Memory Engineering | Skill files | `.claude/skills/` | Not started |
| 3.12 | Memory Engineering | Beads issue tracking | `.beads/` | Not started — using TodoWrite as a lighter substitute |
| 3.14 | Memory Engineering | Weekly maintenance | 4-week maintenance log | Not started — project isn't 4 weeks old yet |
| 3.16 | Memory Engineering | Memory continuum diagram | `memory-hierarchy.md` | Partial — taught live (dual-memory-system explanation), no diagram file |
| 2.8 | Agent Fundamentals | Strategic fresh sessions | `context-strategy.md` | Not started |
| 3.4 | Memory Engineering | CLAUDE.md under 100 lines | `refactoring-notes.md` | Not checked |
| 3.8 | Memory Engineering | Lazy loading for memory | `memory-map.md` | Not started |

## Phase 4: Connecting to the Real World (Week 4)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 4.1 | External Integration | What MCP is | `mcp-explainer.md` | Not started — optional per earlier agreement |
| 4.2 | External Integration | Secure DB credentials | `.env` + `.env.example` | Not started — no credentials yet, Step 6 |
| 4.5 | External Integration | DB vocabulary | `db-vocabulary.md` | In progress — scaffold created (10 terms), user filling in own-words definitions after a 6-question active-recall review confirmed solid conceptual grasp with some vocabulary imprecision (relational vs. flat data terminology, primary/surrogate/natural key distinction) |
| 4.3 | External Integration | MCP → DB connection | `mcp-setup.md` | Not started — optional |
| 4.4 | External Integration | READ-ONLY access | Permission proof | Not started |
| 4.6 | External Integration | Schema-first habit | `schema-first-checklist.md` | Not started — corrected 2026-07-28, not yet genuinely practiced |
| 4.9 | External Integration | Data analysis + viz | Analysis script, 2+ charts | Not started |
| 4.17 | External Integration | Why deployment | `deployment-rationale.md` | Not started — Step 8 |
| 4.18 | External Integration | Cron jobs | `cron-candidates.md` | Deferred — optional, not required for MVP |
| 4.19 | External Integration | Frontend vs. backend | `system-architecture.md` | Partial — explained conceptually, no diagram yet |
| 4.20 | External Integration | What an API is | `api-test.md` | Not started — Step 6 |
| 4.21 | External Integration | Env variables | `env-security.md` | Not started — Step 6 |

## Phase 5: Sharpening the Blade (Week 5)

| SLO | Domain | What it's testing | Required artifact | Status |
|---|---|---|---|---|
| 1.9–1.17, 1.20 | Mental Models | Advanced reflective practices (tab tax, friction maxxing, map vs. territory, ELI5 audit, scout mindset, stakes, biomimetic patterns, identity shift) | Various journals/docs | Not started |
| 4.7 | External Integration | Critically evaluate agent's DB decisions | `db-review-log.md` | Partial — the workspace-column pushback is a real logged case; dedicated file not made |
| 4.8 | External Integration | Relational vs. flat data | `data-modeling.md` | In progress — scaffold created, user filling in own-words content — **corrected: this is Phase 5, not Phase 4** |
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
| 4.22 | External Integration | **RAG for document Q&A** | `rag-evaluation.md`, 10+ docs, 5 working + 3 failing queries documented | **In progress** — PDF extraction done (Step 3), chunking built (Step 4), embeddings/Chroma next, then Step 6 Q&A. This is the centerpiece SLO of the whole project. |
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
| 5.5 | Autonomous Operations | Safety monitoring | Dashboard, 3+ metrics, 1wk data | Not started — mapped to Step 7/8 |
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
