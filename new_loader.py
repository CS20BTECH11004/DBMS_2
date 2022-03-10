from matplotlib.cbook import contiguous_regions
from sympy import false, true
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
def get_resch_paper_vals(all_papers):
    resch_paper_vals = []
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract) = paper
        resch_paper_vals.append((paper_id,title,abstract,venue,year))
    return resch_paper_vals
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
    all_papers = [ele for ele in all_papers if ele[4]!='NULL' and len(ele[1])!=0]

    #loading into research paper tabl
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        try:
            val = [paper_id,title,abstract,venue,year]
            cursor.execute("""
                            INSERT INTO research_paper(
                                                        paper_id,
                                                        paper_title,
                                                        abstract,
                                                        venue,
                                                        year)
                            VALUES(%s,%s,%s,%s,%s)""",(val,))
        except Exception as err_msg:
            print("error occured for paper id "+str(paper_id)+" !\n"+str(err_msg))


    #loading into reference table
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        for referenced_id in references: 
            try:
                val = [paper_id,referenced_id]
                cursor.execute( """
                                INSERT INTO reference_table(paper_id, paper_referenced) 
                                VALUES(%s,%s);""",(val,))
            except Exception as err_msg:
                print("error occured for paper id "+str(paper_id)+" !\n"+str(err_msg))

    #loading into insert_info
    author_index = 0
    for paper in all_papers:
        (title,author,year,venue,paper_id,references,abstract)=paper
        for cur_author in author:
            fname= cur_author.split(' ')[0]
            lastname = cur_author.split(' ')[-1]
            middlename = ""
            if(len(cur_author.split(' '))>2):
                middlename = cur_author.split(' ')[1]
            
            try:
                val = [author_index,fname,middlename,lastname]
                cursor.execute( """
                                INSERT INTO author_info(
                                                        author_id,
                                                        first_name,
                                                        middle_name,
                                                        last_name
                                                        )VALUES(%s,%s,%s,%s);""",(val,))
                author_index+=1
            except Exception as err_msg:
                print("error occured for paper id "+str(paper_id)+" !\n"+str(err_msg))

    #loading into author_group
    for paper in all_papers:
        author_rank = 0
        (title,author,year,venue,paper_id,references,abstract)=paper
        for cur_author in author: 
            
            try:
                val = [paper_id,author_rank,author_rank] #fix this
                cursor.execute( """
                                INSERT INTO author_group(paper_id, author_id, author_rank) 
                                VALUES(%s,%s,%s);""",(val,))
                author_rank +=1
            except Exception as err_msg:
                print("error occured for paper id "+str(paper_id)+" !\n"+str(err_msg))

    db_connection.commit()
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