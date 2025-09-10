import pandas as pd

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

potentiallyEligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

for _,a in allSeasons.iterrows():
    if a['Player'] in eligiblePlayers['Player'].values:
        potentiallyEligibleSeasons.loc[len(potentiallyEligibleSeasons)] = a

playerCounts = {}

for _,a in potentiallyEligibleSeasons.iterrows():
    if a['Player'] not in playerCounts.keys():
        playerCounts[a['Player']] = 1
    else:
        playerCounts[a['Player']] += 1

print(playerCounts)

for a in playerCounts.keys():
    for _,b in eligiblePlayers.iterrows():
        if a == b['Player'] and playerCounts[a] != b['Count']:
            pass