-- ============================================================
-- Housing Affordability Analysis
-- Phase 2: SQL Market Intelligence
-- File 03: Analysis Queries
-- ============================================================

-- Query 1: Average Home Value per City (2015-2024)
-- Finding: Los Angeles is the most expensive city, nearly
-- double Houston which remains the most affordable
SELECT city, ROUND(AVG(home_value), 2) AS avg_home_value
FROM cities_long
GROUP BY city
ORDER BY avg_home_value DESC;

-- ============================================================

-- Query 2: Average Affordability Index per City
-- Finding: LA average of 1.745 confirms it as the least
-- affordable city across the entire period
SELECT city, ROUND(AVG(affordability_index), 3) AS avg_affordability
FROM cities_long
GROUP BY city
ORDER BY avg_affordability DESC;

-- ============================================================

-- Query 3: Affordability Index Trend by City and Year
-- Finding: Miami nearly doubled from 0.611 to 1.170,
-- all cities worsened sharply post-2020
SELECT city, year, ROUND(AVG(affordability_index), 3) AS avg_affordability
FROM cities_long
GROUP BY city, year
ORDER BY city, year;

-- ============================================================

-- Query 4: Most Expensive City per Year
-- Finding: Los Angeles was the most expensive city
-- every single year from 2015 to 2024
SELECT DISTINCT year,
       FIRST_VALUE(city) OVER (PARTITION BY year ORDER BY avg_hv DESC) AS most_expensive_city,
       FIRST_VALUE(ROUND(avg_hv, 0)) OVER (PARTITION BY year ORDER BY avg_hv DESC) AS home_value
FROM (
    SELECT city, year, AVG(home_value) AS avg_hv
    FROM cities_long
    GROUP BY city, year
) sub
ORDER BY year;

-- ============================================================

-- Query 5: City Affordability Rankings per Year
-- Finding: Rankings stayed consistent for 8 of 10 years.
-- Chicago overtook Houston as most affordable in 2022
SELECT city, year,
       ROUND(AVG(affordability_index), 3) AS avg_affordability,
       RANK() OVER (PARTITION BY year ORDER BY AVG(affordability_index) ASC) AS affordability_rank
FROM cities_long
GROUP BY city, year
ORDER BY year, affordability_rank;

-- ============================================================

-- Query 6: Year Over Year Change in Affordability
-- Finding: 2021-2022 were the worst years across all cities.
-- LA deteriorated 0.302 in a single year (2022)
SELECT city, year,
       ROUND(AVG(affordability_index), 3) AS avg_affordability,
       ROUND(AVG(affordability_index) - LAG(AVG(affordability_index))
           OVER (PARTITION BY city ORDER BY year), 3) AS yoy_change
FROM cities_long
GROUP BY city, year
ORDER BY city, year;

-- ============================================================

-- Query 7: Market Risk Summary
-- Finding: LA is HIGH RISK, New York MODERATE RISK.
-- Miami is technically LOW RISK but has the second highest
-- total deterioration — a warning sign for the future
SELECT
    city,
    ROUND(MIN(affordability_index), 3) AS best_ever,
    ROUND(MAX(affordability_index), 3) AS worst_ever,
    ROUND(MAX(affordability_index) - MIN(affordability_index), 3) AS total_deterioration,
    ROUND(AVG(affordability_index), 3) AS avg_index,
    CASE
        WHEN AVG(affordability_index) > 1.5 THEN 'HIGH RISK'
        WHEN AVG(affordability_index) > 1.0 THEN 'MODERATE RISK'
        ELSE 'LOW RISK'
    END AS risk_level
FROM cities_long
GROUP BY city
ORDER BY avg_index DESC;

-- ============================================================

-- Query 8: Rent to Income Ratio by City and Year
-- Finding: New York hit 44% rent-to-income in 2024 — the highest
-- burden of all 5 cities. LA reached 40%. Houston remained the
-- healthiest near 23% throughout. Miami jumped from 24% to 37%
-- post-2020 — a sign of rapid deterioration beyond home prices.
SELECT city, year,
       ROUND(AVG(monthly_rent), 2) AS avg_rent,
       ROUND(AVG(median_income), 2) AS avg_income,
       ROUND((AVG(monthly_rent) * 12) / AVG(median_income) * 100, 2) AS rent_to_income_pct
FROM cities_long
GROUP BY city, year
ORDER BY city, year;

-- ============================================================

-- Query 9: Total Home Value Growth 2015 vs 2024
-- Finding: Miami had the highest growth at 120.2% despite
-- starting from a lower base. LA grew 85.3% on top of already
-- being the most expensive city. New York had the lowest
-- growth at 59.4% but started from the highest base.
SELECT
    a.city,
    ROUND(a.avg_home_value, 0) AS value_2015,
    ROUND(b.avg_home_value, 0) AS value_2024,
    ROUND(((b.avg_home_value - a.avg_home_value) / a.avg_home_value) * 100, 1) AS growth_pct
FROM
    (SELECT city, AVG(home_value) AS avg_home_value
     FROM cities_long WHERE year = 2015
     GROUP BY city) a
JOIN
    (SELECT city, AVG(home_value) AS avg_home_value
     FROM cities_long WHERE year = 2024
     GROUP BY city) b
ON a.city = b.city
ORDER BY growth_pct DESC;

-- ============================================================

-- Query 10: First Year Each City Crossed Affordability Threshold
-- Finding: LA and New York were already above 1.0 in 2015 meaning
-- the crisis predates our dataset. Miami only crossed in 2022 —
-- directly linked to the post-COVID migration boom into Florida.
-- Chicago and Houston never crossed 1.0 in the entire period.
SELECT DISTINCT ON (city)
    city,
    year,
    ROUND(AVG(affordability_index), 3) AS avg_index
FROM cities_long
GROUP BY city, year
HAVING AVG(affordability_index) > 1.0
ORDER BY city, year ASC;