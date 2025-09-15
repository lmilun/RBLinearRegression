import pandas as pd

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

eligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

for _,a in allSeasons.iterrows():
    if a['playerID'] in eligiblePlayers['playerID'].values:
        eligibleSeasons.loc[len(eligibleSeasons)] = a

eligibleSeasons.to_csv('data/playerSeasons.csv')


cols = ['playerID', 'Player']

for i in range(20,40):
    cols.append(i)

yptTimeline = pd.DataFrame(columns = cols)

for _,a in eligiblePlayers.iterrows():
    new_row = pd.DataFrame({'playerID': [a['playerID']], 'Player': [a['Player']]})
    yptTimeline = pd.concat([yptTimeline, new_row], ignore_index=True)

yptTimeline.set_index('playerID', inplace=True)

for _,a in eligibleSeasons.iterrows():
    if a['Touch'] >= 10:
        yptTimeline.at[a['playerID'], a['Age']] = a['YScm'] / a['Touch']
 

yptTimeline.to_csv('data/age_vs_YPT.csv')

cols = ['playerID', 'Player', 'Year', 'YpT']

byYear = pd.DataFrame(columns=cols)

for _,a in eligibleSeasons.iterrows():
    if a['Touch'] >= 10:
        new_row = pd.DataFrame({'playerID': [a['playerID']], 'Player': [a['Player']], 'Year': [a['Season']], 'YpT': [a['YScm'] / a['Touch']]})
        byYear = pd.concat([byYear,new_row], ignore_index = True)

byYear = byYear.sort_values(by = ['playerID','Year'],ignore_index = True)

byYear.to_csv('data/statsByYear.csv')