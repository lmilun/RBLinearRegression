import pandas as pd
import numpy as np
from xgboost import XGBRegressor, plot_importance
from sklearn.model_selection import train_test_split, cross_val_score, KFold
import matplotlib.pyplot as plt
import joblib

exclude = []
#exclude = ['Age', 'G%', 'G%-1', 'G%-2', 'G', 'G-1', 'G-2', 'receivingTD', 'receivingTD-1', 'receivingTD-2', 'receivingSucc%', 'receivingSucc%-1', 'receivingSucc%-2', 'receivingY/R', 'receivingY/R-1', 'receivingY/R-2', 'receivingY/A', 'receivingY/A-1', 'receivingY/A-2']

df = pd.read_csv('data/statsByYear.csv')

df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis = 1)
'''
df['Age'] = df['Age'].clip(upper=32)   # bucket ages
df['Age'] = df['Age'].astype('category')

# One-hot encode Age
df = pd.get_dummies(df, columns=['Age'], drop_first=True)
'''
df = df.drop(columns=[col for col in exclude if col in df.columns])

target = 'nextYpT'
X = df.drop(columns=[target])
Y = df[target]

maxMean = [-1,-1000,0]

X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42
)

cols = ['n_estimators','learning_rate', 'max_depth','subsample','colsample_bytree', 'gamma', 'min_child_weight',
        'cv_score1', 'cv_score2', 'cv_score3',
        'mean_cv_score', 'cv_score_std', 'train_minus_cv']

tuning = pd.DataFrame(columns = cols)
    
cv = KFold(n_splits = 3, shuffle = True, random_state = 42)

feature_accumulator = np.zeros(len(X.columns))
total_weight = 0.0
feature_names = X.columns.tolist()

for i in range(10000):
    n_estimators = np.random.randint(50,300)
    learning_rate = np.random.uniform(0.01,0.075)
    max_depth = 2
    subsample = np.random.uniform(0.4,1)
    colsample_bytree = np.random.uniform(0.5,1)
    gamma = np.random.uniform(0,3)
    min_child_weight = np.random.uniform(1,10)

    model = XGBRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        subsample=subsample,
        colsample_bytree=colsample_bytree,
        gamma = gamma,
        min_child_weight = min_child_weight,
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
        'gamma': gamma,
        'min_child_weight': min_child_weight,
        'cv_score1': cv_scores[0],
        'cv_score2': cv_scores[1],
        'cv_score3': cv_scores[2],
        'mean_cv_score': cv_scores.mean(),
        'cv_score_std': cv_scores.std(),
        'train_minus_cv': train_score - cv_scores.mean()
    }

    importance = model.feature_importances_
    weight = cv_scores.mean()

    # accumulate weighted importance
    feature_accumulator += importance * weight
    total_weight += weight


    tuning.loc[len(tuning)] = new_row

    if cv_scores.mean() > maxMean[1]:
        maxMean[0] = i
        maxMean[1] = cv_scores.mean()
        maxMean[2] = model
        print(f'{i} simulations completed. Max mean: {maxMean[0]}, {maxMean[1]}')
        tuning.to_csv('data/xgBoostTuning.csv')
        if total_weight > 0:
            avg_importance = feature_accumulator / total_weight
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'weighted_importance': avg_importance
            }).sort_values('weighted_importance', ascending=False)

            importance_df.to_csv("data/xgBoostFeatureImportance.csv", index=False)

    if i % 50 == 0:
        print(f'{i} simulations completed. Max mean: {maxMean[0]}, {maxMean[1]}')
        tuning.to_csv('data/xgBoostTuning.csv')
        if total_weight > 0:
            avg_importance = feature_accumulator / total_weight
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'weighted_importance': avg_importance
            }).sort_values('weighted_importance', ascending=False)

            importance_df.to_csv("data/xgBoostFeatureImportance.csv", index=False)
    
        if i % 100 == 0:
            joblib.dump(maxMean[2], f'data/xgb_best_model_after_{i}_0.pkl')



print(tuning)

joblib.dump(maxMean[2], 'data/xgb_best_model.pkl')

'''
model.fit(X_train, y_train, eval_set = [(X_test, y_test)], verbose = False)

plt.figure(figsize=(10, 8))
plot_importance(model, max_num_features=20)
plt.title("Top 20 Most Important Features for nextYpT")
plt.show()
'''