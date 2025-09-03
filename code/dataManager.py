import pandas as pd

headers = ['Type', 'Year', 'player_yead_id', 'Name', 'Age', 'Team(s)', 'pos', 'G', 'GS', 'Att/Tgt', 'Yds/Rec', 'TD/Yds', '1D/YpR', 'Succ%/TD', 'Lng/1D', 'YpA/Succ%', 'YpG/Lng', 'ApG/RpG', 'Fmb/YpG', 'Awards/Ctch%', '/YpTgt', '/Fmb', '/Awards']

# Import csv to a pandas data frame
rawData = pd.read_csv("data/rawData.csv", header = 0, names = headers, low_memory=False)


#Beginning process of cleaning data by finding all duplicate names
playerYears = {}


for i in rawData.values:
    #Adds this player's season to playerYears
    if i[3] in playerYears.keys():
        #Rushing and receiving are separate
        if i[0] == 'Rushing':
            #In the form of name: [year, type, touches]
            playerYears[i[3]].append([i[1], i[0], i[9]])
        else:
            playerYears[i[3]].append([i[1], i[0], i[10]])
    #Only add players if they were active post-2000
    elif i[1] >= 2000:
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

with open("data/problemNames.txt", "w") as file:
    pass

#Check for both of these issues
for i in playerYears.keys():
    maxRushYear = 0
    minRushYear = 0
    maxRecYear = 0
    minRecYear = 0
    bad = False
    prev = None
    prevType = None
    issues = []
    for j in playerYears[i]:
        #If it isn't the first entry for this player, either a year is skipped or both a year is repeated and type stays the same
        if prev != None and j[1] == prevType:
            if j[0] + 1 < prev:
                bad = True
                issues.append(f'Skipped a year {j[0]} {j[1]}')
            if j[0] == prev:
                issues.append(f'Repeated a year {j[0]} {j[1]}')
                bad = True
        prev = j[0]
        prevType = j[1]
        if j[1] == 'Rushing':
            if maxRushYear == 0:
                maxRushYear = j[0]
            minRushYear = j[0]
        else:
            if maxRecYear == 0:
                maxRecYear = j[0]
            minRecYear = j[0]
        
    if minRushYear > maxRecYear or minRecYear > maxRushYear:
        issues.append('Rush and Rec are offset')
        bad = True

    #Print out all of the "bad" players and what number they are:
    if bad == True:
        count += 1
        with open("data/problemNames.txt", "a") as file:
            file.write(f'{count}. {i}: \n\t{playerYears[i]} \n\t {issues}\n\n')