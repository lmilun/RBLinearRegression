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


model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    tree_method="hist"
)

cv = KFold(n_splits = 5, shuffle = True, random_state = 42)

cv_scores = cross_val_score(model, X, Y, cv=cv, scoring = None)

print(f"Cross-Validation Scores (R² for each fold): {cv_scores}")
print(f"Mean CV Score (R²): {cv_scores.mean():.4f}")
print(f"Std Dev of CV Scores: {cv_scores.std():.4f}")

model.fit(X_train, y_train, eval_set = [(X_test, y_test)], verbose = False)

plt.figure(figsize=(10, 8))
plot_importance(model, max_num_features=20)
plt.title("Top 20 Most Important Features for nextYpT")
plt.show()