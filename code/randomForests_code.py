import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv('data/statsByYear.csv')

X = df.drop(columns=['playerID', 'Player', 'nextYpT'])
y = df['nextYpT']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

param_distributions = {
    'n_estimators': np.arange(100, 1001, 100),
    'max_depth': [None] + list(range(3, 21)),
    'min_samples_split': np.arange(2, 11),
    'min_samples_leaf': np.arange(1, 6),
    'max_features': ['sqrt', 'log2', None],
    'bootstrap': [True, False]
}

rf = RandomForestRegressor(random_state=42, n_jobs=-1)

search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_distributions,
    n_iter=30,
    scoring='r2',
    cv=3,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

search.fit(X,y)

print("\n=== Random Forest Randomized Search Results ===")
print("Best Parameters:")
for key, value in search.best_params_.items():
    print(f"  {key}: {value}")
print(f"\nBest CV R²: {search.best_score_:.4f}")


joblib.dump(search.best_estimator_, 'random_forest_best_model.pkl')



'''
Output:
=== Random Forest Randomized Search Results ===
Best Parameters:      
  n_estimators: 300   
  min_samples_split: 2
  min_samples_leaf: 5 
  max_features: sqrt
  max_depth: 18
  bootstrap: True

Best CV R²: 0.2085
'''