# DB Decision Review Log

Course SLO 4.7. A log of times a database-related decision got questioned or checked, instead of just being accepted because "the assistant said so."

## 2026-07-21 — The `workspace` column, instead of one column per person

Papers needed to be kept separate by who uploaded them, without building full logins (that's explicitly out of scope for now). The first instinct — give each person their own column — was rejected. Instead: one `workspace` column, and everyone's papers just live in the same column as different row values. See `docs/decisions.md` (2026-07-21) and `docs/data-modeling.md` for the reasoning: a new column per person means changing the table's shape every time someone new shows up, which doesn't scale. One column, many rows, does.

## 2026-07-23 — A column that doesn't actually exist got caught

While writing `docs/db-vocabulary.md` (SLO 4.5, own-words definitions), a draft mentioned a column that isn't actually in the real table. Caught by checking it against the real `app/db/schema.py`, fixed before it got committed. The version that exists now only mentions real columns.

## 2026-07-23 — A mixed-up explanation caught in `data-modeling.md`

While writing `docs/data-modeling.md` (SLO 4.8), an early draft explained *why* the `workspace` column counts as "relational" in a way that didn't quite match how it actually works in this project. Caught and fixed before commit.

## 2026-07-28 — The course tracker itself was wrong about SLO 4.6

`docs/course-alignment.md` had claimed more progress on SLO 4.6 (schema-first habit) than had actually happened. Caught and corrected — it now honestly says "not yet genuinely practiced" instead of overstating it. This one's a bit different: it's the tracking document being checked for honesty, not the database code itself.

## 2026-07-31 — Two Step 5 decisions, actually questioned this time

Two decisions from Step 5 (`app/db/queries.py`) got pushed on directly, live, instead of accepted right away:

- **Should `insert_paper` hand back the new drawer number (`lastrowid`)?** First reaction was "why not also hand back the title" — worth asking, but it turned out to add nothing, since the title was already known (you gave it to the function yourself). The real question — can the drawer number ever come back wrong — got a real answer: only if a *different* filing clerk (a different database connection) were asked, which isn't what happens here. Same clerk files it and is asked immediately after, so it's safe in this specific code.
- **Was switching to `sqlite3.Row` (name-tagged results instead of unlabeled ones) actually necessary?** First instinct was that it's how we "know which paper we're getting" — that's wrong, that part is decided by the search filter (`WHERE workspace = ?`), not by name tags. Name tags only make it safer to read the paper's fields afterward (by name instead of position), so mislabeling doesn't sneak in later. Not strictly necessary for the app to work, but a real safety upgrade.

Compared to the four earlier entries — which were mostly the assistant catching something after the fact — this is the first time the questioning happened *before* just accepting the decision, which is the actual skill this SLO is checking for.
