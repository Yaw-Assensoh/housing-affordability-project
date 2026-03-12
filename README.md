#  Housing Affordability & Market Crisis Analysis

A three-phase data analytics project examining the US housing affordability 
crisis across 5 major metro areas — New York, Los Angeles, Chicago, 
Houston, and Miami — covering 2015 to 2024.

---

##  Project Structure
```
├── data/raw/          # Original downloaded datasets (Zillow, FRED)
├── data/cleaned/      # Cleaned and transformed data
├── excel/             # Phase 1 Excel dashboard
├── sql/               # Phase 2 PostgreSQL queries
├── notebooks/         # Phase 3 Python Jupyter notebooks
```

---

##  Phase 1 — Excel Dashboard

**Core question:** How have home prices and affordability changed 
across major US cities over the past decade?

**Affordability Index formula:**
> Index = Median Home Price ÷ (Annual Median Income × 5)
- Score = 1.0 → perfectly affordable
- Score = 1.5 → 50% overpriced relative to income  
- Score = 2.0+ → severely unaffordable

**Key findings:**
- Los Angeles reached an affordability index of 2.1+ by 2024 — 
  more than double the affordable threshold
- Miami showed the sharpest deterioration post-2020, driven by 
  the COVID-era migration boom into Florida
- Houston remained below 1.5 throughout — the only city to stay 
  near the affordable range for the full period

**Tools:** Microsoft Excel — data cleaning, long-format reshaping, 
VLOOKUP, PivotTables, line charts

**Data sources:**
- [Zillow Research](https://www.zillow.com/research/data/) — ZHVI & ZORI
- [FRED](https://fred.stlouisfed.org) — Median Household Income (MEHOINUSA672N)

---

##  Phase 2 — SQL Market Intelligence

PostgreSQL analysis to identify supply/demand imbalances 
and rank markets by risk and opportunity.

**Tools:** PostgreSQL

---

##  Phase 3 — Python Predictive Model

Regression model using Python (Pandas, Scikit-learn) to forecast 
home prices and identify key economic drivers.

**Tools:** Python, Jupyter Notebook, Pandas, Scikit-learn, Seaborn

---

##  Data Sources

| Dataset | Source | Used In |
|---|---|---|
| ZHVI — Home Values | Zillow Research | Phase 1, 2 |
| ZORI — Rents | Zillow Research | Phase 1 |
| Median Household Income | FRED | Phase 1, 3 |
| Realtor.com Inventory | Realtor.com | Phase 2 |
```



##  Phase 2 — SQL Market Intelligence

**Core question:** Which markets show the most risk and how has
affordability changed year over year?

**Key findings:**
- 🔴 Los Angeles is the only HIGH RISK market — avg index 1.745,
  peaked at 2.279 in 2022. Rent consumes 40% of median income.
- 🟡 New York is MODERATE RISK — rent hit 44% of income in 2024,
  the highest of all 5 cities
- 📈 Miami had the fastest home value growth at 120% since 2015,
  crossing the affordability threshold for the first time in 2022
- 🟢 Houston is the most resilient — lowest growth rate (67%),
  rent stayed near 23% of income throughout
- 📉 2021–2022 were the worst years across all cities —
  LA deteriorated 0.302 index points in a single year

**SQL concepts used:** GROUP BY, AVG, ROUND, RANK, LAG,
CASE WHEN, UNION ALL, subqueries, JOINS, DISTINCT ON,
window functions (PARTITION BY, FIRST_VALUE)

**Tools:** PostgreSQL 14, pgAdmin 4

**Query files:** [`sql/03_analysis_queries.sql`](sql/03_analysis_queries.sql)