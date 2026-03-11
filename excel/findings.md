# Phase 1 Findings — Housing Affordability Dashboard

## What I Analysed
Monthly home value and rent data for 5 US cities (2015–2024), 
cross-referenced with national median household income to calculate 
an affordability index per city per month.

## Affordability Index Explained
Formula: Median Home Price ÷ (Annual Income × 5)  
- 1.0 = affordable  
- Above 1.5 = concerning  
- Above 2.0 = severely unaffordable

## The 3 Key Observations

### 1. Los Angeles — Chronically Unaffordable
LA's affordability index exceeded 2.0 after 2020 and has stayed there.
A household earning the national median income would need to spend 
more than double the "healthy" limit to buy an average home.
This is the most extreme case in the dataset.

### 2. Houston — The Affordable Outlier
Houston is the only city that stayed below 1.5 for nearly the 
entire 2015–2024 period. Lower land costs, fewer building 
restrictions, and stronger housing supply kept prices in check 
even as other cities surged.

### 3. Miami — Fastest Deterioration Post-2020
Miami's index hovered around 1.2–1.3 from 2015–2019, then 
jumped sharply from 2020 onwards. This aligns with the well-documented 
post-COVID remote-work migration into Florida, which drove 
demand — and prices — up faster than any other city in this dataset.

## What This Means
The data shows a clear split: Sun Belt cities (Miami, Houston) 
diverged dramatically after 2020 — one becoming much less affordable 
(Miami), the other holding steady (Houston). Coastal cities like 
LA and New York remained expensive throughout, with little relief.

## Next Steps
Phase 2 will use SQL to drill into supply/demand metrics and 
identify which markets show the most risk or opportunity at a 
more granular level.