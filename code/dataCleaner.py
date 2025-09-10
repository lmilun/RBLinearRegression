import pandas as pd

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

potentiallyEligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

print(allSeasons)