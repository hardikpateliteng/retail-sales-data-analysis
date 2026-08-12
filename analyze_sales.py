"""
Retail Sales Data Analysis Project
-----------------------------------
A fresher-friendly, resume-ready data analyst project.

What this script does (the full analyst workflow):
1. Loads a messy, real-world-style retail sales dataset
2. Cleans it (missing values, duplicates, inconsistent text/dates, outliers)
3. Analyzes it (SQL-style groupby/aggregation questions)
4. Visualizes findings (saved as PNG charts)
5. Writes a business insights report (insights_report.md)

Run with:  python3 analyze_sales.py
Requires:  pandas, numpy, matplotlib, seaborn  (pip install pandas numpy matplotlib seaborn)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

RAW_PATH = "retail_sales_raw.csv"
CLEAN_PATH = "retail_sales_cleaned.csv"
CHARTS_DIR = "charts"
REPORT_PATH = "insights_report.md"

os.makedirs(CHARTS_DIR, exist_ok=True)

# ---------------------------------------------------------------
# STEP 1: LOAD DATA
# ---------------------------------------------------------------
print("Step 1: Loading raw data...")
df = pd.read_csv(RAW_PATH)
print(f"  Raw shape: {df.shape}")

# ---------------------------------------------------------------
# STEP 2: CLEAN DATA
# ---------------------------------------------------------------
print("Step 2: Cleaning data...")

# 2a. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"  Removed {before - len(df)} duplicate rows")

# 2b. Standardize text columns (strip whitespace, fix casing)
df["Region"] = df["Region"].astype(str).str.strip().str.title()
df["Region"] = df["Region"].replace("Nan", np.nan)

df["Category"] = df["Category"].str.strip().str.title()
df["Channel"] = df["Channel"].str.strip().str.title()
df["PaymentMethod"] = df["PaymentMethod"].astype(str).str.strip().str.title()
df["PaymentMethod"] = df["PaymentMethod"].replace("Nan", np.nan)

# 2c. Parse inconsistent date formats into a single datetime column
def parse_date(val):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y"):
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["OrderDate"] = df["OrderDate"].apply(parse_date)

# 2d. Handle missing values
# Region/PaymentMethod: fill with "Unknown" (categorical, don't want to drop rows)
df["Region"] = df["Region"].fillna("Unknown")
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")

# UnitPrice/Discount: fill with median of that category (more accurate than overall median)
df["UnitPrice"] = df.groupby("Category")["UnitPrice"].transform(
    lambda x: x.fillna(x.median())
)
df["Discount"] = df["Discount"].fillna(df["Discount"].median())

# 2e. Handle returns (negative quantity) -> separate flag, keep for return-rate analysis
df["IsReturn"] = df["Quantity"] < 0

# 2f. Handle price outliers using IQR method PER CATEGORY (data-entry errors, e.g. price * 50)
# Done per-category since a laptop and a lipstick have very different normal price ranges.
def flag_outliers(group):
    Q1 = group.quantile(0.25)
    Q3 = group.quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 3 * IQR
    return group <= upper_bound

keep_mask = df.groupby("Category")["UnitPrice"].transform(flag_outliers)
outliers_removed = (~keep_mask).sum()
df = df[keep_mask]
print(f"  Removed {outliers_removed} price outlier rows (data entry errors)")

# 2g. Drop rows where date couldn't be parsed at all
before = len(df)
df = df.dropna(subset=["OrderDate"])
print(f"  Dropped {before - len(df)} rows with unparseable dates")

# 2h. Calculate derived business metrics
df["Revenue"] = df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

print(f"  Cleaned shape: {df.shape}")
df.to_csv(CLEAN_PATH, index=False)
print(f"  Saved cleaned data to {CLEAN_PATH}")

# ---------------------------------------------------------------
# STEP 3: ANALYSIS (SQL-style business questions)
# ---------------------------------------------------------------
print("Step 3: Running analysis...")

sales_only = df[~df["IsReturn"]]

# Q1: Revenue by category
revenue_by_category = (
    sales_only.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
)

# Q2: Monthly revenue trend
monthly_revenue = sales_only.groupby("Month")["Revenue"].sum().sort_index()

# Q3: Revenue by region
revenue_by_region = (
    sales_only.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
)

# Q4: Top 10 products by revenue
top_products = (
    sales_only.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(10)
)

# Q5: Return rate by category
return_rate = df.groupby("Category")["IsReturn"].mean().sort_values(ascending=False) * 100

# Q6: Channel comparison (Online vs Retail Store)
channel_comparison = sales_only.groupby("Channel")["Revenue"].agg(["sum", "mean", "count"])

# Q7: Discount impact on average order value
discount_impact = sales_only.groupby("Discount")["Revenue"].mean()

# Q8: Repeat customer rate (customer analytics)
orders_per_customer = sales_only.groupby("CustomerID")["OrderID"].nunique()
repeat_customers = (orders_per_customer > 1).sum()
total_customers = orders_per_customer.shape[0]
repeat_rate = repeat_customers / total_customers * 100

# ---------------------------------------------------------------
# STEP 4: VISUALIZATIONS
# ---------------------------------------------------------------
print("Step 4: Generating charts...")

# Chart 1: Revenue by category
plt.figure()
revenue_by_category.plot(kind="bar", color="#4C72B0")
plt.title("Total Revenue by Category")
plt.ylabel("Revenue")
plt.xlabel("Category")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/revenue_by_category.png", dpi=150)
plt.close()

# Chart 2: Monthly revenue trend
plt.figure()
monthly_revenue.plot(kind="line", marker="o", color="#DD8452")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/monthly_revenue_trend.png", dpi=150)
plt.close()

# Chart 3: Revenue by region
plt.figure()
revenue_by_region.plot(kind="bar", color="#55A868")
plt.title("Total Revenue by Region")
plt.ylabel("Revenue")
plt.xlabel("Region")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/revenue_by_region.png", dpi=150)
plt.close()

# Chart 4: Top 10 products
plt.figure()
top_products.sort_values().plot(kind="barh", color="#C44E52")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/top_10_products.png", dpi=150)
plt.close()

# Chart 5: Return rate by category
plt.figure()
return_rate.plot(kind="bar", color="#8172B2")
plt.title("Return Rate by Category (%)")
plt.ylabel("Return Rate (%)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/return_rate_by_category.png", dpi=150)
plt.close()

# Chart 6: Channel comparison
plt.figure()
channel_comparison["sum"].plot(kind="bar", color="#937860")
plt.title("Total Revenue: Online vs Retail Store")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{CHARTS_DIR}/channel_comparison.png", dpi=150)
plt.close()

print(f"  Saved 6 charts to {CHARTS_DIR}/")

# ---------------------------------------------------------------
# STEP 5: WRITE INSIGHTS REPORT
# ---------------------------------------------------------------
print("Step 5: Writing insights report...")

top_category = revenue_by_category.index[0]
top_category_rev = revenue_by_category.iloc[0]
best_month = monthly_revenue.idxmax()
worst_month = monthly_revenue.idxmin()
top_region = revenue_by_region.index[0]
highest_return_category = return_rate.index[0]
highest_return_pct = return_rate.iloc[0]
best_channel = channel_comparison["sum"].idxmax()

report = f"""# Retail Sales Analysis — Insights Report

## Data Overview
- Raw records: {len(pd.read_csv(RAW_PATH))}
- Cleaned records: {len(df)}
- Duplicates removed, missing values imputed, price outliers removed, inconsistent date formats standardized.

## Key Insights

1. **{top_category} is the top-performing category**, generating ₹{top_category_rev:,.0f} in total revenue —
   the highest of all 5 categories tracked.

2. **Revenue peaked in {best_month}** and was lowest in {worst_month}, indicating a seasonal pattern
   worth investigating further (e.g. promotions, holidays, or demand cycles).

3. **{top_region} region drives the most revenue**, suggesting marketing and inventory
   should be prioritized there, while underperforming regions may need targeted promotions.

4. **{highest_return_category} has the highest return rate at {highest_return_pct:.1f}%**,
   noticeably higher than other categories — worth investigating product quality or
   sizing/description accuracy for this category.

5. **{best_channel} is the stronger revenue channel**, generating
   ₹{channel_comparison['sum'][best_channel]:,.0f} vs
   ₹{channel_comparison['sum'].drop(best_channel).sum():,.0f} from other channel(s).

6. **Customer repeat purchase rate is {repeat_rate:.1f}%** ({repeat_customers} of {total_customers}
   customers made more than one purchase) — a useful baseline metric for future retention campaigns.

## Business Recommendations
- Double down on {top_category} with more inventory and targeted ads, since it's the clear revenue driver.
- Investigate the {highest_return_category} return rate — could be a quality, sizing, or
  description-accuracy issue that's costing money on reverse logistics.
- Design a seasonal promotion calendar around the {best_month}-style demand spike to replicate it more often.
- Since {best_channel} outperforms, consider shifting marketing budget or improving the
  underperforming channel's experience.

## Files in this project
- `retail_sales_raw.csv` — original messy dataset
- `retail_sales_cleaned.csv` — cleaned dataset ready for further analysis
- `analyze_sales.py` — this analysis script (fully reproducible)
- `charts/` — 6 PNG charts supporting the insights above
- `insights_report.md` — this report
"""

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(report)

print(f"  Saved insights report to {REPORT_PATH}")
print("\nDone! Open insights_report.md and the charts/ folder to see the results.")
