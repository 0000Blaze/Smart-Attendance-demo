def convertdictToList(dict):
    list = []
    for x in dict:

        # print(dict[x][0])
        list.append(str(x) + " " + str(dict[x][0]) + " " + str(dict[x][1]))
    return list


# convertdictToList({"hg": ["hgh", "jhj"], "ty": [1, 45]})