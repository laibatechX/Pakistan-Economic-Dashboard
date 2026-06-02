"""
=============================================================
  Pakistan Economic Intelligence Dashboard
  Task-3: Data Fetching from World Bank API
  Course: Advanced Data Visualization (COMP-834)
  PAK-AUSTRIA FACHHOCHSCHULE
=============================================================

This script fetches LIVE data from the World Bank API:
  https://api.worldbank.org

No API key required — completely free and open.

Indicators fetched:
  - NY.GDP.MKTP.CD  : GDP (current US$)
  - FP.CPI.TOTL.ZG  : Inflation, consumer prices (annual %)
  - SP.POP.TOTL      : Population, total
  - NE.EXP.GNFS.ZS   : Exports of goods/services (% of GDP)
  - NE.IMP.GNFS.ZS   : Imports of goods/services (% of GDP)
  - SE.ADT.LITR.ZS   : Literacy rate, adult total (%)
  - SL.UEM.TOTL.ZS   : Unemployment, total (% of labor force)
  - EG.USE.ELEC.KH.PC: Electric power consumption (kWh per capita)
"""

import requests
import pandas as pd
import os

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------
COUNTRY = "PK"          # Pakistan ISO code
START_YEAR = 2000
END_YEAR   = 2023
OUTPUT_DIR = "."        # Save CSVs in current folder

INDICATORS = {
    "NY.GDP.MKTP.CD"  : "GDP_USD",
    "FP.CPI.TOTL.ZG"  : "Inflation_Pct",
    "SP.POP.TOTL"     : "Population",
    "NE.EXP.GNFS.ZS"  : "Exports_PctGDP",
    "NE.IMP.GNFS.ZS"  : "Imports_PctGDP",
    "SE.ADT.LITR.ZS"  : "Literacy_Rate",
    "SL.UEM.TOTL.ZS"  : "Unemployment_Pct",
    "EG.USE.ELEC.KH.PC": "Electricity_KWh_PerCapita",
}

BASE_URL = "https://api.worldbank.org/v2"

# ---------------------------------------------------------------
# HELPER: Fetch one indicator
# ---------------------------------------------------------------
def fetch_indicator(country, indicator, start, end):
    url = (
        f"{BASE_URL}/country/{country}/indicator/{indicator}"
        f"?format=json&date={start}:{end}&per_page=100"
    )
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    # World Bank returns [metadata, [records]]
    if len(data) < 2 or not data[1]:
        print(f"  WARNING: No data for {indicator}")
        return pd.DataFrame()

    records = data[1]
    rows = []
    for rec in records:
        rows.append({
            "Year"    : int(rec["date"]),
            "Value"   : rec["value"],
            "Country" : rec["country"]["value"],
            "CountryCode": rec["countryiso3code"],
        })

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["Value"])
    df = df.sort_values("Year")
    return df

# ---------------------------------------------------------------
# MAIN: Fetch all indicators and merge
# ---------------------------------------------------------------
def main():
    print("=" * 60)
    print("  Pakistan Economic Dashboard — World Bank Data Fetch")
    print("=" * 60)

    master_df = None

    for indicator_code, col_name in INDICATORS.items():
        print(f"\n[+] Fetching: {col_name} ({indicator_code})")
        try:
            df = fetch_indicator(COUNTRY, indicator_code, START_YEAR, END_YEAR)
            if df.empty:
                continue

            df = df.rename(columns={"Value": col_name})
            df = df[["Year", col_name]]

            if master_df is None:
                # First indicator — also keep Country column
                df_country = fetch_indicator(COUNTRY, indicator_code, START_YEAR, END_YEAR)
                df_country = df_country[["Year", "Country", "CountryCode"]]
                master_df = df_country.merge(df, on="Year", how="outer")
            else:
                master_df = master_df.merge(df, on="Year", how="outer")

            print(f"    Records: {len(df)}")
        except Exception as e:
            print(f"    ERROR: {e}")

    if master_df is None or master_df.empty:
        print("\nERROR: No data fetched. Check internet connection.")
        return

    # ---------------------------------------------------------------
    # DERIVED / CALCULATED COLUMNS  (for Power BI data modeling)
    # ---------------------------------------------------------------
    master_df = master_df.sort_values("Year").reset_index(drop=True)

    # GDP in Billions USD (easier to read in dashboards)
    if "GDP_USD" in master_df.columns:
        master_df["GDP_BillionUSD"] = (master_df["GDP_USD"] / 1e9).round(2)

    # GDP Growth Rate (year-over-year %)
    if "GDP_USD" in master_df.columns:
        master_df["GDP_GrowthRate_Pct"] = master_df["GDP_USD"].pct_change() * 100
        master_df["GDP_GrowthRate_Pct"] = master_df["GDP_GrowthRate_Pct"].round(2)

    # Trade Balance (Exports - Imports, % of GDP)
    if "Exports_PctGDP" in master_df.columns and "Imports_PctGDP" in master_df.columns:
        master_df["TradeBalance_PctGDP"] = (
            master_df["Exports_PctGDP"] - master_df["Imports_PctGDP"]
        ).round(2)

    # Population in Millions
    if "Population" in master_df.columns:
        master_df["Population_Millions"] = (master_df["Population"] / 1e6).round(2)

    # Decade category (for slicers in Power BI)
    master_df["Decade"] = master_df["Year"].apply(
        lambda y: "2000s" if y < 2010 else ("2010s" if y < 2020 else "2020s")
    )

    # ---------------------------------------------------------------
    # SAVE CSVs
    # ---------------------------------------------------------------
    main_path = os.path.join(OUTPUT_DIR, "pakistan_economic_data.csv")
    master_df.to_csv(main_path, index=False)
    print(f"\n[✓] Main dataset saved: {main_path}")
    print(f"    Shape: {master_df.shape}")
    print(f"    Columns: {list(master_df.columns)}")

    # Also save a summary stats CSV (for KPI cards in Power BI)
    numeric_cols = master_df.select_dtypes(include=["float64", "int64"]).columns
    summary = master_df[numeric_cols].describe().T
    summary.to_csv(os.path.join(OUTPUT_DIR, "pakistan_summary_stats.csv"))
    print(f"[✓] Summary stats saved: pakistan_summary_stats.csv")

    # Save decade-wise averages (for bar charts)
    decade_cols = [c for c in master_df.columns
                   if c not in ["Year", "Country", "CountryCode", "Decade", "GDP_USD", "Population"]]
    decade_avg = master_df.groupby("Decade")[decade_cols].mean().round(2)
    decade_avg.to_csv(os.path.join(OUTPUT_DIR, "pakistan_decade_averages.csv"))
    print(f"[✓] Decade averages saved: pakistan_decade_averages.csv")

    print("\n" + "=" * 60)
    print("  Data fetch complete! Load CSVs into Power BI.")
    print("=" * 60)
    print("\nPower BI Steps:")
    print("  1. Home → Get Data → Text/CSV")
    print("  2. Select: pakistan_economic_data.csv")
    print("  3. Repeat for pakistan_decade_averages.csv")
    print("  4. In Power Query: verify column types")
    print("     Year → Whole Number")
    print("     All numeric columns → Decimal Number")

if __name__ == "__main__":
    main()
