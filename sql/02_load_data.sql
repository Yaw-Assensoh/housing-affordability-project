-- ============================================================
-- Housing Affordability Analysis
-- Phase 2: SQL Market Intelligence
-- File 02: Load Data from CSVs
-- ============================================================

-- Load monthly data
\COPY cities_long (city, date, year, month, home_value, monthly_rent, median_income, affordability_index) FROM 'data/cleaned/cities_long.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- Load annual summary
\COPY annual_summary (city, year, avg_home_value, avg_monthly_rent, median_income, affordability_index, status) FROM 'data/cleaned/annual_summary.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- Load income
\COPY income (year, median_income) FROM 'data/cleaned/income_clean.csv' WITH (FORMAT csv, HEADER true, NULL '');

-- Verify row counts
SELECT 'cities_long'    AS table_name, COUNT(*) AS rows FROM cities_long
UNION ALL
SELECT 'annual_summary' AS table_name, COUNT(*) AS rows FROM annual_summary
UNION ALL
SELECT 'income'         AS table_name, COUNT(*) AS rows FROM income;
