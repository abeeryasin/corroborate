# Database Vocabulary

Course SLO 4.5. Each term defined in my own words, with a real example from this project where one exists.

## PRIMARY KEY

Definition: primary key is the column the database itself uses to uniquely identify a row

Example from this project: id

## Surrogate key

Definition: surrogate key is internal, manufactured meaningless outside our database

Example from this project: id

## Natural key

Definition: real world identifier that exists independent of our database

Example from this project: doi

## NOT NULL

Definition: signifies that a field can't be left empty in the database

Example from this project: `title`, `workspace`, and `uploaded_at` are all NOT NULL in the papers table — every row must have a value for these three.

## NULL

Definition: explicitly marked as having no value — different from just "empty," it's a deliberate marker that no value exists, not a blank left unfilled

Example from this project: when testing `insert_paper`, we passed `doi=None` for a test paper that has no DOI. It was stored as NULL and printed back as `None` when we queried it.

## Data type (TEXT / INTEGER)

Definition: type of data to be entered in each column Title will have text, Year will have numbers(integers)

Example from this project: Title will have text, Year will have numbers(integers)

## Parameterized query / SQL injection

Definition: '?' placeholders prevent malicious data from being reinterpreted as code(and always treated as data) and preventing SQL injection attacks.

Example from this project: All queries pass values as a separate tuple to `.execute()`, never by pasting values directly into the SQL text.

## AUTOINCREMENT

Definition: automatic increase in values as they're added

Example from this project: id column adds a number to the id as more files are added

## Schema

Definition: structure or blueprint of a database

Example from this project: schema.py stores our schema, how the table is laid out, columns names etc, what type of data each column will contain

## JOIN

Definition: JOIN combines rows from two or more tables based on a related column, letting you pull data that's spread across multiple tables into one result

Example (not yet used in this project — deliberately deferred, see decisions.md):

## DROP

Definition: DROP deletes a database object entirely. It's not reversible unless you have a backup.

Example: can use DROP to delete my papers table along with its data and structure

## INDEX

Definition: INDEX is a data structure that speeds up lookups on a column, similar to an index in a book.

Example: not yet used in this project — our `papers` table is small enough that a full scan is fast; would matter once the table grows large.
