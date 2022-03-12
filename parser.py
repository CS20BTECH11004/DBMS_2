from re import A
from numpy import tile


file = open("source.txt","r", encoding="utf8")
paper_count = int(file.readline())

def get_paper_info():
    global file 
    file_info =[]
    for i in range(paper_count):
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
                author_raw = file_inp[2:].replace("'","''").split(',')
                author_raw=[ele for ele in author_raw if len(ele)>0]
                author_raw = list(dict.fromkeys(author_raw))
                for cur_author in author_raw:
                    lastname = ""
                    middlename = ""
                    fname=""
                    if len(cur_author.split(' '))==0 :
                        continue
                    if len(cur_author.split(' '))==1 :
                        fname= cur_author.split(' ')[0]
                    elif len(cur_author.split(' '))==2:
                        fname= cur_author.split(' ')[0]
                        lastname= cur_author.split(' ')[1]
                    if(len(cur_author.split(' '))>2):
                        middlename = cur_author.split(' ')[1]
                        fname= cur_author.split(' ')[0]
                        lastname= cur_author.split(' ')[-1]
                    author.append((fname,middlename,lastname))
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
        if title == "":
            title = 'NULL'
        if year == "":
            year = 'NULL'
        if venue == "":
            venue ='NULL'
        if paper_id == "":
            continue
        if abstract == "":
            abstract = 'NULL'
        file_info.append((title,author,year,venue,paper_id,references,abstract))
    return file_info

# def main():
#     file_info=get_paper_info()
#     for a in file_info:
#         for b in a:
#             print(b)     

# if __name__=="__main__":
#     main()