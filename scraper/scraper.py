# This module scrapers the table mapping of One Piece anime episodes to titles and corresponding manga chapters
# from the URL into a pandas dataframe 

# Input : link to the URL
# Process : scrape the HTML and move it to a pandas dataframe and extract only the necessary columns
# Output : either a dictionary from number (anime episode) to list(manga chapters) or 
#           to object(name of ep, list of manga chaps) mapping 


import pandas as pd
from collections import defaultdict
from pymongo import MongoClient
from datetime import datetime

map_URL = "https://listfist.com/list-of-one-piece-episode-to-chapter-conversion"
db_URL = "mongodb+srv://amal:luffyisking@episodestochapters.l8qrtlg.mongodb.net/?retryWrites=true&w=majority"

onepieceTables = pd.read_html(map_URL)

onepieceDF = onepieceTables[0]
ep, title, ma = onepieceDF.columns  # Destructuring column titles
episodesN = len(onepieceDF)


def defRet():
    return "Episode not released yet"

# Default dictionaries to store the episodetochapter and episodetotitlemaps
episodeMap = defaultdict(defRet)
titleMap = defaultdict(defRet)


for i in range(0,episodesN):
    # print(onepieceDF.loc[i,title])
    episodeMap[str(onepieceDF.loc[i,ep])] = onepieceDF.loc[i,ma].replace(" ","").split("|")
    titleMap[str(onepieceDF.loc[i,ep])] = onepieceDF.loc[i,title]

cluster = MongoClient(db_URL)
db = cluster['animetomanga']
collexion1 = db['episodetochapter']
collexion2 = db['episodetotitle']

try:
    collexion1.delete_one({})
except Exception as e:
    print(f"Exception encountered while deleting from episodetochapter as : {e}")

try:
    collexion2.delete_one({})
except Exception as e:
    print(f"Exception encountered while deleting from episodetotitle as : {e}")


curDT =datetime.now()
uploadTime = str(curDT.year)+"-"+str(curDT.month)+"-"+str(curDT.day)+"  "+str(curDT.hour)+":"+str(curDT.minute)+":"+str(curDT.second)


collexion1.insert_one({"_id":"onepiecemap","content": episodeMap,"time_uploaded":uploadTime})
collexion2.insert_one({"_id":"onepiecetitles","content": titleMap,"time_uploaded":uploadTime})


# print(f"The map is : {type(onepieceDF.loc[i,ma])}")
