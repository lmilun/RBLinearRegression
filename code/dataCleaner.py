import pandas as pd

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

potentiallyEligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

for _,a in allSeasons.iterrows():
    if a['Player'] in eligiblePlayers['Player'].values:
        potentiallyEligibleSeasons.loc[len(potentiallyEligibleSeasons)] = a

print(potentiallyEligibleSeasons)