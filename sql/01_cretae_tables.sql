-- ============================================================
-- Housing Affordability Analysis
-- Phase 2: SQL Market Intelligence
-- File 01: Create Tables
-- ============================================================

-- Drop tables if they already exist (clean start)
DROP TABLE IF EXISTS cities_long;
DROP TABLE IF EXISTS annual_summary;
DROP TABLE IF EXISTS income;

-- Monthly data table (600 rows)
CREATE TABLE cities_long (
    id          SERIAL PRIMARY KEY,
    city        VARCHAR(50)    NOT NULL,
    date        DATE           NOT NULL,
    year        INTEGER        NOT NULL,
    month       INTEGER        NOT NULL,
    home_value  NUMERIC(12,2),
    monthly_rent NUMERIC(10,2),
    median_income NUMERIC(10,2),
    affordability_index NUMERIC(6,3)
);

-- Annual summary table (50 rows)
CREATE TABLE annual_summary (
    id                  SERIAL PRIMARY KEY,
    city                VARCHAR(50)   NOT NULL,
    year                INTEGER       NOT NULL,
    avg_home_value      NUMERIC(12,2),
    avg_monthly_rent    NUMERIC(10,2),
    median_income       NUMERIC(10,2),
    affordability_index NUMERIC(6,3),
    status              VARCHAR(20)
);

-- Income reference table
CREATE TABLE income (
    id             SERIAL PRIMARY KEY,
    year           INTEGER       NOT NULL,
    median_income  NUMERIC(10,2) NOT NULL
);