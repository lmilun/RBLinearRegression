import pandas as pd

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

eligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

for _,a in allSeasons.iterrows():
    if a['playerID'] in eligiblePlayers['playerID'].values:
        eligibleSeasons.loc[len(eligibleSeasons)] = a

eligibleSeasons = eligibleSeasons.sort_values(['Player', 'playerID', 'Season'])

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

cols = ['playerID', 'Player', 'Year', 'Age','YpT',
        'G', 'G%', 'GS', 'GS%', 'rushingAtt', 'rushingYds', 'rushingY/A', 'rushingTD', 'rushingY/G', 'rushing1D', 'rushingSucc%',
        'receivingTgt', 'receivingRec', 'receivingYds', 'receivingY/R', 'receivingTD', 'receivingY/G', 'receivingCtch%', 'receivingY/Tgt', 'receiving1D', 'receivingSuccs', 'receivingSucc%',
        'Touch', 'TotOff', 'YScm', 'APYd', 'RtY',
        
        'G-1', 'G%-1', 'GS-1', 'GS%-1', 'rushingAtt-1', 'rushingYds-1', 'rushingY/A-1', 'rushingTD-1', 'rushingY/G-1', 'rushing1D-1', 'rushingSucc%-1',
        'receivingTgt-1', 'receivingRec-1', 'receivingYds-1', 'receivingY/R-1', 'receivingTD-1', 'receivingY/G-1', 'receivingCtch%-1', 'receivingY/Tgt-1', 'receiving1D-1', 'receivingSucc%-1',
        'Touch-1', 'TotOff-1', 'YScm-1', 'APYd-1', 'RtY-1',
        
        'G-2', 'G%-2', 'GS-2', 'GS%-2', 'rushingAtt-2', 'rushingYds-2', 'rushingY/A-2', 'rushingTD-2', 'rushingY/G-2', 'rushing1D-2', 'rushingSucc%-2',
        'receivingTgt-2', 'receivingRec-2', 'receivingYds-2', 'receivingY/R-2', 'receivingTD-2', 'receivingY/G-2', 'receivingCtch%-2', 'receivingY/Tgt-2', 'receiving1D-2', 'receivingSucc%-2',
        'Touch-2', 'TotOff-2', 'YScm-2', 'APYd-2', 'RtY-2']

byYear = pd.DataFrame(columns=cols)

for _,a in eligibleSeasons.iterrows():
    if a['Touch'] >= 10:
        new_row = pd.DataFrame({'playerID': [a['playerID']], 'Player': [a['Player']], 'Year': [a['Season']], 'YpT': [a['YScm'] / a['Touch']]})
        byYear = pd.concat([byYear,new_row], ignore_index = True)

byYear = byYear.sort_values(by = ['playerID','Year'],ignore_index = True)

byYear.to_csv('data/statsByYear.csv')