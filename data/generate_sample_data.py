"""
=============================================================
  Generate Sample Dataset (World Bank Format)
  Use this if internet is not available in lab
  Data matches real World Bank figures for Pakistan
=============================================================
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = "."

# Real approximate World Bank figures for Pakistan
data = {
    "Year": list(range(2000, 2024)),
    "Country": ["Pakistan"] * 24,
    "CountryCode": ["PAK"] * 24,

    # GDP in USD (current)
    "GDP_USD": [
        7.29e10, 7.20e10, 7.24e10, 8.32e10, 9.73e10, 1.10e11,
        1.24e11, 1.47e11, 1.71e11, 1.68e11, 1.77e11, 2.14e11,
        2.24e11, 2.32e11, 2.43e11, 2.69e11, 2.78e11, 3.05e11,
        3.15e11, 2.78e11, 2.63e11, 3.47e11, 3.75e11, 3.38e11,
    ],

    # Inflation (%)
    "Inflation_Pct": [
        3.6, 4.4, 3.5, 3.1, 7.4, 9.1, 7.9, 7.6, 12.0, 17.0,
        10.1, 13.7, 11.0, 7.4, 8.6, 4.5, 2.8, 4.1, 3.9, 10.6,
        8.9, 9.5, 19.9, 29.2,
    ],

    # Population
    "Population": [
        1.38e8, 1.41e8, 1.44e8, 1.48e8, 1.51e8, 1.55e8,
        1.59e8, 1.63e8, 1.67e8, 1.71e8, 1.75e8, 1.79e8,
        1.83e8, 1.87e8, 1.91e8, 1.95e8, 1.99e8, 2.03e8,
        2.08e8, 2.12e8, 2.16e8, 2.20e8, 2.24e8, 2.28e8,
    ],

    # Exports % of GDP
    "Exports_PctGDP": [
        13.5, 14.1, 14.6, 16.3, 15.0, 14.2, 14.2, 14.5,
        13.2, 12.8, 13.4, 13.2, 12.2, 12.4, 11.4, 10.0,
        8.8, 8.6, 9.2, 9.0, 9.8, 10.1, 10.8, 9.2,
    ],

    # Imports % of GDP
    "Imports_PctGDP": [
        14.2, 14.8, 15.6, 18.1, 17.4, 17.8, 19.3, 21.5,
        24.0, 24.2, 19.8, 19.0, 17.9, 17.7, 17.2, 16.2,
        16.3, 17.7, 19.9, 17.8, 18.4, 20.1, 22.3, 18.8,
    ],

    # Literacy Rate (%)
    "Literacy_Rate": [
        43.9, None, None, None, None, 53.0, None, None, None,
        53.7, None, None, None, None, 56.4, None, None, None,
        59.1, None, None, 62.3, None, None,
    ],

    # Unemployment (%)
    "Unemployment_Pct": [
        7.8, 7.8, 8.3, 8.3, 7.7, 7.7, 6.2, 5.5, 5.1, 5.4,
        5.6, 6.0, 6.0, 6.2, 6.2, 5.9, 5.9, 5.8, 5.8, 6.9,
        6.9, 6.3, 6.3, 8.5,
    ],

    # Electricity KWh per capita
    "Electricity_KWh_PerCapita": [
        None, None, None, None, None, 394, 411, 445, 471, 463,
        461, 444, 444, 447, 451, 455, 462, 484, 487, 492,
        504, 511, 518, None,
    ],
}

df = pd.DataFrame(data)

# Fill missing literacy using interpolation
df["Literacy_Rate"] = df["Literacy_Rate"].interpolate(method="linear").round(1)
df["Electricity_KWh_PerCapita"] = df["Electricity_KWh_PerCapita"].interpolate(method="linear").round(0)

# Derived columns
df["GDP_BillionUSD"] = (df["GDP_USD"] / 1e9).round(2)
df["GDP_GrowthRate_Pct"] = df["GDP_USD"].pct_change() * 100
df["GDP_GrowthRate_Pct"] = df["GDP_GrowthRate_Pct"].round(2)
df["TradeBalance_PctGDP"] = (df["Exports_PctGDP"] - df["Imports_PctGDP"]).round(2)
df["Population_Millions"] = (df["Population"] / 1e6).round(2)
df["Decade"] = df["Year"].apply(lambda y: "2000s" if y < 2010 else ("2010s" if y < 2020 else "2020s"))

# Save main CSV
path = os.path.join(OUTPUT_DIR, "pakistan_economic_data.csv")
df.to_csv(path, index=False)
print(f"[✓] Main dataset: {path}")
print(f"    Shape: {df.shape}")
print(df.head())

# Decade averages
numeric_cols = ["GDP_BillionUSD", "GDP_GrowthRate_Pct", "Inflation_Pct",
                "Exports_PctGDP", "Imports_PctGDP", "TradeBalance_PctGDP",
                "Literacy_Rate", "Unemployment_Pct", "Electricity_KWh_PerCapita"]
decade_avg = df.groupby("Decade")[numeric_cols].mean().round(2)
decade_avg.to_csv(os.path.join(OUTPUT_DIR, "pakistan_decade_averages.csv"))
print(f"[✓] Decade averages saved")

# Summary stats
summary = df[numeric_cols].describe().T.round(2)
summary.to_csv(os.path.join(OUTPUT_DIR, "pakistan_summary_stats.csv"))
print(f"[✓] Summary stats saved")
print("\nAll 3 CSV files ready for Power BI!")
