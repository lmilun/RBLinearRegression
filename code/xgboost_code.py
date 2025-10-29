import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor, plot_importance
import matplotlib.pyplot as plt
import joblib


df = pd.read_csv('data/statsByYear.csv')
print(df.shape)
print(df.head())

df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis = 1)

target = 'nextYpT'

X = df.drop(columns=[target])
Y = df[target]

train_df = df[df['Year'] <= 2020]
test_df = df[df['Year'] > 2020]

X_train = train_df.drop(columns=[target])
y_train = train_df[target]
X_test  = test_df.drop(columns=[target])
y_test  = test_df[target]


model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    early_stopping_rounds=20,
    tree_method="hist"
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.3f}")
print(f"Test RMSE: {rmse:.4f}")
print(f"Test R squared: {r2:.4f}")


plt.figure(figsize=(10, 8))
plot_importance(model, max_num_features=20)
plt.title("Top 20 Most Important Features for nextYpT")
plt.show()