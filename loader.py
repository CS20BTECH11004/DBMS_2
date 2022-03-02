from multiprocessing.dummy import connection
import psycopg2
from sympy import true
import parser
import time
#import pyodbc

user = "postgres"
password = "postgres"
db_name = "newer_db"
file_info = []
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
            paper_title VARCHAR(500) NOT NULL,
            abstract TEXT NOT NULL,
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
            middle_name VARCHAR(50),
            last_name VARCHAR(50) NOT NULL 
        )
        """
    ]
    for command in create_table_commands:
        cursor.execute(command)
    db_connection.commit()
    cursor.close()
    db_connection.close()
def get_parsed_data():
    global file_info
    print("reading from file")
    file_info = parser.get_paper_info()
def input_into_db():
    global file_info
    db_connection = psycopg2.connect(
        database=db_name,
        user=user,
        password=password,
        host='localhost',
        port= '5432')
    #db_connection.set_client_encoding('UTF-8')
    
    #db_connection.autocommit = true #too damn slow
    cursor = db_connection.cursor()
    cursor.execute("SET CLIENT_ENCODING TO 'UTF-8';")
    db_connection.commit()
    #cursor.fast_executemany =true
    
    #entering into research_paper
    resch_paper_sql = """
    INSERT INTO research_paper(
        paper_id,
        paper_title,
        abstract,
        venue,
        year
    )
    VALUES(%s,%s,%s,%s,%s)"""
    resch_paper_values = []
    for x in file_info:
        resch_paper_values.append((x[4],x[0],x[6],x[3],str(x[2])))
    cursor.executemany(resch_paper_sql,resch_paper_values)
    
    #entering into reftable
    ref_table_sql = """
    INSERT INTO reference_table(paper_id, paper_referenced) 
    VALUES(%s,%s)"""
    ref_table_vals = []
    for x in file_info:
        for y in x[5]:
            ref_table_vals.append((x[4],y))


    cursor.executemany(ref_table_sql,ref_table_vals)
    #entering into author_info
    auth_info_sql = """
    INSERT INTO author_info(
        author_id,
        first_name,
        middle_name,
        last_name
    )VALUES(%s,%s,%s,%s);"""
    auth_info_values = []
    ttt = 69 #ik im shitting my pants here but bear with me
    for x in file_info:
        for i in range(len(x[1])):
            fname= x[1][i].split(' ')[0]
            lastname = x[1][i].split(' ')[-1]
            middlename = ""
            if(len(x[1][i].split(' '))>2):
                middlename = x[1][i].split(' ')[1]
            auth_info_values.append((ttt,fname,middlename,lastname))
            ttt+=1
    cursor.executemany(auth_info_sql,auth_info_values)

    #entering into author_group
    auth_grp_sql = """
    INSERT INTO author_group(paper_id, author_id, author_rank) 
    VALUES(%s,%s,%s);"""
    auth_grp_vals = []
    for x in file_info:
        for i in range(len(x[1])):
            fname= x[1][i].split(' ')[0]
            lastname = x[1][i].split(' ')[-1]
            middlename = ""
            if(len(x[1][i].split(' '))>2):
                middlename = x[1][i].split(' ')[1]
            auth_id =""
            for t in auth_info_values:
                if t[1]==fname and t[2]==middlename and t[3]==lastname:
                    auth_id = t[0]
            auth_grp_vals.append((x[4],str(auth_id),str(i+1)))
    cursor.executemany(auth_grp_sql,auth_grp_vals)

    db_connection.commit()
    # try:
        
    # except:
    #     print("error occured.")
    #     db_connection.rollback()
    db_connection.close()
def load():
    print("inserting into db")
    input_into_db()
    print("finished task")

create_db()  
create_tables()
start_time =time.time()
get_parsed_data()
load()
end_time = time.time()
print("Time taken: "+str(end_time-start_time)+" seconds")