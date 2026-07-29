# Relational vs. Flat Data

Course SLO 4.8. Explained using this project's actual `papers` table as the example.

## What is flat/spreadsheet data?

Everything lives in one table of rows and columns. Every fact about a record has to fit into that same row. Theres no seperate place to put a variable number of related data.

## What is relational data?

A relational database lets you separate data into structures so a new instance of something doesn't require changing the table's shape. Sometimes that means a new *row* in the same table — like our `workspace` column, where every friend's value lives in the same column, and the table just grows more rows. Sometimes it means a genuinely separate table, linked back by an ID (a foreign key) — which we haven't built yet in this project (that's JOIN territory, deliberately deferred — see decisions.md). Both are "relational" thinking; our `workspace` column is the simpler of the two techniques.

## The real example: the `workspace` column

I added one `workspace` column instead of adding a new *column* for each friend — the mistake would have been one column per person. Instead, one `workspace` column holds every friend's value, and the table grows by adding more *rows*, not more columns.

## Diagram

| id | title | workspace |
|----|-------|-----------|
| 1 | Maternal Mortality Trends in Rural Punjab | abeer |
| 2 | Climate Drivers of Dengue in Karachi | ali |
| 3 | Postpartum Hemorrhage Risk Factors | abeer |
| 4 | Mosquito Breeding and Monsoon Patterns | ali |
| 5 | Vaccine Uptake in Peri-Urban Clinics | sara |

Same `workspace` column, three different friends (abeer, ali, sara), told apart entirely by row values — no schema change needed to add a fourth or fiftieth friend.

## Why a spreadsheet wouldn't work here

A spreadsheet has no way to express "this paper belongs to a group, and the group's membership can change" without either adding a new column every time membership changes, or duplicating a paper's row once per person who can see it.
