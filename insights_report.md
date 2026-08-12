# Retail Sales Analysis — Insights Report

## Data Overview
- Raw records: 5100
- Cleaned records: 4935
- Duplicates removed, missing values imputed, price outliers removed, inconsistent date formats standardized.

## Key Insights

1. **Electronics is the top-performing category**, generating ₹80,745,344 in total revenue —
   the highest of all 5 categories tracked.

2. **Revenue peaked in 2024-09** and was lowest in 2024-11, indicating a seasonal pattern
   worth investigating further (e.g. promotions, holidays, or demand cycles).

3. **West region drives the most revenue**, suggesting marketing and inventory
   should be prioritized there, while underperforming regions may need targeted promotions.

4. **Beauty has the highest return rate at 2.5%**,
   noticeably higher than other categories — worth investigating product quality or
   sizing/description accuracy for this category.

5. **Online is the stronger revenue channel**, generating
   ₹54,498,879 vs
   ₹54,114,877 from other channel(s).

6. **Customer repeat purchase rate is 100.0%** (400 of 400
   customers made more than one purchase) — a useful baseline metric for future retention campaigns.

## Business Recommendations
- Double down on Electronics with more inventory and targeted ads, since it's the clear revenue driver.
- Investigate the Beauty return rate — could be a quality, sizing, or
  description-accuracy issue that's costing money on reverse logistics.
- Design a seasonal promotion calendar around the 2024-09-style demand spike to replicate it more often.
- Since Online outperforms, consider shifting marketing budget or improving the
  underperforming channel's experience.

## Files in this project
- `retail_sales_raw.csv` — original messy dataset
- `retail_sales_cleaned.csv` — cleaned dataset ready for further analysis
- `analyze_sales.py` — this analysis script (fully reproducible)
- `charts/` — 6 PNG charts supporting the insights above
- `insights_report.md` — this report
