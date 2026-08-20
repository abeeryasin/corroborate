"""Functions for inserting and retrieving papers from the database."""

import sqlite3

DB_PATH = "data/papers.db"


def insert_paper(title, authors, year, journal, doi, abstract, workspace, filename, uploaded_at):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.execute(
        """
        INSERT INTO papers (title, authors, year, journal, doi, abstract, workspace, filename, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (title, authors, year, journal, doi, abstract, workspace, filename, uploaded_at),
    )
    connection.commit()
    paper_id = cursor.lastrowid
    connection.close()
    return paper_id


def get_papers_by_workspace(workspace):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(
        "SELECT * FROM papers WHERE workspace = ?",
        (workspace,),
    )
    papers = cursor.fetchall()
    connection.close()
    return papers


def get_all_workspaces():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.execute("SELECT DISTINCT workspace FROM papers ORDER BY workspace")
    workspaces = [row[0] for row in cursor.fetchall()]
    connection.close()
    return workspaces


def get_paper_by_id(paper_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.execute(
        "SELECT * FROM papers WHERE id = ?",
        (paper_id,),
    )
    paper = cursor.fetchone()
    connection.close()
    return paper


def delete_paper(paper_id):
    connection = sqlite3.connect(DB_PATH)
    connection.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
    connection.commit()
    connection.close()


def update_paper(paper_id, title, authors, year, journal, doi, abstract):
    connection = sqlite3.connect(DB_PATH)
    connection.execute(
        """
        UPDATE papers
        SET title = ?, authors = ?, year = ?, journal = ?, doi = ?, abstract = ?
        WHERE id = ?
        """,
        (title, authors, year, journal, doi, abstract, paper_id),
    )
    connection.commit()
    connection.close()


if __name__ == "__main__":
    insert_paper(
        title="Climate Drivers of Dengue Transmission in Pakistan",
        authors="A. Khan, S. Ahmed",
        year=2022,
        journal="Journal of Tropical Medicine",
        doi=None,
        abstract="A study of temperature and rainfall effects on dengue incidence.",
        workspace="abeer-test",
        filename="khan_dengue_2022.pdf",
        uploaded_at="2026-07-23T10:00:00",
    )

    papers = get_papers_by_workspace("abeer-test")
    print([dict(paper) for paper in papers])
