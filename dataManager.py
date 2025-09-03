import pandas as pd

headers = ['Type', 'Year', 'player_yead_id', 'Name', 'Age', 'Team(s)', 'pos', 'G', 'GS', 'Att/Tgt', 'Yds/Rec', 'TD/Yds', '1D/YpR', 'Succ%/TD', 'Lng/1D', 'YpA/Succ%', 'YpG/Lng', 'ApG/RpG', 'Fmb/YpG', 'Awards/Ctch%', '/YpTgt', '/Fmb', '/Awards']

# Import csv to a pandas data frame
rawData = pd.read_csv("rawData.csv", header = 0, names = headers, low_memory=False)

playerYears = {}

for i in rawData[rawData['Year'] >= 2000].values:
    if i[3] in playerYears.keys():
        if i[0] == 'Rushing':
            playerYears[i[3]].append([i[1], i[0], i[9]])
        else:
            playerYears[i[3]].append([i[1], i[0], i[10]])
    else:
        if i[0] == 'Rushing':
            playerYears[i[3]] = [[i[1], i[0], i[9]]]
        else:
            playerYears[i[3]] = [[i[1], i[0], i[10]]]

toPop = []
for i in playerYears.keys():
    this = {}
    for j in playerYears[i]:
        if j[0] in this.keys():
            this[j[0]][1] += j[2]
        else:
            this[j[0]] = [0,j[2]]
        if j[1] == 'Rushing':
            this[j[0]][0] += j[2]
    good = False
    for j in this.keys():
        if this[j][0] > 50 and this[j][1] > 75:
            good = True
    if good == False:
        toPop.append(i)

for i in toPop:
    playerYears.pop(i)

print(playerYears)