# author=[]
# file_inp="#aNigga,Kala lund,Nigga nigger niggest"
# author = file_inp[2:].replace("'","''").split(',')
# author=[ele for ele in author if len(ele)>0]
# for cur_author in author:
#     lastname = None
#     middlename = None
#     fname=None
#     if len(cur_author.split(' '))==0 :
#         continue
#     if len(cur_author.split(' '))==1 :
#         fname= cur_author.split(' ')[0]
#     elif len(cur_author.split(' '))==2:
#         fname= cur_author.split(' ')[0]
#         lastname= cur_author.split(' ')[1]
#     if(len(cur_author.split(' '))>2):
#         middlename = cur_author.split(' ')[1]
#         fname= cur_author.split(' ')[0]
#         lastname= cur_author.split(' ')[-1]
#     val = (fname,middlename,lastname)
#     print(val)



l = [6, 5, 2, 1, 3, 4, 5, 2, 3]
l = list(dict.fromkeys(l))
print(l)