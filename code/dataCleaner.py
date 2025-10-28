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

cols = ['playerID', 'Player', 'Year', 'Age',
        'YpT', 'G', 'possibleGames', 'G%', 'rushingAtt', 'rushingYds', 'rushingY/A', 'rushingTD', 'rushingY/G', 'rushing1D', 'rushingSucc%',
        'receivingTgt', 'receivingRec', 'receivingYds', 'receivingY/R', 'receivingTD', 'receivingY/G', 'receivingCtch%', 'receivingY/Tgt', 'receiving1D', 'receivingSucc%',
        'Touches', 'TotOff', 'YScm', 'APYd', 'RtY',
        
        'YpT-1', 'G-1', 'G%-1', 'GS-1', 'GS%-1', 'rushingAtt-1', 'rushingYds-1', 'rushingY/A-1', 'rushingTD-1', 'rushingY/G-1', 'rushing1D-1', 'rushingSucc%-1',
        'receivingTgt-1', 'receivingRec-1', 'receivingYds-1', 'receivingY/R-1', 'receivingTD-1', 'receivingY/G-1', 'receivingCtch%-1', 'receivingY/Tgt-1', 'receiving1D-1', 'receivingSucc%-1',
        'Touches-1', 'TotOff-1', 'YScm-1', 'APYd-1', 'RtY-1',
        
        'YpT-2', 'G-2', 'G%-2', 'GS-2', 'GS%-2', 'rushingAtt-2', 'rushingYds-2', 'rushingY/A-2', 'rushingTD-2', 'rushingY/G-2', 'rushing1D-2', 'rushingSucc%-2',
        'receivingTgt-2', 'receivingRec-2', 'receivingYds-2', 'receivingY/R-2', 'receivingTD-2', 'receivingY/G-2', 'receivingCtch%-2', 'receivingY/Tgt-2', 'receiving1D-2', 'receivingSucc%-2',
        'Touches-2', 'TotOff-2', 'YScm-2', 'APYd-2', 'RtY-2']

byYear = pd.DataFrame(columns=cols)
possibleGames = 0
rushingSuccs = 0
receivingSuccs = 0

for a in range(3,len(eligibleSeasons)):
    new_row = {col: None for col in cols}
    bad = False

    for b in new_row.keys():
        if b[-2:] == '-2':
            if eligibleSeasons['playerID'][a-2] == eligibleSeasons['playerID'][a]:
                new_row[b] = eligibleSeasons[b[:-2]][a-2]
            else:
                bad = True
                break

        elif b[-2:] == '-1':
            new_row[b] = eligibleSeasons[b[:-2]][a-1]

        elif b == 'Year':
            new_row[b] = eligibleSeasons['Season'][a]

        elif b == 'YpT':
            new_row[b] = eligibleSeasons['YScm'][a] / eligibleSeasons['Touch'][a]

        elif b == 'G%':
            possibleGames += 16 if eligibleSeasons['Season'][a] <= 2020 else 17
            new_row[b] = eligibleSeasons['G'][a] / possibleGames

        elif b == 'rushingY/A':
            new_row[b] = eligibleSeasons['rushingYds'][a] / eligibleSeasons['rushingAtt'][a]

        elif b == 'rushingY/G':
            new_row[b] = eligibleSeasons['rushingYds'][a] / eligibleSeasons['G'][a]

        elif b == 'rushingSucc%':
            rushingSuccs += eligibleSeasons['rushingSucc%'][a] * eligibleSeasons['rushingAtt'][a]
            new_row[b] = rushingSuccs * eligibleSeasons['rushingAtt'][a]

        elif b == 'receivingY/R':
            new_row[b] = eligibleSeasons['receivingYds'][a] / eligibleSeasons['receivingRec'][a]

        elif b == 'receivingY/G':
            new_row[b] = eligibleSeasons['receivingYds'][a] / eligibleSeasons['G'][a]

        elif b == 'receivingCatch%':
            new_row[b] = 

        elif b == 'receivingSucc%':
            receivingSuccs += eligibleSeasons['receivingSucc%'][a] * eligibleSeasons['receivingTgt'][a]
            new_row[b] = receivingSuccs * eligibleSeasons['receivingTgt'][a]

        elif b == 'playerID' and b == 'Player' and b == 'Year' and b == 'Age':
            new_row[b] = eligibleSeasons[b][a]
        
        else:
            new_row[b] = eligibleSeasons[b][a - 1] + eligibleSeasons[b][a]
    
    if bad == True:
        possibleGames = 0
        rushingSuccs = 0
        receivingSuccs = 0
        continue

    byYear = pd.concat([byYear,new_row], ignore_index = True)

byYear = byYear.sort_values(by = ['playerID','Year'],ignore_index = True)

byYear.to_csv('data/statsByYear.csv')