from re import A
from numpy import tile


file = open("source.txt","r", encoding="utf8")
paper_count = int(file.readline())

def get_paper_info():
    global file 
    file_info =[]
    for i in range(60):
        title = ""
        author= []
        year = ""
        venue = ""
        paper_id = ""
        references =[]
        abstract = ""

        file_inp = file.readline().strip() 
        while(file_inp!=""):
            if file_inp[0:2] == '#*':
                title = file_inp[2:].replace("'","''")
            elif file_inp[0:2] == '#@':
                author = file_inp[2:].replace("'","''").split(',')
            elif file_inp[0:2] == '#t':
                year = file_inp[2:]
            elif file_inp[0:2] == '#c':
                venue = file_inp[2:].replace("'","''")
            elif file_inp[0:6] == '#index':
                paper_id = file_inp[6:].replace("'","''")
            elif file_inp[0:2] == '#%':
                references.append(file_inp[2:].replace("'","''"))
            elif file_inp[0:2] == '#!':
                abstract = file_inp[2:].replace("'","''")
        
            file_inp = file.readline().strip()
        
        # for x in [title,author,year,venue,paper_id,references,abstract]:
        #     if x=="" or x==[]:
        #         x='NULL'
        if title == "":
            title = 'NULL'
        if year == "":
            year = 'NULL'
        if venue == "":
            venue ='NULL'
        if paper_id == "":
            paper_id = 'NULL'
        if abstract == "":
            abstract = 'NULL'
        file_info.append((title,author,year,venue,paper_id,references,abstract))
    
    return file_info