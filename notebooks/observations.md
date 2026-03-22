# 📓 Phase 3 Observations, Python Analysis
## Housing Affordability Analysis (2015–2024)
**Author:** Yaw Assensoh Opoku
**Date:** 2026

---

##  EDA Observations (`01_eda.ipynb`)

### Data Quality
- 600 monthly observations across 5 cities, 100% complete after imputing 4 missing rent values
- Missing rent data: Miami (Jun–Jul 2021), New York (Aug–Sep 2020), gaps in ZORI source data
- All imputation used city monthly median to preserve seasonal patterns

### Distribution Findings
- Home values are **right-skewed**, LA pulls the mean far above the median
- Rent distributions are tighter than home values, rent is more compressed across cities
- Income standard deviation is only $3,505 over 10 years vs hundreds of thousands in home values

### Trend Findings
- Every city shows a clear upward trajectory, no city saw prices fall over the full period
- The steepest acceleration happened post-2020 across all 5 cities simultaneously
- Miami grew 120.2% from $222,470 (2015) to $489,833 (2024), fastest appreciation
- Los Angeles maintained the largest absolute gap from all other cities throughout

### Correlation Findings
- Strong positive correlation between home value and affordability index, rising prices are the primary driver
- Income growth barely correlates with home value change, wages did not keep pace
- Rent and home values are strongly correlated, expensive cities have expensive rents

### City Comparison (2015 vs 2024)
- Miami had the highest home value growth at 120.2%
- Los Angeles had the highest absolute deterioration in affordability
- Houston and Chicago remained the most stable markets throughout

---

##  Clustering Observations (`02_clustering.ipynb`)

### Model Selection
- Tested K = 2, 3, 4 (maximum K = n_samples - 1 = 4 with 5 cities)
- Optimal K determined by highest silhouette score
- Silhouette score measures how well each city fits its own cluster vs neighbouring clusters

### Cluster Assignments
- **Most Affordable**: Houston & Chicago, index consistently below 1.0
- **Moderate**: Miami, index crossing 1.0 post-2020, fastest deterioration
- **Least Affordable**: Los Angeles & New York, index above 1.0 throughout

### Key Clustering Insights
- Clusters align perfectly with SQL Phase 2 risk classifications, validating both analyses
- The radar chart reveals LA and NY dominate all stress metrics simultaneously
- Miami is the most volatile city, moderate on average but spiking on growth metrics
- Houston has the smallest radar footprint, most balanced and predictable market

---

##  Time Series Observations (`03_timeseries.ipynb`)

### Decomposition Findings
- All 5 cities show consistent 12-month seasonal patterns, prices peak every summer
- Strong upward trend component in all cities, no reversal detected
- Large residual spikes around 2020–2022 confirm COVID-19 introduced significant noise

### Stationarity Testing
- All 5 cities failed the ADF test on raw data, non-stationary due to upward trend
- All 5 cities passed after first differencing (d=1), confirming ARIMA parameter choice
- Modelling month-to-month changes rather than absolute prices resolves non-stationarity

### ARIMA Model Performance
- Auto ARIMA selected optimal parameters for each city independently
- All models use d=1, consistent with stationarity test findings
- Seasonal component (m=12) captures the consistent summer peak pattern

### Forecast Findings (2025–2027)
- All 5 cities forecast to see continued price growth, no reversal predicted
- Los Angeles approaching $1M+ by December 2027
- Miami shows the steepest forecast trajectory, consistent with post-2020 acceleration
- Houston and Chicago remain most affordable with narrowest confidence bands
- Confidence intervals widen over time, uncertainty increases the further we forecast

---

##  Regression Observations (`04_regression.ipynb`)

### Model Performance
- Multiple linear regression explains a strong portion of home value variance
- Minimal gap between training and testing R², no significant overfitting
- MAPE indicates the model predicts within a reasonable percentage of actual values

### Feature Importance
- City location (city_encoded) is among the top predictors, where a home is matters as much as economic fundamentals
- Affordability index and rent are strong predictors, the housing market is self-reinforcing
- Income alone is a weak predictor, wages have not driven price changes

### Residual Analysis
- Residuals centered near zero, model is unbiased
- Some deviation from normality at the tails, expected with housing data
- Actual vs predicted scatter shows good alignment across all price ranges

### Scenario Analysis
- A 10% income increase has a moderate effect on predicted home values
- A 15% rent increase shifts values more significantly, rent and home values are tightly linked
- Combined scenarios show compounding effects, multiple pressures simultaneously worsen affordability
- Structural supply constraints remain the dominant force beyond what the model captures

---

##  Geospatial Observations (`05_geospatial.ipynb`)

### Geographic Distribution
- Affordability crisis is geographically concentrated on the coasts, not a uniform national problem
- West Coast (LA) and Northeast (NY) are high risk, visible immediately on any map
- Midwest (Chicago) and South (Houston) show strong affordability despite being major metros
- Florida (Miami) is the transition zone, moving from affordable toward crisis territory

### Map Insights
- The interactive Folium map confirms visual separation between risk levels
- The choropleth makes a compelling policy case, city-specific solutions needed
- The bubble map reveals LA is both the most expensive AND most unaffordable simultaneously
- The time animation is the most powerful visual, watch Miami shift from green to amber in real time

### Key Geospatial Finding
Geography matters as much as economics in housing affordability. Two cities with similar incomes (Chicago and New York) have dramatically different affordability outcomes, driven by location, zoning, supply constraints, and migration patterns.

---

## 
 Overall Project Conclusions

### The 5 Key Findings Across All Phases

| Finding | Evidence |
|---------|---------|
| LA is in a housing crisis | Affordability index 2.22, only HIGH RISK city |
| COVID-19 was the inflection point | All cities deteriorated sharply 2020–2022 |
| Miami is the biggest warning sign | 120% growth, crossed threshold in 2022 |
| Houston is the counter-narrative | Affordable, stable, lowest risk throughout |
| Income growth is not the problem | Wages grew $11k over 10 years, prices grew $100k+ |

### What This Means for Policy
1. **Supply** is the primary lever, income policy alone cannot fix the crisis
2. **Coastal cities** need city-specific intervention, national policy won't work
3. **Miami** requires immediate attention, it is transitioning from affordable to unaffordable faster than any other market
4. **Houston's model** deserves study, lower zoning restrictions and land availability kept it affordable despite strong growth

### Technical Skills Demonstrated
- **Excel**: Data cleaning, VLOOKUP, PivotTables, affordability index calculation
- **SQL**: 10 queries using GROUP BY, window functions, LAG, RANK, CASE WHEN, JOINs
- **Python EDA**: Pandas, Matplotlib, Seaborn, distributions, trends, correlations
- **Clustering**: K-Means, elbow method, silhouette score, radar chart, 3D scatter
- **Time Series**: Decomposition, ADF stationarity test, SARIMA, 36-month forecasting
- **Regression**: Simple and multiple linear regression, feature importance, scenario analysis
- **Geospatial**: Folium interactive maps, Plotly choropleth, bubble map, time animation