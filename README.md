# Retail Sales Data Analysis Project

A complete, resume-ready data analyst project: clean messy real-world-style data,
analyze it, visualize it, and produce business insights.

## What's inside
- `retail_sales_raw.csv` — the raw, messy dataset (5,100 rows: duplicates, missing
  values, inconsistent date formats, price outliers — just like real data)
- `analyze_sales.py` — the main script: cleans data, runs analysis, builds charts,
  writes an insights report
- `generate_data.py` — script that created the raw dataset (optional, for reference)
- `retail_sales_cleaned.csv` — generated after you run the script
- `charts/` — 6 PNG charts generated after you run the script
- `insights_report.md` — generated business insights report

## How to run it

1. Install Python 3 if you don't have it already (https://www.python.org/downloads/)
2. Install the required libraries:
   ```
   pip install pandas numpy matplotlib seaborn
   ```
3. Open a terminal in this folder and run:
   ```
   python3 analyze_sales.py
   ```
4. Check the results:
   - `retail_sales_cleaned.csv` — the cleaned dataset
   - `charts/` — 6 charts (revenue by category, monthly trend, by region, top
     products, return rate, channel comparison)
   - `insights_report.md` — a written summary of findings and recommendations

## How to put this on your resume

**Project bullet (example):**
> Retail Sales Analysis Project — Cleaned and analyzed a 5,000+ row messy retail
> dataset in Python (Pandas); identified top revenue category and highest-return
> category, built 6 visualizations, and delivered actionable business
> recommendations. [GitHub link]

**Tips:**
- Push this whole folder to a public GitHub repo and link it on your resume.
- Open `insights_report.md` on GitHub — it renders nicely and shows recruiters
  you can turn numbers into business recommendations, not just make charts.
- If you know Power BI or Tableau, load `retail_sales_cleaned.csv` into it and
  build an interactive dashboard as a second, complementary project — that combo
  (Python cleaning + BI dashboard) is exactly what data analyst job postings ask for.
- Be ready to explain your cleaning decisions in an interview (e.g. "why did you
  fill missing prices with the category median instead of dropping the rows?") —
  interviewers care more about your reasoning than the final chart.

## Extending this project (optional, to make it stand out further)
- Add a Power BI/Tableau dashboard on top of `retail_sales_cleaned.csv`
- Add a customer segmentation analysis (RFM: Recency, Frequency, Monetary)
- Load the cleaned data into a SQL database and write the analysis as SQL
  queries instead of Pandas, to show both skill sets
