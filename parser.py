file = open("source.txt","r",encoding="utf8")
paper_count = int(file.readline())

def get_paper_info():
    global file
    
    title = ""
    author= []
    year = int()
    venue = ""
    paper_id = ""
    references =[]
    abstract = ""

    file_inp = file.readline().strip() 
    while(file_inp!=""):
        if file_inp[0:2] == '#*':
            title = file_inp[2:]
        elif file_inp[0:2] == '#@':
            author = file_inp[2:].split(',')
        elif file_inp[0:2] == '#t':
            year = int(file_inp[2:])
        elif file_inp[0:2] == '#c':
            venue = file_inp[2:0]
        elif file_inp[0:6] == '#index':
            paper_id = file_inp[6:]
        elif file_inp[0:2] == '#%':
            references.append(file_inp[2:])
        elif file_inp[0:2] == '#!':
            abstract = file_inp[2:0]

        file_inp = file.readline().strip()

    return (title,author,year,venue,paper_id,references,abstract)