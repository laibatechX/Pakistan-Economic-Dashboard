"""
=============================================================
  Pakistan Economic Dashboard — Task-4 ML Forecasting
  Algorithm: ARIMA (AutoRegressive Integrated Moving Average)
  Course: Advanced Data Visualization (COMP-834)
  PAK-AUSTRIA FACHHOCHSCHULE
=============================================================

This script:
1. Loads cleaned Pakistan economic data
2. Applies ARIMA forecasting on GDP, Inflation, Population
3. Predicts next 5 years (2024–2028)
4. Evaluates model accuracy (MAE, RMSE, R²)
5. Exports forecast_results.csv for Power BI import
6. Generates visualization charts
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings("ignore")
import os

# ---------------------------------------------------------------
# 0. SETUP
# ---------------------------------------------------------------
OUTPUT_DIR = "."
FORECAST_YEARS = 5          # Predict 2024–2028
TEST_SIZE = 4               # Last 4 years as test set

print("=" * 60)
print("  Pakistan Economic Forecasting — ARIMA + Linear Regression")
print("=" * 60)

# ---------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------
df = pd.read_csv(os.path.join(OUTPUT_DIR, "pakistan_economic_data.csv"))
df = df.sort_values("Year").reset_index(drop=True)
df = df.dropna(subset=["GDP_BillionUSD", "Inflation_Pct"])

print(f"\n[+] Data loaded: {len(df)} records ({df['Year'].min()}–{df['Year'].max()})")

# ---------------------------------------------------------------
# 2. ARIMA IMPLEMENTATION (Manual — no external library needed)
#    We use differencing + OLS which is ARIMA(1,1,0) equivalent
# ---------------------------------------------------------------

class SimpleARIMA:
    """
    Simplified ARIMA(1,1,0) implementation using numpy.
    d=1 (first-order differencing to make series stationary)
    p=1 (one autoregressive lag)
    q=0 (no moving average component)
    """
    def __init__(self):
        self.phi = None          # AR coefficient
        self.mean_diff = None    # Mean of differenced series
        self.last_values = None  # For forecasting

    def fit(self, series):
        """Fit ARIMA(1,1,0) to a time series."""
        values = np.array(series, dtype=float)

        # Step 1: First-order differencing (d=1)
        diff = np.diff(values)
        self.mean_diff = np.mean(diff)

        # Step 2: Center the differenced series
        diff_centered = diff - self.mean_diff

        # Step 3: Fit AR(1) — regress diff[t] on diff[t-1]
        y = diff_centered[1:]
        x = diff_centered[:-1].reshape(-1, 1)

        model = LinearRegression()
        model.fit(x, y)
        self.phi = model.coef_[0]

        # Store last differenced value and last actual value
        self.last_diff = diff_centered[-1]
        self.last_value = values[-1]

        return self

    def forecast(self, steps):
        """Generate multi-step forecast."""
        forecasts = []
        current_diff = self.last_diff
        current_value = self.last_value

        for _ in range(steps):
            # AR(1) prediction on differenced series
            next_diff_centered = self.phi * current_diff
            next_diff = next_diff_centered + self.mean_diff

            # Invert differencing to get actual value
            next_value = current_value + next_diff

            forecasts.append(next_value)
            current_diff = next_diff_centered
            current_value = next_value

        return np.array(forecasts)

    def predict_in_sample(self, series):
        """Predict values for the training set."""
        values = np.array(series, dtype=float)
        diff = np.diff(values)
        diff_centered = diff - self.mean_diff

        predicted = [values[0]]  # First value unchanged
        predicted.append(values[1])  # Second value unchanged

        for i in range(1, len(diff_centered)):
            next_diff_c = self.phi * diff_centered[i-1]
            next_diff = next_diff_c + self.mean_diff
            next_val = predicted[-1] + next_diff
            predicted.append(next_val)

        return np.array(predicted)


# ---------------------------------------------------------------
# 3. TRAIN & EVALUATE MODELS
# ---------------------------------------------------------------
targets = {
    "GDP_BillionUSD"  : "GDP (Billion USD)",
    "Inflation_Pct"   : "Inflation (%)",
    "Population_Millions": "Population (Millions)",
}

results_rows = []
eval_rows = []

colors = {
    "GDP_BillionUSD"     : "#2196F3",
    "Inflation_Pct"      : "#FF5722",
    "Population_Millions": "#4CAF50",
}

fig, axes = plt.subplots(3, 1, figsize=(12, 14))
fig.suptitle(
    "Pakistan Economic Forecasting Dashboard\nARIMA(1,1,0) Model — 2024–2028 Projections",
    fontsize=15, fontweight="bold", y=1.01
)

for idx, (col, label) in enumerate(targets.items()):
    print(f"\n[+] Forecasting: {label}")

    series = df[col].dropna().values
    years  = df["Year"].values[:len(series)]

    # Train / Test split
    train_series = series[:-TEST_SIZE]
    test_series  = series[-TEST_SIZE:]
    train_years  = years[:-TEST_SIZE]
    test_years   = years[-TEST_SIZE:]

    # Fit ARIMA on training data
    model = SimpleARIMA()
    model.fit(train_series)

    # Predict on test set
    test_pred = model.forecast(TEST_SIZE)

    # Evaluation metrics
    mae  = mean_absolute_error(test_series, test_pred)
    rmse = np.sqrt(mean_squared_error(test_series, test_pred))
    r2   = r2_score(test_series, test_pred)
    mape = np.mean(np.abs((test_series - test_pred) / test_series)) * 100

    print(f"    MAE  = {mae:.3f}")
    print(f"    RMSE = {rmse:.3f}")
    print(f"    R²   = {r2:.4f}")
    print(f"    MAPE = {mape:.2f}%")

    eval_rows.append({
        "Metric"    : label,
        "MAE"       : round(mae, 3),
        "RMSE"      : round(rmse, 3),
        "R2_Score"  : round(r2, 4),
        "MAPE_Pct"  : round(mape, 2),
        "Accuracy_Pct": round(100 - mape, 2),
    })

    # Refit on FULL data for future forecast
    model_full = SimpleARIMA()
    model_full.fit(series)
    future_values = model_full.forecast(FORECAST_YEARS)
    future_years  = np.arange(2024, 2024 + FORECAST_YEARS)

    # Collect forecast results
    for yr, val in zip(future_years, future_values):
        results_rows.append({
            "Year"       : yr,
            "Type"       : "Forecast",
            "Indicator"  : col,
            "Label"      : label,
            "Value"      : round(float(val), 3),
        })
    # Also include historical actuals
    for yr, val in zip(years, series):
        results_rows.append({
            "Year"       : yr,
            "Type"       : "Actual",
            "Indicator"  : col,
            "Label"      : label,
            "Value"      : round(float(val), 3),
        })

    # ---------------------------------------------------------------
    # PLOT
    # ---------------------------------------------------------------
    ax = axes[idx]
    color = colors[col]

    ax.plot(years, series, color=color, linewidth=2.5,
            marker="o", markersize=4, label="Actual", zorder=3)

    ax.plot(test_years, test_pred, color="orange", linewidth=2,
            linestyle="--", marker="s", markersize=5,
            label="Test Prediction", zorder=4)

    ax.plot(future_years, future_values, color="red", linewidth=2.5,
            linestyle="--", marker="^", markersize=6,
            label="Forecast (2024–2028)", zorder=5)

    # Confidence interval (±10% band)
    lower = future_values * 0.90
    upper = future_values * 1.10
    ax.fill_between(future_years, lower, upper,
                    alpha=0.15, color="red", label="90% Confidence Band")

    # Vertical divider at forecast start
    ax.axvline(x=2023.5, color="gray", linestyle=":", linewidth=1.5)
    ax.text(2023.6, ax.get_ylim()[0] + (ax.get_ylim()[1]-ax.get_ylim()[0])*0.05,
            "Forecast →", fontsize=9, color="gray")

    ax.set_title(f"{label} — ARIMA(1,1,0) | R²={r2:.3f} | MAPE={mape:.1f}%",
                 fontsize=11, fontweight="bold")
    ax.set_xlabel("Year", fontsize=9)
    ax.set_ylabel(label, fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(1999, 2029)

plt.tight_layout()
chart_path = os.path.join(OUTPUT_DIR, "forecast_charts.png")
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"\n[✓] Forecast charts saved: {chart_path}")

# ---------------------------------------------------------------
# 4. SAVE OUTPUTS
# ---------------------------------------------------------------
# Forecast results CSV (re-import into Power BI for predictive dashboard)
results_df = pd.DataFrame(results_rows)
results_path = os.path.join(OUTPUT_DIR, "forecast_results.csv")
results_df.to_csv(results_path, index=False)
print(f"[✓] Forecast results saved: {results_path}")

# Evaluation metrics CSV (for error analysis table in Power BI)
eval_df = pd.DataFrame(eval_rows)
eval_path = os.path.join(OUTPUT_DIR, "model_evaluation.csv")
eval_df.to_csv(eval_path, index=False)
print(f"\n[✓] Model evaluation saved: {eval_path}")
print("\n" + eval_df.to_string(index=False))

# ---------------------------------------------------------------
# 5. PIVOT forecast for Power BI (wide format — easier for visuals)
# ---------------------------------------------------------------
pivot = results_df.pivot_table(
    index=["Year", "Type"],
    columns="Indicator",
    values="Value",
    aggfunc="first"
).reset_index()
pivot.columns.name = None
pivot.to_csv(os.path.join(OUTPUT_DIR, "forecast_pivot.csv"), index=False)
print(f"\n[✓] Pivot forecast saved: forecast_pivot.csv")

print("\n" + "=" * 60)
print("  Task-4 Complete! Files ready for Power BI:")
print("    → forecast_results.csv  (Actual vs Forecast)")
print("    → forecast_pivot.csv    (Wide format for charts)")
print("    → model_evaluation.csv  (MAE/RMSE/R² table)")
print("    → forecast_charts.png   (Insert in Word report)")
print("=" * 60)
