import pandas as pd

headers = ['Type', 'Year', 'player_yead_id', 'Name', 'Age', 'Team(s)', 'pos', 'G', 'GS', 'Att/Tgt', 'Yds/Rec', 'TD/Yds', '1D/YpR', 'Succ%/TD', 'Lng/1D', 'YpA/Succ%', 'YpG/Lng', 'ApG/RpG', 'Fmb/YpG', 'Awards/Ctch%', '/YpTgt', '/Fmb', '/Awards']

# Import csv to a pandas data frame
rawData = pd.read_csv("rawData.csv", header = 0, names = headers)

print(rawData.tail())