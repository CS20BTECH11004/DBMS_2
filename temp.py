def unique(info_list):
    titles = set()
    new = []
    for i in reversed(info_list):
        if i[0] in titles:
            pass
        else:
            titles.add(i[0])
            new.append(i)
    
    return new


l = [('a', 1), ('b', 2), ('c', 3), ('a', 4)]
l = unique(l)

print(l)