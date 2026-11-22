# 🛒 Superstore Retail Analytics | SQL + Python + Power BI

An end-to-end analytics project on retail sales data. It starts with a MySQL database and SQL analysis, moves to Python for cleaning, profitability, customer segmentation and forecasting, and finishes with a 5-page Power BI dashboard built for business users. A Streamlit version of the dashboard is also hosted online.

The goal is simple: find out where the business makes money, where it loses it, and what to do about it.

🔗 **Live Streamlit app:** [Superstore Analytics · Streamlit](https://superstore-retail-analytics-t4xxmbjvhzbanguvwkgens.streamlit.app/)

---

## 📌 Business Problem

A retail company wants to understand its sales performance, customer buying behaviour and profitability across regions and product categories.

## 🎯 Project Objectives

- Identify top-performing products
- Analyse profit trends over time
- Improve customer targeting
- Increase sales in weaker regions
- Find loss-making products, states and discount patterns
- Build a 6-month sales forecast

---

## 🏗️ Workflow

```
        Superstore CSV (9,994 rows, 21 columns)
                        │
                        ▼
          MySQL: staging table → clean table
                        │
                        ▼
            SQL analysis (region, category,
            customers, monthly trend, ABC)
                        │
                        ▼
        Python: cleaning, EDA, RFM + K-Means,
        correlation, Holt-Winters forecast
                        │
                        ▼
          Power BI: 5-page interactive dashboard
                        │
                        ▼
      Streamlit: same dashboard, live on the web
```

## ⭐ Tech Stack

| Category | Technology |
|---|---|
| Database | MySQL 8 |
| Querying | SQL (CTEs, window functions) |
| Programming | Python |
| Data processing | Pandas, NumPy |
| Visualisation | Matplotlib, Seaborn |
| Machine learning | scikit-learn (K-Means) |
| Forecasting | statsmodels (Holt-Winters) |
| BI tool | Power BI Desktop |
| Web app | Streamlit, Plotly |
| Version control | Git and GitHub |

---

## 📂 Project Structure

```
Superstore-Retail-Analytics/
│
├── app.py                      (Streamlit dashboard)
├── requirements.txt
├── README.md
│
├── sql/
│   └── superstore_analysis.sql
│
├── python/
│   └── Project_2_fixed.ipynb
│
├── Data/
│   └── Processed/
│       ├── superstore_clean.csv
│       ├── customer_segments.csv
│       └── forecast.csv
│
├── powerbi/
│   └── superstore_dashboard.pbix
│
├── screenshots/
│   ├── 1_executive_overview.png
│   ├── 2_regional_drillthrough.png
│   ├── 3_product_performance.png
│   ├── 4_customer_segmentation.png
│   └── 5_sales_forecast.png
```

Note: the folder is `Data/Processed` with capital letters because GitHub (and Streamlit's Linux servers) treat folder names as case-sensitive.

---

## 📊 Dataset

Superstore sales data from Kaggle (Vivek468, "Superstore Dataset Final").

| Item | Value |
|---|---|
| Rows (order lines) | 9,994 |
| Columns | 21 |
| Orders | 5,009 |
| Customers | 793 |
| Period | Jan 2014 to Dec 2017 |
| Regions | Central, East, South, West |
| Categories | Furniture, Office Supplies, Technology |

One row is one product line inside an order, so `Order ID` repeats and `Row ID` is the primary key.

---

## 🗄️ SQL Analysis (MySQL)

Raw data is loaded into a text-only staging table first, then cleaned and moved into a typed table (dates converted with `STR_TO_DATE`, postal codes kept as text).

Queries included:

- Region-wise sales, profit and margin
- Profit by category and sub-category
- Top 10 customers
- Monthly sales trend, seasonality and year-over-year growth
- Loss-making sub-categories and products
- Discount level vs profit (revenue leakage)
- Worst states by profit
- ABC product analysis
- Repeat vs one-time customers

## 🐍 Python Analysis

- Data cleaning: column names, date types, duplicates, missing values
- Sales and profit trend plots, seasonality
- Profitability by category, sub-category and region x category heatmap
- Correlation matrix (sales, quantity, discount, profit)
- Customer segmentation using RFM and K-Means (4 clusters)
- 6-month sales forecast using Holt-Winters
- Clean CSV exports used by the Power BI dashboard

## 📈 Power BI Dashboard

| Page | What it shows |
|---|---|
| Executive Overview | KPI cards, monthly sales vs profit, sales by region, profit by category, top 5 customers, slicers |
| Regional Drill-through | Region drill-through, profitability heatmap (sub-category x region), bottom 10 states by profit |
| Product Performance | Top 10 products by sales, profit by sub-category, top 10 loss-making products, discount vs margin |
| Customer Segmentation | Cluster sizes, segment map, at-risk customers, win-back list |
| Sales Forecast | Actual vs 6-month forecast, seasonality by month |

Features: dynamic KPI cards, interactive slicers (Year, Region, Segment, Category), drill-through from region to detail page, and conditional colours (green for profit, red for loss).

---

## 🔍 Key Business Insights

**Overall:** $2.30M in sales, $286K in profit, 12.47% margin, 5,009 orders and 793 customers.

**Most profitable region:** West leads with about $108K profit. East follows with about $92K. Central has $501K in sales but only about $40K in profit (roughly 8% margin), the weakest of the four.

**Loss-making products and categories:**
- Tables (about -$17.7K), Bookcases (about -$3.5K) and Supplies (about -$1.2K) lose money
- Three of the top 10 products by sales also make a loss, including the Cisco TelePresence EX90
- The worst states are Texas, Ohio, Pennsylvania and Illinois

**Seasonal trends:** Sales peak in September, November and December and are weakest in January and February.

**ABC analysis (1,850 products):** 285 products (about 15%) bring in 70% of sales (class A), 376 are class B, and 1,189 are class C, adding only about 10% of sales.

**Customer retention:** 98% of customers are repeat buyers, but 174 customers who ordered often haven't ordered in over six months. These are the win-back targets.

**Forecast:** Holt-Winters predicts about $362K in sales for Jan to Jun 2018. The holdout error (MAPE) was about 17%, so treat it as a planning guide, not an exact figure.

---

## 💡 Recommendations

1. **Fix Central before expanding it.** Review pricing and discounts in Texas and Illinois first.
2. **Control discounts.** The weakest margins sit at higher discount levels, especially on Tables and Bookcases.
3. **Review loss-making products.** Reprice or drop consistent losers from the bottom-10 list.
4. **Run a win-back campaign** for the 174 high-value customers who have gone quiet.
5. **Plan stock early** for the September to December peak and keep January and February lean.

---

## 🚀 Getting Started

```bash
git clone https://github.com/AaranTuscano/Superstore-Retail-Analytics.git
cd Superstore-Retail-Analytics

python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

1. Run `sql/superstore_analysis.sql` in MySQL Workbench, section by section.
2. Run `python/Project_2_fixed.ipynb` cell by cell (set `CSV_PATH` to your file location). It exports the 3 processed CSVs.
3. Open `powerbi/superstore_dashboard.pbix` in Power BI Desktop and refresh the data source path if asked.
4. Run the Streamlit app locally with `streamlit run app.py`.

> Note: never commit database passwords. Keep credentials in a local `.env` file and add it to `.gitignore`.


---

## 📋 Future Enhancements

- Publish the report to Power BI Service
- Product-level forecasting
- Automated data refresh from MySQL

## 📚 Skills Demonstrated

SQL (MySQL) · Python · Pandas · Data Cleaning · EDA · RFM and K-Means Segmentation · Time-Series Forecasting · Power BI · DAX · Dashboard Design · Business Analytics · Git and GitHub

## 👨‍💻 Author

**Aaran Tuscano**
MBA Business Analytics | SQL | Python | Power BI

LinkedIn: [linkedin.com/in/aaran-tuscano](https://www.linkedin.com/in/aaran-tuscano)
GitHub: [github.com/AaranTuscano](https://github.com/AaranTuscano)
