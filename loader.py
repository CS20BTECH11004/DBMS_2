from multiprocessing.dummy import connection
import psycopg2
from sympy import true
import parser
import time

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
            paper_title VARCHAR(500) NOT NULL,
            abstract VARCHAR(1000) NOT NULL,
            venue VARCHAR(500) NOT NULL,
            year VARCHAR(100) NOT NULL,
            PRIMARY KEY(paper_id, paper_title,venue)
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
            paper_id VARCHAR(10) NOT NULL references research_paper(paper_id),
            author_id VARCHAR(10) NOT NULL,
            author_rank INT NOT NULL,
            PRIMARY KEY(paper_id, author_id)
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
def input_into_db():
    db_connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    db_connection.autocommit = true
    cursor = db_connection.cursor()
    paper_count = parser.paper_count
    while paper_count > 0:
        (title,author,year,venue,paper_id,references,abstract) = parser.get_paper_info()
        if title == "":
            title = "UNAVAILABLE"
        if author == "":
            author = "UNAVAILABLE"
        if year == 0:
            year = "UNAVAILABLE"
        if venue == "":
            venue = "UNAVAILABLE"
        if abstract == "":
            abstract = "UNAVAILABLE"
        
        
        # #inserting into research_paper
        # sql="""INSERT INTO research_paper(
        #     paper_id,
        #     paper_title,
        #     abstract,
        #     venue,
        #     year
        #     )
        #     VALUES("""+"'"+paper_id+"',"+"'"+title+"',"+"'"+abstract+"',"+"'"+venue+"','"+str(year)+"');"
        # cursor.execute(sql)

        # #inserting into reference table
        # for ref_paper in references:
        #     cursor.execute("""
        #     INSERT INTO reference_table(paper_id, paper_referenced)
        #     VALUES(%s,%s)""",((paper_id,ref_paper),))
        try:
            sql = """INSERT INTO reference_table(paper_id, paper_referenced) 
            VALUES(%s,%s)"""
            cursor.executemany(sql,)
            db_connection.commit()
        except:
            db_connection.rollback()
        paper_count -=1
def load():
    start_time =time.time()
    print("loading started")
    input_into_db()
    end_time = time.time()
    print("loading ended")
    print("Time taken: "+str(end_time-start_time)+" seconds")

create_db()  
create_tables()
load()