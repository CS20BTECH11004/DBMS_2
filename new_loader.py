from sympy import true
import parser
import psycopg2

user = "postgres"
password = "postgres"
db_name = "db_assgn3"



def get_all_papers():
    print("Started reading papers from file")
    all_papers = parser.get_paper_info()
    print("finished reading papers")
    return all_papers
def load_info_into_db():
    global user
    global password
    db_connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    db_connection.set_client_encoding('UTF-8')
    cursor = db_connection.cursor()

    all_papers = get_all_papers()
    #sql insert statement
    resch_paper_sql = """
    INSERT INTO research_paper(
        paper_id,
        paper_title,
        abstract,
        venue,
        year)
    VALUES(%s,%s,%s,%s,%s);"""
    #loading into research paper table
    for cur_paper in all_papers:
        try:
            cursor.execute(resch_paper_sql,(cur_paper,))    
        except:
            continue
    
def create_db():
    global user
    global password
    temp_connection = psycopg2.connect(
        database='postgres',
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    temp_connection.autocommit = true
    temp_cursor = temp_connection.cursor()

    temp_cursor.execute("DROP DATABASE IF EXISTS "+db_name+";")
    temp_cursor.execute("CREATE DATABASE "+db_name+" ENCODING = 'UTF8';")
    temp_connection.commit()
    temp_cursor.close()
    temp_connection.close()
def create_tables():
    global user
    global password
    db_connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    db_connection.set_client_encoding('UTF-8')
    cursor = db_connection.cursor()
    create_table_commands = [
        """
        CREATE TABLE research_paper(
            paper_id VARCHAR(10) UNIQUE NOT NULL,
            paper_title VARCHAR(500) UNIQUE,
            abstract TEXT,
            venue VARCHAR(500),
            year VARCHAR(100),
            PRIMARY KEY(paper_id, paper_title,venue)
        );
        """,
        """
        CREATE TABLE reference_table(
            paper_id VARCHAR(10) NOT NULL references research_paper(paper_id),
            paper_referenced VARCHAR(10) NOT NULL CHECK(paper_referenced != paper_id) references research_paper(paper_id),
            PRIMARY KEY(paper_id, paper_referenced)
        );
        """,
        """
        CREATE TABLE author_info(
            author_id VARCHAR(10) PRIMARY KEY NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            last_name VARCHAR(50) NOT NULL 
        )
        """,
        """
        CREATE TABLE author_group(
            paper_id VARCHAR(10) NOT NULL references research_paper(paper_id),
            author_id VARCHAR(10) NOT NULL references author_info(author_id),
            author_rank INT NOT NULL,
            PRIMARY KEY(paper_id, author_id)
        )
        """
    ]
    for command in create_table_commands:
        cursor.execute(command)
    db_connection.commit()
    cursor.close()
    db_connection.close()
def initialise_db():
    create_db()
    create_tables()
def main():
    initialise_db()
    load_info_into_db()        

if __name__=="__main__":
    main()