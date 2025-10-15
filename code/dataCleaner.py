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

# --- Obtaining career statistics and lag features for all metrics ---

# Identify numeric columns to track
numeric_cols = ['G','Att','Rec','Touch','rushingYds','rushingTD',
                'receivingTgt','receivingYds','receivingTD','YScm']

# Initialize career stats container
careerStats = {}
withCareerStats = pd.DataFrame()

# Build cumulative stats through each season
for _, season in eligibleSeasons.sort_values(['playerID','Season']).iterrows():
    pid = season['playerID']
    if pid not in careerStats:
        careerStats[pid] = {stat: 0 for stat in numeric_cols}
        careerStats[pid]['Year'] = 0

    careerStats[pid]['Year'] += 1

    row = {
        'playerID': pid,
        'Player': season['Player'],
        'Season': season['Season'],
        'Age': season['Age'],
        'Year': careerStats[pid]['Year']
    }

    # Add career totals (_c) for all tracked stats
    for stat in numeric_cols:
        row[f'{stat}_c'] = careerStats[pid][stat]

    # Derived metrics
    row['rushingY/A_c'] = row['rushingYds_c'] / row['Att_c'] if row['Att_c'] > 0 else 0
    row['receivingY/R_c'] = row['receivingYds_c'] / row['Rec_c'] if row['Rec_c'] > 0 else 0
    row['receivingCtch%_c'] = (row['receivingYds_c'] / row['receivingTgt_c'] * 100) if row['receivingTgt_c'] > 0 else 0
    row['YpT_c'] = (row['rushingYds_c'] + row['receivingYds_c']) / row['Touch_c'] if row['Touch_c'] > 0 else 0

    # Current season metrics (_t-1)
    for stat in numeric_cols:
        row[f'{stat}_t-1'] = season[stat]

    # Derived metrics for current season (_t-1)
    row['rushingY/A_t-1'] = season['rushingYds'] / season['Att'] if season['Att'] > 0 else 0
    row['receivingY/R_t-1'] = season['receivingYds'] / season['Rec'] if season['Rec'] > 0 else 0
    row['receivingCtch%_t-1'] = (season['receivingYds'] / season['receivingTgt'] * 100) if season['receivingTgt'] > 0 else 0
    row['YpT_t-1'] = (season['rushingYds'] + season['receivingYds']) / season['Touch'] if season['Touch'] > 0 else 0

    withCareerStats = pd.concat([withCareerStats, pd.DataFrame([row])], ignore_index=True)

    # Update career totals
    for stat in numeric_cols:
        if pd.notna(season[stat]):
            careerStats[pid][stat] += season[stat]

# Sort by player and season
withCareerStats = withCareerStats.sort_values(['playerID','Season']).copy()

# --- Create lag features for t-2 and t-3 ---
lag_stats = numeric_cols + ['rushingY/A', 'receivingY/R', 'receivingCtch%', 'YpT']
for stat in lag_stats:
    withCareerStats[f'{stat}_t-2'] = withCareerStats.groupby('playerID')[f'{stat}_t-1'].shift(1)
    withCareerStats[f'{stat}_t-3'] = withCareerStats.groupby('playerID')[f'{stat}_t-1'].shift(2)

# Filter for players with at least 3 prior seasons
withCareerStats = withCareerStats[withCareerStats['Year'] >= 4]

# Add target variable (next season’s YpT)
withCareerStats['next_YpT'] = withCareerStats.groupby('playerID')['YpT_t-1'].shift(-1)

# Drop rows with no target (final career season)
model_data = withCareerStats.dropna(subset=['next_YpT']).copy()

# Save for XGBoost
model_data.to_csv('data/xgboost_input.csv', index=False)
print("Saved:", model_data.shape, "→ data/xgboost_input.csv")