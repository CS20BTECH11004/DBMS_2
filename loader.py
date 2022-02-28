from multiprocessing.dummy import connection
import psycopg2
from sympy import true
import parser

user = "postgres"
password = "postgres"
db_name = "newer_db"

def create_db():
    temp_connection = psycopg2.connect(
        database='postgres',
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    temp_connection.autocommit = true
    temp_cursor = temp_connection.cursor()

    temp_cursor.execute("DROP DATABASE IF EXISTS "+db_name+";")
    temp_cursor.execute("CREATE DATABASE "+db_name+";")
    temp_cursor.close()
    temp_connection.close()
def create_tables():
    db_connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    db_connection.autocommit = true
    cursor = db_connection.cursor()
    create_table_commands = [
        """
        CREATE TABLE research_paper(
            paper_id VARCHAR(10) UNIQUE NOT NULL,
            paper_title VARCHAR(255) NOT NULL,
            abstract VARCHAR(1000) NOT NULL,
            venue VARCHAR(255) NOT NULL,
            author_id_index VARCHAR(10) UNIQUE NOT NULL,
            year INT NOT NULL,
            PRIMARY KEY(paper_id, paper_title,abstract,venue,author_id_index)
        );
        """,
        """
        CREATE TABLE reference_table(
            paper_id VARCHAR(10) NOT NULL references research_paper(paper_id),
            paper_referenced VARCHAR(10) NOT NULL CHECK(paper_referenced != paper_id),
            PRIMARY KEY(paper_id, paper_referenced)
        );
        """,
        """
        CREATE TABLE author_group(
            author_id_index VARCHAR(10) NOT NULL references research_paper(author_id_index),
            author_id VARCHAR(10) NOT NULL,
            author_rank INT NOT NULL,
            PRIMARY KEY(author_id_index,author_id)
        )
        """,
        """
        CREATE TABLE author_info(
            author_id VARCHAR(10) PRIMARY KEY NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            second_name VARCHAR(50) NOT NULL 
        )
        """
    ]
    for command in create_table_commands:
        cursor.execute(command)

    cursor.close()
    db_connection.close()


create_db()  
create_tables()
