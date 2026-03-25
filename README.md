# 🏠 US Housing Affordability Analysis (2015–2024)

A comprehensive 3-phase data analytics portfolio project examining the US housing
affordability crisis across 5 major cities — New York, Los Angeles, Chicago,
Houston, and Miami — using Excel, SQL, Python, and an interactive Streamlit dashboard.

> **Core Question:** Why are some cities becoming unaffordable while others remain stable?

---

##  Key Findings

| Finding | Insight |
|---------|---------|
| 🔴 **The Crisis** | Los Angeles (index 2.22) and New York (1.58) have been unaffordable since before 2015. A household needs $200K+ annual income to afford a median LA home. |
| 🟡 **The Warning Sign** | Miami crossed the affordability threshold for the first time in 2022 — 120% home value growth since 2015, the fastest in the dataset. |
| 🟢 **The Counter-Narrative** | Chicago and Houston stayed below 1.0 throughout the entire 10-year period. Major metros CAN remain affordable with the right land use policies. |
|  **The Inflection Point** | COVID-19 (2020–2022) caused the sharpest simultaneous deterioration across all 5 cities. LA's index jumped 0.302 points in 2022 alone. |
|  **Supply, Not Income** | Median income grew $11K over 10 years. LA home values grew $400K. Regression confirms: income subsidies alone cannot solve a structural supply problem. |

## 📈 2024 Market Snapshot

| City | Home Value | Monthly Rent | Affordability Index | 10-Year Growth | Risk Level |
|------|------------|--------------|---------------------|----------------|------------|
| Los Angeles | $1,058,000 | $3,800 | 2.22 | +95.7% | 🔴 HIGH |
| New York | $761,000 | $3,500 | 1.53 | +66.2% | 🔴 HIGH |
| Miami | $524,000 | $2,400 | 1.32 | +108.2% | 🟡 MODERATE |
| Chicago | $289,000 | $1,600 | 0.74 | +36.3% | 🟢 LOW |
| Houston | $271,000 | $1,500 | 0.69 | +46.2% | 🟢 LOW |

*The affordability index measures home price relative to income. Score = 1.0 is the threshold — anything above means housing costs more than a household earning the median income can comfortably afford.*
---

## 🗂️ Project Structure
```
housing-affordability-project/
├── data/
│   ├── raw/                        # Original Zillow & FRED downloads (gitignored)
│   └── cleaned/                    # Processed CSVs used by notebooks & dashboard
│       ├── cities_long.csv
│       ├── annual_summary.csv
│       ├── clustering_results.csv
│       ├── forecasts_2025_2027.csv
│       ├── arima_model_summary.csv
│       ├── regression_predictions.csv
│       ├── regression_feature_importance.csv
│       └── regression_scenarios.csv
├── excel/
│   ├── housing_affordability_dashboard.xlsx
│   └── findings.md
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_load_data.sql
│   ├── 03_analysis_queries.sql
│   └── findings.md
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_clustering.ipynb
│   ├── 03_timeseries.ipynb
│   ├── 04_regression.ipynb
│   ├── 05_geospatial.ipynb
│   └── observations.md
├── dashboard/
│   ├── Dashboard.py
│   ├── pages/
│   │   ├── 1_EDA.py
│   │   ├── 2_Clustering.py
│   │   ├── 3_Time_Series.py
│   │   ├── 4_Regression.py
│   │   └── 5_Geospatial.py
│   └── requirements.txt
├── assets/                         # Chart PNGs and HTML maps
├── requirements.txt
└── README.md
```

---

##  Phase 1 — Excel Dashboard

**Tool:** Microsoft Excel

**Core question:** How have home prices and affordability changed across major US cities over the past decade?

### Affordability Index Formula
```
Index = Median Home Price ÷ (Annual Median Income × 5)
```

| Score | Meaning |
|-------|---------|
| ≤ 1.0 | Affordable — within reach for median income households |
| 1.0–1.5 | Moderate risk — stretched but manageable |
| > 1.5 | HIGH RISK — severely unaffordable |

### Key Findings
- Los Angeles reached 2.22 by 2024 — more than double the affordable threshold
- Miami showed the sharpest post-2020 deterioration, driven by COVID-era migration
- Houston remained below 1.0 throughout — the only city to stay affordable for the full period
- National median income grew just $11,000 over 10 years while home values grew $400,000+

### Techniques Used
Data cleaning, long-format reshaping, VLOOKUP, PivotTables, line charts, KPI cards

### Data Sources
- [Zillow Research](https://www.zillow.com/research/data/) — ZHVI (home values) & ZORI (rents)
- [FRED](https://fred.stlouisfed.org) — Median Household Income (MEHOINUSA672N)

---

##  Phase 2 — SQL Market Intelligence

**Tool:** PostgreSQL 14, pgAdmin 4

**Core question:** Which markets show the most risk and how has affordability changed year over year?

### 10 Analytical Queries

| # | Query | Purpose |
|---|-------|---------|
| 1 | Avg home value per city | Baseline price comparison |
| 2 | Avg affordability index | Overall risk ranking |
| 3 | Affordability trend by year | Track deterioration over time |
| 4 | Most expensive city per year | `FIRST_VALUE` window function |
| 5 | City rankings per year | `RANK` with `PARTITION BY` |
| 6 | Year-over-year change | `LAG` function |
| 7 | Market risk classification | `CASE WHEN` (HIGH / MODERATE / LOW) |
| 8 | Rent-to-income ratio | Affordability stress metric |
| 9 | Home value growth 2015 vs 2024 | `JOIN` subqueries |
| 10 | First year each city crossed 1.0 | `DISTINCT ON` |

### Key Findings
- 🔴 **Los Angeles** — only HIGH RISK market. Avg index 1.745, peaked at 2.279 in 2022. Rent consumes 40% of median income
- 🟡 **New York** — MODERATE RISK. Rent hit 44% of income in 2024, highest of all 5 cities
- 📈 **Miami** — fastest home value growth at 120% since 2015, crossed threshold in 2022
- 🟢 **Houston** — most resilient. Rent stayed near 23% of income throughout, lowest risk
- 📉 **2021–2022** — worst years across all cities. LA deteriorated 0.302 index points in a single year

### SQL Concepts Used
`GROUP BY` · `AVG` · `ROUND` · `RANK` · `LAG` · `CASE WHEN` · `UNION ALL` · subqueries · `JOIN` · `DISTINCT ON` · window functions (`PARTITION BY`, `FIRST_VALUE`)

---

## 🐍 Phase 3 — Python Advanced Analytics

**Tools:** Python 3.9+, Jupyter Notebook

### 5 Notebooks

#### `01_eda.ipynb` — Exploratory Data Analysis
- Distribution analysis across all 5 cities
- 10-year trend visualisation
- Correlation heatmap
- City comparison 2015 vs 2024

**Libraries:** Pandas, Matplotlib, Seaborn, Plotly

---

#### `02_clustering.ipynb` — K-Means Market Segmentation

Unsupervised machine learning to group cities into natural market segments without prior knowledge of risk levels.

| Cluster | Cities | Avg Index |
|---------|--------|-----------|
| 🟢 Most Affordable | Houston, Chicago | < 1.0 |
| 🟡 Moderate | Miami | ~1.17 |
| 🔴 Least Affordable | Los Angeles, New York | > 1.5 |

> **Key Validation:** K-Means identified the same risk groups as SQL without using any thresholds — two completely different methods (supervised SQL logic vs unsupervised machine learning) reaching identical conclusions. This confirms the findings are robust, not artefacts of methodology.

**Libraries:** Scikit-learn, Plotly

**Techniques:** K-Means, elbow method, silhouette score, radar chart, 3D scatter

#### `03_timeseries.ipynb` — SARIMA Forecasting

Time series decomposition and 36-month forecasting through December 2027.

- All 5 cities tested for stationarity using ADF test — all required d=1 differencing
- Seasonal ARIMA (SARIMA) with m=12 to capture annual price cycles
- 95% confidence intervals generated for all forecasts

| City | 2027 Forecast | vs 2024 |
|------|--------------|---------|
| Los Angeles | $990,000 | -6.4% |
| New York | $813,000 | +6.8% |
| Miami | $629,000 | +20.0% |
| Chicago | $326,000 | +12.8% |
| Houston | $308,000 | +13.6% |

*SARIMA models trained on 10 years of monthly data, generating 36-month forecasts with 95% confidence intervals.*

**Libraries:** Statsmodels, pmdarima, Plotly

---

#### `04_regression.ipynb` — Multiple Linear Regression

7-feature regression model identifying economic drivers of home values.

| Feature | Role |
|---------|------|
| median_income | Economic baseline |
| monthly_rent | Market pressure |
| affordability_index | Existing stress |
| rent_to_income | Affordability burden |
| year | Temporal trend |
| month | Seasonal cycle |
| city_encoded | Location effect |

**Scenario Analysis (Los Angeles 2024):** Modelled the effect of +10% income, +15% rent, and combined shocks. Result: income changes have minimal effect on prices — confirming supply constraints as the dominant force.

**Libraries:** Scikit-learn, Statsmodels, Plotly

---

#### `05_geospatial.ipynb` — Interactive Maps

Four map types visualising the geographic concentration of the affordability crisis.

| Map | Type | Key Insight |
|-----|------|-------------|
| Interactive Folium | Click markers for full metrics | Coastal concentration visible immediately |
| Choropleth | State-level affordability colour | Green Midwest vs Red coasts |
| Bubble Map | Size = price, Colour = risk | LA largest AND reddest bubble |
| Time Animation | Play 2015–2024 | Watch Miami shift from green to amber in real time |

**Libraries:** Folium, Plotly Express

---

## 📱 Streamlit Dashboard

**Live App:** [https://yaw-assensoh-housing-affordability-pr-dashboarddashboard-0wtwto.streamlit.app]

### Pages

| Page | Content |
|------|---------|
| 🏠 Dashboard | Executive summary, KPI cards, risk table, 10-year trend chart, key findings |
| 📊 EDA | Filters, trend tabs, distribution explorer, correlation heatmap |
| 🔵 Clustering | Cluster cards, scatter plot, radar chart, feature comparison |
| 📈 Time Series | 2027 forecasts, city selector, confidence intervals, ARIMA parameters |
| 📐 Regression | Model metrics, feature importance, actual vs predicted, scenario analysis |
| 🗺️ Geospatial | 4 map types, metrics table, geographic findings |

---

## 🚀 How to Run Locally

### Prerequisites
```bash
Python 3.9+
PostgreSQL 14 (for Phase 2 only)
```

### Setup
```bash
# Clone the repository
git clone https://github.com/Yaw-Assensoh/Housing-Affordability-Analysis.git
cd Housing-Affordability-Analysis

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows

# Install dependencies
pip install -r requirements.txt
```


##  Requirements
```
streamlit
pandas
plotly
folium
numpy
scikit-learn
statsmodels
pmdarima
matplotlib
seaborn
psycopg2-binary
openpyxl
jupyter
```

---

##  Data Sources

| Dataset | Source | Used In |
|---------|--------|---------|
| ZHVI — Median Home Values | [Zillow Research](https://www.zillow.com/research/data/) | Phase 1, 2, 3 |
| ZORI — Monthly Rents | [Zillow Research](https://www.zillow.com/research/data/) | Phase 1, 2, 3 |
| Median Household Income | [FRED — MEHOINUSA672N](https://fred.stlouisfed.org/series/MEHOINUSA672N) | Phase 1, 2, 3 |

---

## 👤 Author

**Yaw Assensoh Opoku**
Data Analyst · Excel · SQL · Python · Streamlit

[GitHub](https://github.com/Yaw-Assensoh) · [LinkedIn](https://www.linkedin.com/in/yaw-assensoh-opoku/)

---

##  License

This project is open source and available under the [MIT License](LICENSE).