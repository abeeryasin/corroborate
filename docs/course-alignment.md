# Course Alignment

Tracks how the Evidence Intelligence Platform build satisfies the AI-native engineer curriculum written by the author's brother. He's reviewing informally, not officially grading; he's confirmed genuinely team/organization-dependent SLOs don't apply to a solo learner. Everything else — even material outside this app's direct feature set — is meant to be genuinely understood, not skipped for convenience.

## Phases 1–3 (Weeks 1–3): First Contact, Mindset Shift, Memory Architecture

**Artifacts already produced in a prior project** — not being recreated here (file-formats-guide.md, comparison-table.md, producer-mindset.md, etc.). **But the underlying skills, especially memory architecture and prompting, are being actively practiced in this project, not just recapped:**

- `CLAUDE.md` — the project's "employee handbook" layer (SLO 3.1, 3.2).
- `docs/decisions.md` — the project "journal" layer; dated entries after real decisions, practicing the "close the loop" pattern (SLO 3.5, 3.7).
- The memory-continuum distinction (context window vs. CLAUDE.md vs. decisions log vs. the assistant's own private cross-session memory) taught directly against this project's real setup (SLO 3.16).
- Prompting technique (zero-shot/few-shot/chain-of-thought, iterative feedback) taught live whenever a real prompt-writing moment comes up — most notably the RAG system prompt in Step 6 (SLO 2.5, 2.6, 2.10).

## Phase 4: Connecting to the Real World

| SLO | Description | Roadmap step | Status |
|-----|--------------|--------------|--------|
| 4.5 | Define key DB terms | Step 2 — Metadata DB | Pending |
| 4.6 | Schema-first instruction | Step 2 — Metadata DB | Pending |
| 4.8 | Relational vs. flat data | Step 2 — Metadata DB | Satisfied — `workspace` column design (see decisions.md) |
| 4.2 | Securely store credentials | Step 6 — RAG Q&A | Pending |
| 4.21 | Environment variables, never hardcode secrets | Step 6 — RAG Q&A | Pending (`.env` / `.env.example` pattern already introduced) |
| 4.20 | What an API is | Step 6 — RAG Q&A | Pending |
| 4.19 | Frontend vs. backend | Step 5 — Streamlit v1 | Partially covered conceptually |
| 4.17 | Why agents need deployment (laptop vs. cloud) | Step 8 — Deploy | Pending |
| 4.18 | Cron jobs / scheduled automation | Step 8 — Deploy | Deferred — optional, not required for MVP |
| 4.1, 4.3, 4.4 | MCP: what it is, connect to a DB, read-only access | Step 2 — Metadata DB (optional: connect Claude Code to the SQLite DB via MCP) | Optional |
| 4.7 | Critically evaluate agent's DB decisions | Step 7 — Polish | Pending |
| 4.22 | Set up RAG for document Q&A | Step 4 + Step 6 | Pending — the centerpiece feature |

## Deferred — no natural home in this MVP

SLOs 4.9–4.16 (advanced data analysis, Procrustean bed risk, knowledge graphs). Either v2 territory or need a different tool entirely (a knowledge graph would mean standing up Neo4j for no other reason). Revisit as a standalone exercise once the core app is solid.

## Phase 7A/7B — reclassified, not blanket-skipped (corrected 2026-07-21)

Earlier version of this document wrongly treated "Phase 7A/7B" as a single skippable block. Corrected:

**Genuinely team/organization-dependent — skip:** 3.10 (share skill files with colleagues), 5.10 (onboard a colleague), 5.11 (team adoption playbook), 5.12 (org ROI reporting).

**Solo-adaptable — will be genuinely covered, mapped to where they fit:**

| SLO | Description | Where it fits |
|-----|--------------|----------------|
| 5.3 | Cost/comm/approval guardrails | Step 6 — a cost cap on Claude API calls, low-confidence → say-so-don't-guess |
| 5.5 | Safety/cost/latency monitoring | Step 7/8 |
| 5.6 | Escalation protocol | Step 8, adapted solo — what you actually do when it breaks |
| 5.13 | Production-infra / SLA mindset | Step 8 |
| 5.14 | Staging vs. production | Step 8 |
| 5.15 | Observability (cost, latency, errors) | Step 8/9 |
| 1.18 | Deliberate thinking before prompting | Ongoing practice, not tied to one step |
| 1.19 | Study what masters actually do | Adapted: study a real agentic workflow/blog/repo instead of a literal colleague to shadow |

**Awkward without a deployed multi-agent system — adapt, don't fully skip:**

| SLO | Description | Adaptation |
|-----|--------------|------------|
| 5.8 | Agent handoff protocol | Demonstrate the underlying idea via subagent-to-subagent handoff when a real occasion fits, not a dedicated exercise |
| 5.9 | Parallel agents | Directly demonstrable — run multiple Claude Code subagents in parallel on independent parts of this project when it's genuinely useful |

## Not yet received

The curriculum was pasted into a chat and cut off partway through Phase 7B by a length limit — anything after that point isn't reflected here yet.
