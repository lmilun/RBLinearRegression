import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt


model = joblib.load('data/xgb_best_model_after_9000.pkl')

df = pd.read_csv('data/statsByYear.csv')
df = df.drop(columns=['playerID', 'Player'])
df = df.drop(df.columns[0], axis=1)

target = 'nextYpT'
X = df.drop(columns=[target])
Y = df[target]

explainer = shap.Explainer(model, X)

shap_values = explainer(X)

plt.title("SHAP Summary Plot for XGBoost Model")
shap.summary_plot(shap_values, X, max_display=28)

shap.summary_plot(shap_values, X, plot_type="bar", max_display = 28)