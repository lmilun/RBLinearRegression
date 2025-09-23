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


#Obtaining career statistics up to given season
cols = ['playerID', 'Player', 'Year','Att','Rec','Touch','rushingYds','rushingY/A','rushingTD','receivingTgt','receivingYds','receivingY/R','receivingTD','receivingCtch%','YScm','YpT']

careerStats = {}

numeric_cols = ['Season','Att','Rec','Touch','rushingYds','rushingTD',
                'receivingTgt','receivingYds','receivingTD','YScm']

# Convert columns to numeric (errors='coerce' turns non-numeric strings into NaN)
eligibleSeasons[numeric_cols] = eligibleSeasons[numeric_cols].apply(pd.to_numeric, errors='coerce')


withCareerStats = pd.DataFrame(columns = cols)

for _, season in eligibleSeasons[::-1].iterrows():  # oldest -> newest
    pid = season['playerID']
    
    # Initialize career stats
    if pid not in careerStats:
        careerStats[pid] = {'Att':0, 'Rec':0, 'Touch':0, 'rushingYds':0, 'rushingTD':0,
                            'receivingTgt':0, 'receivingYds':0, 'receivingTD':0, 'YScm':0}

    # Update cumulative totals first
    for stat in careerStats[pid]:
        if pd.notna(season[stat]):
            careerStats[pid][stat] += season[stat]

    # Build row
    row = {
        'playerID': pid,
        'Player': season['Player'],
        'Year': season['Season'],
        'Att': careerStats[pid]['Att'],
        'Rec': careerStats[pid]['Rec'],
        'Touch': careerStats[pid]['Touch'],
        'rushingYds': careerStats[pid]['rushingYds'],
        'rushingTD': careerStats[pid]['rushingTD'],
        'receivingTgt': careerStats[pid]['receivingTgt'],
        'receivingYds': careerStats[pid]['receivingYds'],
        'receivingTD': careerStats[pid]['receivingTD'],
        'YScm': careerStats[pid]['YScm']
    }

    # Derived stats
    row['rushingY/A'] = row['rushingYds'] / row['Att'] if row['Att'] > 0 else 0
    row['receivingY/R'] = row['receivingYds'] / row['Rec'] if row['Rec'] > 0 else 0
    row['receivingCtch%'] = (row['receivingYds'] / row['receivingTgt'] * 100) if row['receivingTgt'] > 0 else 0
    row['YpT'] = (row['rushingYds'] + row['receivingYds']) / row['Touch'] if row['Touch'] > 0 else 0

    # Only append rows for years >= 2000
    if row['Year'] >= 2000:
        withCareerStats = pd.concat([withCareerStats, pd.DataFrame([row])], ignore_index=True)

withCareerStats.to_csv('data/withCareerStats.csv')