import psycopg2
from sympy import true
import parser
from sh import pg_dump

user = "postgres"
password = "amandapanda"

db_connection = psycopg2.connect(
    database="postgres",
    user='postgres',
    password='postgres',
    host='localhost',
    port= '5432')
db_connection.autocommit = true
cursor = db_connection.cursor()


cursor.execute("DROP DATABASE testdb")
cursor.execute("CREATE DATABASE testdb")
#create tables
create_table_commands = [
    """
    CREATE TABLE research_paper(
        paper_id VARCHAR(10) NOT NULL,
        paper_title VARCHAR(255) NOT NULL,
        abstract VARCHAR(1000) NOT NULL,
        venue VARCHAR(255) NOT NULL,
        author_id_index VARCHAR(10) NOT NULL,
        year INT NOT NULL,
        PRIMARY KEY(paper_id, paper_title,abstract,venue,author_ids)
    );
    """,
    """
    CREATE TABLE reference_table(
        paper_id VARCHAR(10) NOT NULL references research_paper(paper_id),
        paper_referenced VARCHAR(10) NOT NULL CHECK(paper_referenced != paper_id)
        PRIMARY KEY(paper_id, paper_referenced)
    );
    """,
    """
    CREATE TABLE author_group(
        author_id_index VARCHAR(10) NOT NULL references research_paper(author_id_index),
        author_id VARCHAR(10) NOT NULL,
        author_rank INT NOT NULL
        PRIMARY KEY(author_id_index,author_id)
    )
    """,
    """
    CREATE TABLE author_info(
        author_id VARCHAR(10) NOT NULL
        first_name VARCHAR(50) NOT NULL
        second_name VARCHAR(50) NOT NULL 
    )
    """,

]
for command in create_table_commands:
    cursor.execute(command)

db_connection.close()