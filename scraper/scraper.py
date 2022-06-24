# This module scrapers the table mapping from the URL into a pandas dataframe 

# Input : link to the URL
# Process : scrape the HTML and move it to a pandas dataframe and extract only the necessary columns
# Output : either a dictionary from number (anime episode) to list(manga chapters) or 
#           to object(name of ep, list of manga chaps) mapping 


import pandas as pd

map_URL = "https://listfist.com/list-of-one-piece-episode-to-chapter-conversion"

onepieceTable = pd.read_html(map_URL)
print(f"The total number of tables is : {len(onepieceTable)}")
