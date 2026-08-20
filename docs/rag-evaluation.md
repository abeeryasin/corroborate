# RAG Evaluation

Course SLO 4.22 — RAG for document Q&A. 10 real questions run against the `abeer-test` workspace (10 papers: dengue diagnostics, clinical management, vaccine development, Pakistan/Asia epidemiology — see `docs/decisions.md`, 2026-08-04, for the full corpus list). 6 produced correct, well-cited answers; 4 failed or fell short. Every claim below — in both the working and failing examples — was independently re-checked against the actual PDF text before being written up here, not just accepted at face value.

## Working examples

### 1. "Which dengue serotype has been most dominant in epidemics in Pakistan?"

Answered correctly from paper 5 (Khan et al., Pakistan epidemiology 1980–2014): DENV-2 identified as the major circulating serotype, with supporting detail (Karachi/Lahore/Faisalabad/Rawalpindi since 1994) pulled from a part of the paper separate from the passage the question was based on — confirming the answer synthesized across the paper rather than echoing a single lucky chunk.

### 2. "What are examples of inappropriate clinical management of dengue?"

Correctly synthesized across two different papers: paper 6 (misdiagnosis leading to inappropriate antimalarial/antibiotic treatment, due to overlapping symptoms) and paper 10, the WHO guidelines (a strong recommendation against NSAIDs in arboviral disease, due to bleeding risk). Both citations verified word-for-word against source text, including a direct quote ("WHO recommends against the use of non-steroidal anti-inflammatory medications (NSAIDs)... [Strong recommendation, low certainty evidence]") that wasn't in what was originally pasted into this eval but was found deeper in the guideline body.

### 3. "What is the impact of prior JE or YF vaccination on TAK-003 performance?"

Correctly answered entirely from paper 12 (the JE/YF vaccination subgroup study), with no blending in of paper 9 (TAK-003's general development story) even though both papers are about TAK-003. This is the positive control for the same paper pair that produced failure #2 below — proof retrieval *can* correctly distinguish similar papers when the question is specific enough, which makes failure #2 more clearly a crowding/fragmentation problem than a fundamental inability to tell the papers apart.

### 4. "Why is development of a vaccine against Dengue challenging?"

A broad question, correctly synthesized across paper 7 (Nicaragua severity study — Dengvaxia/QDenga efficacy limitations) and paper 9 (TAK-003 story — the "particularly intricate, long, and expensive endeavor" quote, verified verbatim). Unlike failures #1 and #4, which failed on broad questions needing multiple chunks *within one large document*, this succeeded because the relevant content in each of the two source papers happened to independently rank well.

### 5. "Which serotypes cause the most severe symptoms?"

Correctly answered from paper 7, citing DENV3's association with pleural effusion, poor capillary refill, and compensated shock (verified as a near-verbatim match to the paper's body text), plus the DENV4 short-circulation-time caveat (also verified). Initially looked like it might conflict with the paper's abstract, which attributes pleural effusion to DENV2 instead — checking the body text resolved this as two different specific comparisons reported in the same paper, not an error. Lesson: a mismatch against an abstract's simplified summary doesn't by itself mean a detailed answer is wrong.

### 6. "Is DENV-2II invasive? If yes, describe in detail."

Correctly answered from paper 3, including the "invasive potential" phrasing, its spread into the Americas/Caribbean (2019–2020), and the nuance that it hasn't fully displaced pre-existing genotypes everywhere (co-circulation with DENV-2III Asian-American, no displacement of DENV-2V Asian-I in Mainland SEA) — all verified verbatim. Notably, this is the same paper and same underlying content as failure #1 below, asked differently: naming the entity directly ("DENV-2II") instead of asking a comparative "which one is most X" question. Retrieval succeeded here, which suggests failure #1 wasn't about the content being unreachable, but about how superlative/comparative question phrasing interacts with chunk-level retrieval.

## Failing examples

### 1. "Which DENV serotype has the most extensive geographical distribution, and describe its historical spread?"

Expected answer: DENV-2II (Cosmopolitan), reported from the 1950s to 2020s in India, Malaysia, Singapore, Indonesia, and the Philippines, plus surges in Bangladesh, Sri Lanka, and Pakistan; established in Vietnam and Thailand in the mid-2000s, and Laos and Cambodia in the mid-2010s (paper 3).

Actual answer: "I don't know based on the uploaded papers."

**Cause:** a retrieval failure, not a generation failure — the right paragraph didn't make it into the 5 chunks handed to Claude. This is a 36-page paper split into ~1000-character chunks, so the total chunk count for this paper alone is far larger than the fixed `n_results=5` limit. The 5 chunks that were retrieved didn't contain the paragraph about geographical spread. This was also a comparative superlative question — answering it correctly requires comparing across multiple chunks (all four serotypes' distributions), not retrieving from a single chunk's embedding.

### 2. "What type of immune response does TAK-003 elicit?"

Expected answer: activation of both CD8+ and CD4+ T cells, tetravalent type-specific and cross-reactive memory B cells, and production of complement-fixing antibodies against all 4 DENV serotypes (paper 9).

Actual answer: a real, confidently-stated, correctly-cited answer — but incomplete, covering only neutralizing antibodies and general immunogenicity, missing the T-cell/B-cell/complement-fixing detail entirely. Nothing in the answer flagged it as partial.

**Cause:** two compounding problems, not one causing the other. First, the paragraph with the missing content was split mid-sentence across two chunks by the fixed 1000-character chunking (ends "...as well as production of c" in one chunk, continues "omplement-fixing antibodies..." in the next). Second, and primarily, the chunk containing most of that content never made the top-5 retrieved results at all — it was crowded out by 4 of the 5 slots going to paper 12 (a related but different TAK-003 paper) instead. Even if the right chunk had made it in, the fragmentation means only half the answer would have been retrievable from it alone.

### 3. "What is the reason given regarding superiority of NS1 antigen-based tests in detection of Dengue?"

Expected answer: NS1 tests can detect infection during the acute phase, don't require paired sera, and are suitable for decentralized settings — leading to timely diagnosis and improved patient management (paper 13, the Cochrane review protocol).

Actual answer: "I don't know based on the uploaded papers." Attributed the excerpts to discussing diagnostic accuracy/sensitivity but not a stated reason for superiority.

**Cause:** the PDF text for paper 13 extracted with a font-encoding problem specific to that file — words came out broken with stray spaces jammed into nearly every word (e.g. "further" became "fu r t h er"). When this corrupted text got embedded by the sentence-transformer model, the resulting vector was noisy and unreliable, which is why none of the retrieved chunks came from this paper at all. Second, separate issue: 3 of the 5 chunks that *were* retrieved (from paper 11 instead) were reference-list/bibliography entries, not actual body content — they ranked highly only because they're dense with the same keywords as the query ("NS1," "antigen," "dengue," "assay"), despite containing no explanatory content.

### 4. "What is the clinical management of patients with severe, suspected or confirmed, arboviral disease (hospitalized)?" (bonus, beyond the 3 required)

Expected answer: several pages of detailed clinical protocol exist in paper 10 (the WHO guidelines) covering this exact topic.

Actual answer: only general framing ("clinical management should be based on suspected aetiology," "standardization of procedures is best practice") with an explicit admission that specific protocols weren't in the retrieved excerpts.

**Cause:** the same underlying mechanism as failure #1, in a more extreme form. Paper 10 alone breaks into 281 chunks (it's a ~280-page document), and 62 of those specifically discuss severe-disease management or hospitalization — but only 5 chunks total were retrieved, and none were from that substantive pool. Instead, all 4 retrieved chunks from this paper were front-matter: executive summary scope, GRADE methodology notes, and a line literally pointing to "prior WHO guidance" for more detail rather than containing the detail itself. WHO guidelines repeat generic framing vocabulary ("recommendations," "clinical management," "guidance") consistently from the executive summary onward, so that vocabulary embeds as strongly "on-topic" as the actual buried protocol content — with only 5 slots against 281 chunks, the generic front-matter wins by sheer repetition.

## What this reveals

Every failure here is a **retrieval** failure, not a **generation** failure — in each case, Claude correctly followed its instruction to say "I don't know" (or answer only partially) rather than hallucinate, given what it was actually handed. The problem consistently happened one step earlier, in what `search()` chose to retrieve.

Three distinct root causes showed up, and the fixed `n_results=5` limit ([vector_store.py:36](../app/rag/vector_store.py#L36)) is implicated in three of the four failures:

1. **Comparative/superlative questions** (#1) inherently need to compare content across more chunks than a fixed small `n_results` can supply.
2. **Naive fixed-size chunking** ([chunking.py](../app/rag/chunking.py)) splits sentences mid-word with no awareness of structure (#2), and provides no way to distinguish reference lists from real content (#3).
3. **Large single documents** (#4, and to a lesser extent #1) get diluted — a 281-chunk document sampled at `n_results=5` barely gets touched at all, and generic front-matter/boilerplate language can out-rank deeply buried specifics.
4. **PDF extraction quality varies by source file** (#3) — one paper's font encoding broke extraction badly enough to degrade its embeddings, with no way for the current pipeline to detect or flag this.

These findings are the direct evidence behind the v2 items already logged in `CLAUDE.md`: structure-aware ingestion (PDF → clean Markdown before chunking) and section/paragraph-aware chunking instead of fixed-character splitting. Success #6 — a retry of failure #1's exact topic, phrased differently, which worked — is a useful reminder that these are retrieval-layer limitations tied to *how a question is asked and how content is chunked*, not a sign the underlying content is unreachable or the pipeline is fundamentally broken.

## Post-deployment validation (2026-08-21): the same failure mode recurs in a new domain

After deploying to Streamlit Community Cloud, the user uploaded 3 new papers on an entirely unrelated topic (diabetic ketoacidosis management — a 2024 ADA/Umpierrez et al. consensus report, a UK trust clinical guideline by Anthony (2017), and Rosenbloom & Hanas (1996)) and asked real questions live on the deployed app, independent of the original eval corpus.

**Broad question: "What is the management of DKA?"** Answered with only general/tangential content (an audit note, discharge education, mortality statistics, epidemiology) and explicitly said it lacked "specific fluid resuscitation regimens, insulin dosing rates, or electrolyte replacement targets" — despite the 2024 consensus report alone containing extensive detail (`0.1 units/kg` insulin dosing appears 8 times, `0.9% sodium chloride` fluid protocol 4 times, `potassium replacement` 8 times, `mmol/L` targets 79 times). Replicated locally to confirm the mechanism: the 3 papers produced 173 total chunks (126 from the consensus report alone), but only 5 ever get retrieved regardless of how much relevant content exists — the broad question pulled in introduction/epidemiology/audit-flavored chunks instead of the dense, numbers-heavy protocol paragraphs. **This is the exact same root cause as failure #4 above (large single document diluted by fixed `n_results=5`), independently reproduced in a completely different domain and corpus** — strong evidence this is a systemic retrieval-layer limitation, not something specific to the original dengue eval corpus.

**Narrower question: "What fluid resuscitation protocol is recommended for DKA?"** Worked well — pulled specific, correctly-cited protocol detail from both the 2024 consensus report (500–1,000 mL/h initial rate, correction over 24–48 hours, caution for fluid-overload risk groups) and Anthony (2017) (immediate fluids within 60 minutes, 4–6 L average deficit, 500 mL over 10 minutes for hypotensive patients). Confirms the same workaround pattern as success #6: narrowing a question's scope avoids the crowding problem, even without any code changes.

**One more live confirmation, inside that same good answer:** the Anthony (2017) excerpt cuts off mid-sentence — *"give 500 mL of 0.9% saline over 10 [minutes]"* — the exact mid-word/mid-sentence chunk fragmentation from failure #2, caught live in a new document. Reinforces that fixed-size chunking's boundary problem isn't a one-off; it's structural, and will keep recurring on any new paper until the chunking strategy itself changes (the v2 structure-aware chunking item above).
