# Phase 2 Findings — SQL Market Intelligence

## What I Analysed
10 SQL queries across 3 database tables covering 600 months of 
housing data for 5 US cities (2015–2024).

## Key Metrics Used
- **Affordability Index** = Home Price ÷ (Income × 5) — threshold 1.0
- **Rent to Income %** = (Monthly Rent × 12) ÷ Annual Income — threshold 30%
- **YoY Change** = Current year index minus previous year (LAG function)
- **Risk Level** = CASE WHEN classification based on avg affordability index

## The 10 Key Findings

### 1. Los Angeles — Chronically High Risk
Avg affordability index of 1.745 — the only HIGH RISK city.
Peaked at 2.279 in 2022. Rent consumes 40% of median income.
Has been above the 1.0 threshold since before 2015.

### 2. New York — Moderate Risk, Worsening
Crossed 1.5 in 2022 and hasn't recovered. Rent hit 44% of 
income in 2024 — the highest rent burden of all 5 cities.

### 3. Miami — The Biggest Warning Sign
Home values grew 120% since 2015 — fastest of all cities.
Was affordable until 2022 when COVID migration pushed it 
above the 1.0 threshold for the first time.

### 4. Houston — Most Resilient
Never crossed 1.0. Rent stayed near 23% of income.
67% home value growth — significant but the most manageable.

### 5. Chicago — Quietly Worsening
Ranked most affordable in 2022 overtaking Houston, but its
index has been rising steadily. Worth monitoring.

### 6. 2021–2022 Were the Crisis Years
Every city shows its biggest YoY deterioration in 2021–2022.
LA jumped 0.302 in a single year. This aligns with post-COVID
demand surge, low inventory, and rising mortgage rates.

### 7. Rent Burden Is a Separate Crisis
Even "affordable" cities by home value show rising rent burdens.
Chicago's rent-to-income ratio hit 27.9% in 2024 — approaching
the 30% danger threshold despite low home prices.

### 8. Rankings Were Stable — Until 2022
Houston and Chicago ranked 1st and 2nd most affordable every 
year. Chicago overtook Houston in 2022 for the first time —
a sign Houston's market heated up faster that year.

### 9. LA and NY Were Already Unaffordable in 2015
Query 10 shows both cities had an index above 1.0 at the 
start of our dataset. The crisis there predates 2015.

### 10. Miami Is the Most Actionable Insight
It went from affordable to unaffordable in 3 years (2020–2022).
This speed of change is the most important signal for 
investors, policymakers, and residents planning a move.

## SQL Techniques Used
- GROUP BY with aggregate functions (AVG, MIN, MAX, ROUND)
- Window functions: RANK(), LAG(), FIRST_VALUE(), PARTITION BY
- Subqueries and JOINs for multi-year comparisons
- CASE WHEN for dynamic risk classification
- DISTINCT ON for first-occurrence detection
