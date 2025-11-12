import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

eligiblePlayers = pd.read_csv('data/rawPlayerData.csv')
allSeasons = pd.read_csv('data/rawSeasonsData.csv')

eligibleSeasons = pd.DataFrame(columns = allSeasons.columns)

for _,a in allSeasons.iterrows():
    if a['playerID'] in eligiblePlayers['playerID'].values:
        eligibleSeasons.loc[len(eligibleSeasons)] = a

eligibleSeasons = eligibleSeasons.sort_values(['Player', 'playerID', 'Season']).reset_index(drop=True)

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


cols = ['playerID', 'Player', 'Year', 'Age', 'nextYpT',
        
        'G', 'possibleG', 'G%', 'rushingAtt', 'rushingYds', 'rushingY/A', 'rushingTD', 'rushingY/G', 'rushing1D', 'rushingSucc', 'rushingSucc%',
        'receivingTgt', 'receivingRec', 'receivingYds', 'receivingY/R', 'receivingTD', 'receivingY/G', 'receivingCtch%', 'receivingY/Tgt', 'receiving1D', 'receivingSucc', 'receivingSucc%',
        'Touch', 'TotOff', 'YScm', 'APYd', 'RtY', 'YpT',
        
        'G-1', 'G%-1', 'rushingAtt-1', 'rushingYds-1', 'rushingY/A-1', 'rushingTD-1', 'rushingY/G-1', 'rushing1D-1', 'rushingSucc%-1',
        'receivingTgt-1', 'receivingRec-1', 'receivingYds-1', 'receivingY/R-1', 'receivingTD-1', 'receivingY/G-1', 'receivingCtch%-1', 'receivingY/Tgt-1', 'receiving1D-1', 'receivingSucc%-1',
        'Touch-1', 'TotOff-1', 'YScm-1', 'APYd-1', 'RtY-1', 'YpT-1',
        
        'G-2', 'G%-2', 'rushingAtt-2', 'rushingYds-2', 'rushingY/A-2', 'rushingTD-2', 'rushingY/G-2', 'rushing1D-2', 'rushingSucc%-2',
        'receivingTgt-2', 'receivingRec-2', 'receivingYds-2', 'receivingY/R-2', 'receivingTD-2', 'receivingY/G-2', 'receivingCtch%-2', 'receivingY/Tgt-2', 'receiving1D-2', 'receivingSucc%-2',
        'Touch-2', 'TotOff-2', 'YScm-2', 'APYd-2', 'RtY-2', 'YpT-2']

byYear = pd.DataFrame(columns=cols)
new_row = {col: 0 for col in cols}
bad = False

for a in range(1,len(eligibleSeasons)):
    if eligibleSeasons['playerID'][a-1] != eligibleSeasons['playerID'][a]:
        new_row = {col: 0 for col in cols}
        continue
    else:
        bad = False

    for b in new_row.keys():
        if b in ['playerID', 'Player', 'Age']:
            new_row[b] = eligibleSeasons[b][a]

        elif b == 'nextYpT':
            if eligibleSeasons['Touch'][a] <= 10:
                bad = True
                new_row[b] = 0
                break
            else:
                new_row[b] = eligibleSeasons['YScm'][a] / eligibleSeasons['Touch'][a]

        elif b == 'Year':
            new_row[b] = eligibleSeasons['Season'][a]

        elif b == 'possibleG':
            new_row[b] += 16 if eligibleSeasons['Season'][a-1] <= 2020 else 17

        elif b == 'G%':
            new_row[b] = new_row['G'] / new_row['possibleG']
        
        elif b == 'rushingY/A':
            if new_row['rushingAtt'] == 0:
                new_row[b] = 0
            else:
                new_row[b] = new_row['rushingYds'] / new_row['rushingAtt']
        
        elif b == 'rushingY/G':
            if new_row['G'] == 0:
                print(new_row['Year'], new_row['playerID'])
            else:
                new_row[b] = new_row['rushingYds'] / new_row['G']
        
        elif b == 'rushingSucc':
            new_row[b] += eligibleSeasons['rushingSucc%'][a-1] * eligibleSeasons['rushingAtt'][a-1]
        
        elif b == 'rushingSucc%':
            if new_row['rushingAtt'] == 0:
                new_row[b] = 0
            else:
                new_row[b] = new_row['rushingSucc'] / new_row['rushingAtt']
        
        elif b == 'receivingY/R':
            if new_row['receivingRec'] == 0:
                new_row[b] = 0
            else:
                new_row[b] = new_row['receivingYds'] / new_row['receivingRec']
        
        elif b == 'receivingY/G':
            new_row[b] = new_row['receivingYds'] / new_row['G']
        
        elif b == 'receivingCtch%':
            if new_row['receivingTgt'] == 0:
                new_row[b] == 0
            else:
                new_row[b] = new_row['receivingRec'] / new_row['receivingTgt']
        
        elif b == 'receivingY/Tgt':
            if new_row['receivingTgt'] == 0:
                new_row[b] == 0
            else:
                new_row[b] = new_row['receivingYds'] / new_row['receivingTgt']
        
        elif b == 'receivingSucc':
            new_row[b] += eligibleSeasons['receivingSucc%'][a-1] * eligibleSeasons['receivingTgt'][a-1]
        
        elif b == 'receivingSucc%':
            if new_row['receivingTgt'] == 0:
                new_row[b] == 0
            else:
                new_row[b] = new_row['receivingSucc'] / new_row['receivingTgt']
        
        elif b == 'YpT':
            if new_row['Touch'] == 0:
                new_row[b] == 0
            else:
                new_row[b] = new_row['YScm'] / new_row['Touch']

        elif b[-2:] == '-2':
            if a >= 2 and eligibleSeasons['playerID'][a-2] == eligibleSeasons['playerID'][a] and eligibleSeasons['Season'][a-2] == int(new_row['Year']) - 2 and eligibleSeasons['Touch'][a-2] > 10:
                if b == 'G%-2':
                    new_row[b] = eligibleSeasons['G'][a-2] / (16 if eligibleSeasons['Season'][a-2] <= 2020 else 17)
                
                elif b == 'rushingY/A-2':
                    if eligibleSeasons['rushingAtt'][a-2] == 0:
                        new_row[b] = 0
                    else:
                        new_row[b] = eligibleSeasons['rushingYds'][a-2] / eligibleSeasons['rushingAtt'][a-2]
                
                elif b == 'rushingY/G-2':
                    new_row[b] = eligibleSeasons['rushingYds'][a-2] / eligibleSeasons['G'][a-2]
                
                elif b == 'receivingY/R-2':
                    if eligibleSeasons['receivingRec'][a-2] == 0:
                        new_row[b] = 0
                    else:
                        new_row[b] = eligibleSeasons['receivingYds'][a-2] / eligibleSeasons['receivingRec'][a-2]
                
                elif b == 'receivingY/G-2':
                    new_row[b] = eligibleSeasons['receivingYds'][a-2] / eligibleSeasons['G'][a-2]
                
                elif b == 'receivingCtch%-2':
                    if eligibleSeasons['receivingTgt'][a-2] == 0:
                        new_row[b] = 0
                    else:
                        new_row[b] = eligibleSeasons['receivingRec'][a-2] / eligibleSeasons['receivingTgt'][a-2]
                
                elif b == 'receivingY/Tgt-2':
                    if eligibleSeasons['receivingTgt'][a-2] == 0:
                        new_row[b] = 0
                    else:
                        new_row[b] = eligibleSeasons['receivingYds'][a-2] / eligibleSeasons['receivingTgt'][a-2]
                
                elif b == 'YpT-2':
                    if eligibleSeasons['Touch'][a-2] == 0:
                        new_row[b] = 0
                    else:
                        new_row[b] = eligibleSeasons['YScm'][a-2] / eligibleSeasons['Touch'][a-2]
                else:
                    new_row[b] = eligibleSeasons[b[:-2]][a-2]
            else:
                bad = True
                break

        elif b[-2:] == '-1':
            if eligibleSeasons['Touch'][a-1] <= 10:
                bad = True
                break

            elif b == 'G%-1':
                new_row[b] = eligibleSeasons['G'][a-1] / (16 if eligibleSeasons['Season'][a-1] <= 2020 else 17)
            
            elif b == 'rushingY/A-1':
                if eligibleSeasons['rushingAtt'][a-1] == 0:
                    new_row[b] = 0
                else:
                    new_row[b] = eligibleSeasons['rushingYds'][a-1] / eligibleSeasons['rushingAtt'][a-1]
            
            elif b == 'rushingY/G-1':
                new_row[b] = eligibleSeasons['rushingYds'][a-1] / eligibleSeasons['G'][a-1]
            
            elif b == 'receivingY/R-1':
                if eligibleSeasons['receivingRec'][a-1] == 0:
                    new_row[b] = 0
                else:
                    new_row[b] = eligibleSeasons['receivingYds'][a-1] / eligibleSeasons['receivingRec'][a-1]
            
            elif b == 'receivingY/G-1':
                new_row[b] = eligibleSeasons['receivingYds'][a-1] / eligibleSeasons['G'][a-1]
            
            elif b == 'receivingCtch%-1':
                if eligibleSeasons['receivingTgt'][a-1] == 0:
                    new_row[b] = 0
                else:
                    new_row[b] = eligibleSeasons['receivingRec'][a-1] / eligibleSeasons['receivingTgt'][a-1]
            
            elif b == 'receivingY/Tgt-1':
                if eligibleSeasons['receivingTgt'][a-1] == 0:
                    new_row[b] = 0
                else:
                    new_row[b] = eligibleSeasons['receivingYds'][a-1] / eligibleSeasons['receivingTgt'][a-1]
            
            elif b == 'YpT-1':
                if eligibleSeasons['Touch'][a-1] == 0:
                    new_row[b] = 0
                else:
                    new_row[b] = eligibleSeasons['YScm'][a-1] / eligibleSeasons['Touch'][a-1]

            else:
                new_row[b] = eligibleSeasons[b[:-2]][a-1]
        
        else:
            new_row[b] += eligibleSeasons[b][a-1]
        

    if bad == False:
        this_row = pd.DataFrame([new_row])
        byYear = pd.concat([byYear,this_row], ignore_index = True)
        if len(byYear) % 1000 == 0:
            print('exporting:',new_row['Year'], new_row['playerID'], len(byYear))

byYear.to_csv('data/statsByYear.csv')




#For LSTM:
features = ['Age', 'G', 'rushingAtt', 'rushingY/A', 'receivingRec', 'receivingY/R', 'RtY', 'YardsPerTouch']
target = ['nextYpT']

df = eligibleSeasons.copy()

df = df.sort_values(['playerID', 'Season']).reset_index(drop=True)

df['YardsPerTouch'] = 0.0
mask = (df['Touch'] > 0)
df.loc[mask, 'YardsPerTouch'] = df.loc[mask, 'YScm'] / df.loc[mask, 'Touch']

df['is_gap'] = (df['Touch'] < 10).astype(int)

df['nextYpT'] = df.groupby('playerID')['YardsPerTouch'].shift(-1)

df = df.dropna(subset=['nextYpT'])

expanded_rows = []

for player, group in df.groupby('playerID'):
    group = group.sort_values('Season').reset_index(drop=True)
    expanded_rows.append(group.iloc[0])  # first season always included
    
    for i in range(1, len(group)):
        prev_age = group.iloc[i - 1]['Age']
        curr_age = group.iloc[i]['Age']
        age_gap = int(round(curr_age - prev_age))
        
        # Insert artificial "gap" seasons if the age jumps by >1
        if age_gap > 1:
            for missing_year in range(1, age_gap):
                gap_row = group.iloc[i - 1].copy()
                gap_row['Season'] = group.iloc[i - 1]['Season'] + missing_year
                gap_row['Age'] = prev_age + missing_year
                gap_row['is_gap'] = 1
                gap_row[features] = 0.0  # or np.nan if masking
                gap_row['nextYpT'] = np.nan
                expanded_rows.append(gap_row)
        
        expanded_rows.append(group.iloc[i])

expanded_df = pd.DataFrame(expanded_rows).reset_index(drop=True)

for f in features:
    expanded_df.loc[expanded_df['is_gap'] == 1, f] = 0.0

expanded_df = expanded_df.dropna(subset=['nextYpT']).reset_index(drop=True)

window_X = []
window_y = []
window_ids = []

for player, group in expanded_df.groupby('playerID'):
    group = group.sort_values('Season').reset_index(drop=True)
    
    X_player = group[features + ['is_gap']].values.astype('float32')
    y_player = group['nextYpT'].values.astype('float32')
    is_gap = group['is_gap'].values.astype('int')
    
    if len(group) < 2:
        continue
    
    for t in range(3, len(group)):
        # Skip targets corresponding to gap years
        if is_gap[t] == 1:
            continue
        window_X.append(X_player[:t])
        window_y.append(y_player[t])
        window_ids.append(player)

# --- Pad sequences ---
X_padded = pad_sequences(window_X, padding='post', dtype='float32')
y_array = np.array(window_y, dtype='float32')

print("X shape:", X_padded.shape)
print("y shape:", y_array.shape)

# --- Save outputs ---
np.save('data/X_LSTM.npy', X_padded)
np.save('data/y_LSTM.npy', y_array)

flattened = []
for pid, Xseq, yval in zip(window_ids, window_X, window_y):
    flattened.append({
        'playerID': pid,
        'seq_length': len(Xseq),
        'features': Xseq.tolist(),
        'target_nextYpT': float(yval)
    })
pd.DataFrame(flattened).to_csv('data/pre-LSTM.csv', index=False)