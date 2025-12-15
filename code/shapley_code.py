import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

model = joblib.load('data/xgb_first_simulation_best.pkl')

df = pd.read_csv('data/statsByYear.csv')
df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis=1)

target = 'nextYpT'
X = df.drop(columns=[target])
y = df[target]

explainer = shap.Explainer(model, X)
shap_values = explainer(X)


shap_matrix = shap_values.values

shap_table = pd.DataFrame({
    "feature": X.columns,
    "mean_abs_shap": np.mean(np.abs(shap_matrix), axis=0),
    "mean_shap": np.mean(shap_matrix, axis=0)
})

shap_table = shap_table.sort_values(
    by="mean_abs_shap",
    ascending=False
).reset_index(drop=True)

shap_table.to_csv("data/shap_feature_table.csv", index=False)

shap_matrix = shap_values.values

shap_table = pd.DataFrame({
    "feature": X.columns,
    "mean_abs_shap": np.mean(np.abs(shap_matrix), axis=0),
    "direction": ["Positive" if x > 0 else "Negative" for x in np.mean(shap_matrix, axis=0)]
})

shap_table = shap_table.sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(shap_table)

shap.summary_plot(
    shap_values,
    X,
    max_display=16
)