# Pakistan-Economic-Dashboard
# 🇵🇰 Pakistan Economic Intelligence Dashboard
### Interactive Power BI Dashboard + ARIMA Forecasting System

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![World Bank](https://img.shields.io/badge/World%20Bank%20API-003087?style=for-the-badge&logo=worldbank&logoColor=white)
![ML](https://img.shields.io/badge/ARIMA-FF6B6B?style=for-the-badge&logo=scikitlearn&logoColor=white)

---

## 📌 Project Overview

A **two-part Business Intelligence system** built on real World Bank economic data for Pakistan (2000–2023):

**Key Achievement:** ARIMA model forecasts Pakistan's GDP, Inflation, and Population through 2028 — achieving **99.9% accuracy** on Population and **88.4% accuracy** on GDP.

---

## 🗂️ Repository Structure

```
Pakistan-Economic-Dashboard/
│
├── 📊 data/
│   ├── pakistan_economic_data.csv       # Main dataset (24 years × 16 indicators)
│   ├── pakistan_decade_averages.csv     # Decade-wise aggregated data
│   ├── pakistan_summary_stats.csv       # Descriptive statistics
│   ├── forecast_results.csv             # ARIMA actual + forecast values
│   ├── forecast_pivot.csv               # Wide-format forecast for Power BI
│   └── model_evaluation.csv             # MAE, RMSE, R², MAPE metrics
│
├── 🐍 scripts/
│   ├── STEP1_setup_and_run.py           # Master script: fetch data + run ARIMA
│   ├── fetch_worldbank_data.py          # Live World Bank API fetch
│   ├── generate_sample_data.py          # Offline data generator
│   └── task4_arima_forecast.py          # ARIMA(1,1,0) ML model
│
├── 📈 visuals/
│   └── forecast_charts.png              # ARIMA forecast visualization (3 indicators)
│
├── 📄 report/
│   └── Pakistan_Economic_Dashboard_Report.docx   # Full technical report
│
└── README.md
```

---

## 📊 Data Source

**World Bank Open Data API** — completely free, no API key required

```
https://api.worldbank.org/v2/country/PK/indicator/{INDICATOR}?format=json&date=2000:2023
```

| Indicator | Code | Column |
|-----------|------|--------|
| GDP (current US$) | `NY.GDP.MKTP.CD` | `GDP_BillionUSD` |
| Inflation (annual %) | `FP.CPI.TOTL.ZG` | `Inflation_Pct` |
| Population, total | `SP.POP.TOTL` | `Population_Millions` |
| Exports (% of GDP) | `NE.EXP.GNFS.ZS` | `Exports_PctGDP` |
| Imports (% of GDP) | `NE.IMP.GNFS.ZS` | `Imports_PctGDP` |
| Literacy rate (%) | `SE.ADT.LITR.ZS` | `Literacy_Rate` |
| Unemployment (%) | `SL.UEM.TOTL.ZS` | `Unemployment_Pct` |

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+   # python --version
Power BI Desktop (free from Microsoft Store)
```

### Step 1 — Run Setup Script
```bash
git clone https://github.com/YOUR_USERNAME/Pakistan-Economic-Dashboard.git
cd Pakistan-Economic-Dashboard
python scripts/STEP1_setup_and_run.py
```
This will:
- ✅ Install required Python packages automatically
- ✅ Fetch live data from World Bank API (or use embedded fallback)
- ✅ Run ARIMA(1,1,0) forecasting model
- ✅ Generate all CSV files + forecast charts

### Step 2 — Open Power BI
```
1. Open Power BI Desktop
2. Home → Get Data → Text/CSV
3. Load: data/pakistan_economic_data.csv
4. Load: data/forecast_pivot.csv
5. Load: data/model_evaluation.csv
6. Build dashboard following /report/ guide
```

---

## 🤖 Machine Learning — ARIMA(1,1,0)

### Why ARIMA?
Pakistan's economic indicators are **non-stationary time series** with consistent trends. ARIMA handles this via differencing, making it ideal for annual economic data.

### Model Configuration
| Parameter | Value | Meaning |
|-----------|-------|---------|
| **p = 1** | 1 AR term | Current value depends on previous year |
| **d = 1** | 1st-order differencing | Removes non-stationarity / trend |
| **q = 0** | No MA term | Keeps model simple for 24 data points |

### Training Setup
```python
Train set:  2000–2019  (20 years = 83%)
Test set:   2020–2023  (4 years  = 17%)
Forecast:   2024–2028  (5-year projection)
```

### Model Evaluation Results

| Indicator | MAE | RMSE | R² Score | MAPE | Accuracy |
|-----------|-----|------|----------|------|----------|
| GDP (Billion USD) | 39.35 | 43.77 | -0.116 | 11.58% | **88.42%** |
| Inflation (%) | 7.25 | 10.32 | -0.528 | 30.91% | 69.09% |
| Population (Millions) | 0.23 | 0.26 | 0.9966 | 0.10% | **99.90%** |

### 5-Year Forecast (2024–2028)

| Year | GDP (B USD) | Inflation (%) | Population (M) |
|------|------------|----------------|----------------|
| 2024 | 350.6 | 24.1 | 232 |
| 2025 | 362.1 | 22.8 | 236 |
| 2026 | 373.6 | 21.5 | 240 |
| 2027 | 385.1 | 20.2 | 244 |
| 2028 | 396.6 | 18.9 | 248 |

---

## 📈 Dashboard Features

### Task-3: Interactive Dashboard
- **5 KPI Cards** — GDP, Inflation, Population, Trade Deficit, Literacy
- **Line Chart** — GDP & Inflation trend 2000–2023 (dual axis)
- **Bar Chart** — Decade-wise economic comparison
- **Pie Chart** — GDP distribution across decades
- **Data Table** — Full raw structured data
- **Area Chart** — Exports vs Imports trade balance
- **2 Slicers** — Decade dropdown + Year range filter
- **Cross-filtering** — Click any visual to filter all others

### Task-4: Forecasting Dashboard
- **Actual vs Predicted Line Chart** — Real data vs ARIMA forecast
- **Error Analysis Table** — MAE / RMSE / R² / MAPE
- **KPI Cards** — Model accuracy + 2028 projections
- **Forecast Image** — Python-generated ARIMA visualization
- **Type Slicer** — Toggle between Actual / Forecast view

---

## 🔑 Key Findings

- 📈 Pakistan's GDP grew **5x** from USD 73B (2000) to USD 375B (2022)
- 💰 Inflation peaked at **29.2%** in 2023 — highest in 24 years
- 📉 Pakistan maintained a **trade deficit every single year** 2000–2023
- 📚 Literacy improved from **43.9% → 63.9%** over two decades
- 🔮 ARIMA forecasts GDP reaching **USD 396B by 2028** (+17% from 2023)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Power BI Desktop** | Interactive dashboard & visualization |
| **Python 3.x** | Data processing & ML modeling |
| **pandas / numpy** | Data manipulation |
| **matplotlib** | Forecast visualization |
| **scikit-learn** | Linear regression (AR coefficient estimation) |
| **World Bank API** | Live economic data source |

---

## 📁 Files for Submission

```
✅ Task3_Pakistan_Dashboard.pbix          (Power BI — Task 3)
✅ Task4_Pakistan_ARIMAForecast.pbix      (Power BI — Task 4)
✅ Pakistan_Economic_Dashboard_Report.docx (Technical Report)
✅ scripts/STEP1_setup_and_run.py         (Python script)
✅ data/*.csv                              (All datasets)
```

---

## 👩‍💻 Author

Laiba Azha  
MS Artificial Intelligence — PAK-AUSTRIA Fachhochschule  
📧 laibaazhar.ds@gmail.com
🔗 https://www.linkedin.com/in/laiba-azhar-b89449263/

---

## 📜 License

This project is for academic purposes.  
Data sourced from [World Bank Open Data](https://data.worldbank.org) under Creative Commons Attribution 4.0.

---

*Built with ❤️ using Python + Power BI | Spring 2026*
