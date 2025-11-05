import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, cross_val_score, KFold


df = pd.read_csv('data/statsByYear.csv')

df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis = 1)

target = 'nextYpT'
X = df.drop(columns=[target])
Y = df[target]

maxMean = [-1,-1000]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

cols = ['n_estimators','learning_rate', 'max_depth','subsample','colsample_bytree',
        'cv_score1', 'cv_score2', 'cv_score3',
        'mean_cv_score', 'cv_score_std', 'train_minus_cv']

tuning = pd.DataFrame(columns = cols)
    
cv = KFold(n_splits = 3, shuffle = True, random_state = 42)

for i in range(500):
    n_estimators= np.random.randint(80,90)
    learning_rate=np.random.uniform(0.04,0.05)
    max_depth=2
    subsample=np.random.uniform(0.5275,0.535)
    colsample_bytree=np.random.uniform(0.6,0.8)

    model = XGBRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        random_state=42,
        tree_method="hist"
    )

    model.fit(X_train, y_train, verbose = False)
    train_score = model.score(X_train, y_train)

    cv_scores = cross_val_score(model, X, Y, cv=cv, scoring = 'r2')

    new_row = {
        'n_estimators': n_estimators,
        'learning_rate': learning_rate,
        'max_depth': max_depth,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'cv_score1': cv_scores[0],
        'cv_score2': cv_scores[1],
        'cv_score3': cv_scores[2],
        'mean_cv_score': cv_scores.mean(),
        'cv_score_std': cv_scores.std(),
        'train_minus_cv': train_score - cv_scores.mean()
    }

    tuning.loc[len(tuning)] = new_row

    if cv_scores.mean() > maxMean[1]:
        maxMean[0] = i
        maxMean[1] = cv_scores.mean()

    if i % 10 == 0:
        print(f'{i} simulations completed. Max mean: {maxMean[0]}, {maxMean[1]}')
        tuning.to_csv('data/xgBoostTuning.csv')


print(tuning)

'''
model.fit(X_train, y_train, eval_set = [(X_test, y_test)], verbose = False)

plt.figure(figsize=(10, 8))
plot_importance(model, max_num_features=20)
plt.title("Top 20 Most Important Features for nextYpT")
plt.show()
'''