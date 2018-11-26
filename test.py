from utils import *

linkParams = [('titleSearch', 'aaa'), ('Action', 'on'), ('Adventure', 'on'), ('Horror', 'on')]
genrePrams = []
for i in range(0, 12):
    if (i < len(linkParams) and linkParams[i][0] != "titleSearch" and linkParams[i][1] == "on"):
        genrePrams.append(linkParams[i][0])
    else:
        genrePrams.append("")
# print(linkParams['titleSearch'])
titleParam = "%{}%".format(None)
searchResult = getData("filmSearch.sql", titleParam, *genrePrams)
print(searchResult)