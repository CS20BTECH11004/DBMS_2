from xml.etree.ElementTree import tostring
from matplotlib.cbook import contiguous_regions
from sympy import false, true
import parser
import psycopg2
import sys
import time
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
    db_connection.autocommit = false
    cursor = db_connection.cursor()

    all_papers = get_all_papers()

    res_paper_start=time.time()
    stdout_fileno = sys.stdout
    sys.stdout = open('paper_errors.txt', 'w')
    #loading into research paper tabl
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        val = (paper_id,title,abstract,venue,year)
        cursor.execute("""
            INSERT INTO research_paper(paper_id,paper_title,abstract,venue,year)
            VALUES(%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING""", val)
    db_connection.commit()
    sys.stdout.close()
    sys.stdout = stdout_fileno  
    res_paper_end=time.time()
    print("Resch papers done in "+str(res_paper_end-res_paper_start)+" seconds")   

    ref_start=time.time()
    stdout_fileno = sys.stdout
    sys.stdout = open('refernce_errors.txt', 'w')
    #loading into reference table
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        for referenced_id in references:
            if(paper_id==referenced_id):
                continue
            val = (paper_id,referenced_id)
            cursor.execute("""
                                INSERT INTO reference_table(paper_id, paper_referenced)
                                SELECT val.paper_id, val.paper_referenced
                                FROM  (
                                    VALUES (CAST(%s AS INT),CAST(%s AS INT))
                                ) val (paper_id, paper_referenced)
                                JOIN research_paper rp1 ON rp1.paper_id = val.paper_id
                                JOIN research_paper rp2 ON rp2.paper_id = val.paper_referenced;""",val ) 
    db_connection.commit()
    sys.stdout.close()
    sys.stdout = stdout_fileno
    ref_end=time.time()
    print("References done in "+str(ref_end-ref_start)+" seconds")   

    auth_lis_start=time.time()
    stdout_fileno = sys.stdout
    sys.stdout = open('author_table_errors.txt', 'w')
    #loading into author list
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        for cur_author in author:
            val = (cur_author[0],cur_author[1],cur_author[2])
            cursor.execute( """
                    INSERT INTO author_info(first_name,middle_name,last_name)VALUES(%s,%s,%s)
                    ON CONFLICT DO NOTHING ;""", val)
    db_connection.commit()
    sys.stdout.close()
    sys.stdout = stdout_fileno
    auth_lis_end=time.time()
    print("Author table done in "+str(auth_lis_end-auth_lis_start)+" seconds")   

    auth_grp_start=time.time()
    stdout_fileno = sys.stdout
    sys.stdout = open('auth_rank_errors.txt', 'w')
    s = "SELECT author_id, first_name, middle_name, last_name FROM author_info"
    cursor.execute(s)
    list_authors = cursor.fetchall()
    author_dict = {}
    for tmp_author in list_authors:
        author_dict[(tmp_author[1], tmp_author[2], tmp_author[3])] = tmp_author[0]

    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        rank = 1
        for cur_author in author:
            author_id = author_dict[(cur_author[0],cur_author[1],cur_author[2])]
            val = (paper_id, author_id, rank)
            rank += 1
            cursor.execute("""
                        INSERT INTO author_group(paper_id, author_id, author_rank) VALUES (%s, %s, %s)
                        ON CONFLICT DO NOTHING;""", val)

    db_connection.commit()
    sys.stdout.close()
    sys.stdout = stdout_fileno
    auth_grp_end=time.time()
    print("Author rank done in "+str(auth_grp_end-auth_grp_start)+" seconds")     


    cursor.close()
    db_connection.close()
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
            paper_id INT UNIQUE NOT NULL,
            paper_title VARCHAR(500) NOT NULL,
            abstract TEXT,
            venue VARCHAR(500),
            year VARCHAR(100),
            PRIMARY KEY(paper_id)
        );
        """,
        """
        CREATE TABLE reference_table(
            paper_id INT NOT NULL references research_paper(paper_id),
            paper_referenced INT NOT NULL CONSTRAINT no_self CHECK(paper_referenced != paper_id) 
            references research_paper(paper_id),
            PRIMARY KEY(paper_id, paper_referenced)
        );
        """,
        """
        CREATE TABLE author_info(
            author_id SERIAL PRIMARY KEY NOT NULL,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL, 
            CONSTRAINT unique_names UNIQUE(first_name, last_name,middle_name)
        );
        """,
        """
        CREATE TABLE author_group(
            paper_id INT NOT NULL references research_paper(paper_id),
            author_id INT NOT NULL references author_info(author_id),
            author_rank INT NOT NULL,
            PRIMARY KEY(paper_id, author_id)
        );
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
    start = time.time()
    load_info_into_db() 
    end = time.time() 
    print("time taken is "+str(end-start)+"seconds")      

if __name__=="__main__":
    main()