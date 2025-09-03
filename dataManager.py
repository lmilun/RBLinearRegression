import pandas as pd

headers = ['Type', 'Year', 'player_yead_id', 'Name', 'Age', 'Team(s)', 'pos', 'G', 'GS', 'Att/Tgt', 'Yds/Rec', 'TD/Yds', '1D/YpR', 'Succ%/TD', 'Lng/1D', 'YpA/Succ%', 'YpG/Lng', 'ApG/RpG', 'Fmb/YpG', 'Awards/Ctch%', '/YpTgt', '/Fmb', '/Awards']

# Import csv to a pandas data frame
rawData = pd.read_csv("rawData.csv", header = 0, names = headers, low_memory=False)


#Beginning process of cleaning data by finding all duplicate names
playerYears = {}

#Iterates through all years post 2000
for i in rawData[rawData['Year'] >= 2000].values:
    #Adds this player's season to playerYears
    if i[3] in playerYears.keys():
        #Rushing and receiving are separate
        if i[0] == 'Rushing':
            #In the form of name: [year, type, touches]
            playerYears[i[3]].append([i[1], i[0], i[9]])
        else:
            playerYears[i[3]].append([i[1], i[0], i[10]])
    else:
        if i[0] == 'Rushing':
            playerYears[i[3]] = [[i[1], i[0], i[9]]]
        else:
            playerYears[i[3]] = [[i[1], i[0], i[10]]]

toPop = []

#Removes players who never meet minimum seasons
for i in playerYears.keys():
    #Makes dictionary of all years for this player
    this = {}
    for j in playerYears[i]:
        if j[0] in this.keys():
            this[j[0]][1] += j[2]
        else:
            this[j[0]] = [0,j[2]]
        if j[1] == 'Rushing':
            this[j[0]][0] += j[2]

    #Checks if minimum requirements of 50 carries and 75 touches is met for each season
    good = False
    for j in this.keys():
        if this[j][0] >= 50 and this[j][1] >= 75:
            good = True
    
    #If minimums aren't met, player name is added to list of players to remove
    if good == False:
        toPop.append(i)

#Removes all players who don't ever meet minimum
for i in toPop:
    playerYears.pop(i)

#Now we are left with all players who at some point meet the minimum
#Next is to find all of the repeat names
#These players fit into two categories: players who skip a year and names that appear multiple times in the same season


count = 0

#Check for both of these issues
for i in playerYears.keys():
    bad = False
    prev = None
    prevType = None
    for j in playerYears[i]:
        #If it isn't the first entry for this player, either a year is skipped or both a year is repeated and type stays the same
        if prev != None and (j[0] - 1 > prev or (j[0] == prev and j[1] == prevType)):
            bad = True
            break
        prev = j[0]
        prevType = j[1]

    #Print out all of the "bad" players and what number they are:
    if bad == True:
        count += 1
        print(f'{count}\t {i}: {playerYears[i]}')