import pandas as pd

print("Reading Excel file...")

cities_long = pd.read_excel(
    'excel/housing_affordability_dashboard.xlsx',
    sheet_name='cities_long'
)

annual = pd.read_excel(
    'excel/housing_affordability_dashboard.xlsx',
    sheet_name='Annual_Summary'
)

income = pd.read_excel(
    'excel/housing_affordability_dashboard.xlsx',
    sheet_name='Income',
    header=1  # skip the merged title row
)

# Clean column names
cities_long.columns = ['city','date','year','month','home_value',
                       'monthly_rent','median_income','affordability_index']

annual.columns = ['city','year','avg_home_value','avg_monthly_rent',
                  'median_income','affordability_index','status']

income.columns = ['year','median_income']

# Save
cities_long.to_csv('data/cleaned/cities_long.csv', index=False)
annual.to_csv('data/cleaned/annual_summary.csv', index=False)
income.to_csv('data/cleaned/income_clean.csv', index=False)

print(f" cities_long.csv     → {len(cities_long)} rows")
print(f" annual_summary.csv  → {len(annual)} rows")
print(f" income_clean.csv    → {len(income)} rows")