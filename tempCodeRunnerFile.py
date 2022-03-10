
        (title,author,year,venue,paper_id,references,abstract)=paper
        try:
            cursor.execute("""INSERT INTO research_paper(
                                paper_id,
                                paper_title,
                                abstract,
                                venue,
                                year)
                            VALUES(%s,%s,%s,%s,%s);""",((paper_id,title,abstract,venue,year),))
        except Exception as err_msg:
            print("error occured for paper id "+str(paper_id)+" !