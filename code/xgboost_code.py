import pandas as pd
import numpy as np
from xgboost import XGBRegressor, plot_importance
from sklearn.model_selection import train_test_split, cross_val_score, KFold
import matplotlib.pyplot as plt


df = pd.read_csv('data/statsByYear.csv')

df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis = 1)

target = 'nextYpT'
X = df.drop(columns=[target])
Y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

count = 0

cols = ['n_estimators','learning_rate', 'max_depth','subsample','colsample_bytree',
        'cv_score1', 'cv_score2', 'cv_score3', 'cv_score4', 'cv_score5',
        'mean_cv_score', 'cv_score_std']

tuning = pd.DataFrame(columns = cols)


for i in range(250):
    n_estimators= np.random.randint(100,1000)
    learning_rate=np.random.randint(1,30) / 100
    max_depth=np.random.randint(3,10)
    subsample=np.random.randint(50,100) / 100
    colsample_bytree=np.random.randint(50,100) / 100

    model = XGBRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate / 100,
        max_depth=max_depth,
        subsample=subsample / 100,
        colsample_bytree=colsample_bytree / 100,
        random_state=42,
        tree_method="hist"
    )

    cv = KFold(n_splits = 5, shuffle = True, random_state = 42)

    cv_scores = cross_val_score(model, X, Y, cv=cv, scoring = None)

    new_row = {
        'n_estimators': n_estimators,
        'learning_rate': learning_rate,
        'max_depth': max_depth,
        'subsample': subsample,
        'colsample_bytree': colsample_bytree,
        'cv_score1': cv_scores[0],
        'cv_score2': cv_scores[1],
        'cv_score3': cv_scores[2],
        'cv_score4': cv_scores[3],
        'cv_score5': cv_scores[4],
        'mean_cv_score': cv_scores.mean(),
        'cv_score_std': cv_scores.std()
    }

    tuning.loc[len(tuning)] = new_row

    count += 1

    if count % 5 == 0:
        print(f'{count} simulations completed')
        tuning.to_csv('data/xgBoostTuning.csv', index = False)

print(tuning)

'''
model.fit(X_train, y_train, eval_set = [(X_test, y_test)], verbose = False)

plt.figure(figsize=(10, 8))
plot_importance(model, max_num_features=20)
plt.title("Top 20 Most Important Features for nextYpT")
plt.show()
'''