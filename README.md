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
  peaked at 2.279 in 2022
- 🟡 New York is MODERATE RISK — crossed 1.5 in 2022 
  and hasn't recovered
- 📈 Miami shows the fastest deterioration — index nearly 
  doubled 2015–2024 despite LOW RISK average rating
- 🟢 Houston & Chicago remain LOW RISK throughout — 
  never crossed 1.0

**SQL concepts used:** GROUP BY, AVG, ROUND, RANK, 
LAG (window functions), CASE WHEN, UNION ALL, subqueries

**Tools:** PostgreSQL 14, pgAdmin 4