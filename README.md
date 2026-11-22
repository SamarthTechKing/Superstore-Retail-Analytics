🛒 Superstore Retail Analytics Dashboard | SQL + Python + Power BI

An end-to-end retail analytics project focused on understanding sales performance, customer buying behaviour, profitability and regional trends.

The project uses MySQL for database management and SQL analysis, Python for data cleaning, exploratory data analysis, customer segmentation and forecasting, Power BI for business intelligence, and Streamlit for an interactive web-based dashboard.

Developed and customized as a B.Tech Computer Science academic minor project.

🔗 Live Streamlit App: Coming soon

📌 Business Problem

A retail company wants to understand its sales performance, customer buying behaviour and profitability across regions and product categories.

The objective is to identify business opportunities, understand factors affecting profitability and support better data-driven decisions.

🎯 Project Objectives

Identify top-performing products.

Analyse profit trends over time.

Improve customer targeting.

Increase sales in weaker regions.

Find loss-making products, states and discount patterns.

Build a six-month sales forecast.

🏗️ Project Workflow

        Superstore CSV (9,994 rows, 21 columns)
                       |
                       ▼
         MySQL: Staging Table → Clean Table
                       |
                       ▼
           SQL Analysis (Region, Category,
           Customers, Monthly Trends, ABC)
                       |
                       ▼
       Python: Cleaning, EDA, RFM + K-Means,
       Correlation, Holt-Winters Forecast
                       |
                       ▼
         Power BI: 5-Page Interactive Dashboard
                       |
                       ▼
          Streamlit: Interactive Web Dashboard

⭐ Technology Stack

Category

Technology

Database

MySQL 8

Querying

SQL (CTEs, Window Functions)

Programming

Python

Data Processing

Pandas, NumPy

Visualisation

Matplotlib, Seaborn

Machine Learning

Scikit-learn (K-Means)

Forecasting

Statsmodels (Holt-Winters)

BI Tool

Power BI Desktop

Web Application

Streamlit, Plotly

Version Control

Git and GitHub

📂 Project Structure

Superstore-Retail-Analytics/
│
├── app.py
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
└── screenshots/
    ├── 1_executive_overview.png
    ├── 2_regional_drillthrough.png
    ├── 3_product_performance.png
    ├── 4_customer_segmentation.png
    └── 5_sales_forecast.png

Note: The folder is named Data/Processed with capital letters because GitHub and Streamlit's Linux servers treat folder names as case-sensitive.

📊 Dataset

The project uses Superstore retail sales data from Kaggle (Vivek468, "Superstore Dataset Final").

Item

Value

Rows (Order Lines)

9,994

Columns

21

Orders

5,009

Customers

793

Period

January 2014 – December 2017

Regions

Central, East, South, West

Categories

Furniture, Office Supplies, Technology

One row represents one product line inside an order. Therefore, Order ID can repeat, while Row ID serves as the primary key.

🗄️ SQL Analysis (MySQL)

Raw data is loaded into a text-only staging table before being cleaned and moved into a typed table. Dates are converted using STR_TO_DATE, while postal codes are retained as text.

Queries include:

Region-wise sales, profit and margin.

Profit by category and sub-category.

Top 10 customers.

Monthly sales trends, seasonality and year-over-year growth.

Loss-making sub-categories and products.

Discount level versus profit analysis.

Worst-performing states by profit.

ABC product analysis.

Repeat versus one-time customers.

🐍 Python Analysis

Python is used for data processing, statistical analysis and predictive modelling.

Key analytical tasks include:

Data cleaning: column names, date types, duplicates and missing values.

Sales and profit trend analysis.

Profitability by category, sub-category and region.

Correlation analysis involving sales, quantity, discount and profit.

Customer segmentation using RFM analysis and K-Means clustering.

Six-month sales forecasting using Holt-Winters.

Exporting processed CSV files for Power BI.

📈 Power BI Dashboard

The Power BI dashboard contains five analytical pages.

Page

Description

Executive Overview

KPI cards, monthly sales versus profit, regional sales, category profit and top customers

Regional Drill-through

Regional profitability, sub-category heatmap and bottom 10 states

Product Performance

Top products, sub-category profitability and loss-making products

Customer Segmentation

Customer clusters, at-risk customers and win-back targets

Sales Forecast

Historical sales, six-month forecast and monthly seasonality

Dashboard features include dynamic KPI cards, interactive slicers, regional drill-through and conditional formatting.

🔍 Key Business Insights

The following insights are reported in the original analysis of the dataset.

Overall Performance

Total sales: approximately $2.30 million.

Total profit: approximately $286,000.

Profit margin: approximately 12.47%.

Orders: 5,009.

Customers: 793.

Regional Performance

West leads with approximately $108,000 in profit.

East follows with approximately $92,000.

Central has approximately $501,000 in sales but only around $40,000 in profit.

Loss-Making Products and Categories

Tables generate approximately $17,700 in losses.

Bookcases generate approximately $3,500 in losses.

Supplies generate approximately $1,200 in losses.

Texas, Ohio, Pennsylvania and Illinois are among the weakest states by profit.

Seasonality

Sales generally peak in September, November and December and are weakest in January and February.

ABC Analysis

285 products (approximately 15%) account for 70% of sales.

376 products fall into Class B.

1,189 products fall into Class C.

Customer Retention

The original analysis reports that approximately 98% of customers are repeat buyers, with 174 customers identified as potential win-back targets.

Sales Forecast

The original Holt-Winters forecast predicts approximately $362,000 in sales for January to June 2018. The reported holdout MAPE is approximately 17%.

Forecasts should be interpreted as estimates rather than guaranteed outcomes.

💡 Business Recommendations

Improve Central region profitability: Review pricing and discounting strategies in weaker-performing states.

Control excessive discounts: Evaluate the relationship between discount levels and profit margins.

Review loss-making products: Consider repricing or discontinuing consistently unprofitable products.

Improve customer retention: Develop win-back campaigns for inactive customers.

Plan inventory strategically: Prepare for seasonal sales peaks in September through December.

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/SamarthTechKing/Superstore-Retail-Analytics.git

cd Superstore-Retail-Analytics

2. Create a Virtual Environment

python -m venv venv

Windows:

venv\Scripts\activate

Linux / Mac:

source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Run the Project

Run sql/superstore_analysis.sql in MySQL Workbench, section by section.

Run python/Project_2_fixed.ipynb cell by cell, setting the CSV file path correctly.

Open powerbi/superstore_dashboard.pbix in Power BI Desktop and refresh the data source path if required.

Start the Streamlit application:

streamlit run app.py

Note: Database credentials should never be committed to GitHub. Store credentials in a local .env file and include it in .gitignore.

📋 Future Enhancements

Publish the report to Power BI Service.

Introduce product-level forecasting.

Automate data refresh from MySQL.

Expand interactive dashboard capabilities.

Add additional customer and regional performance metrics.

📚 Skills Demonstrated

SQL (MySQL) · Python · Pandas · NumPy · Data Cleaning · Exploratory Data Analysis · RFM Analysis · K-Means Clustering · Time-Series Forecasting · Power BI · Dashboard Design · Business Analytics · Git and GitHub

👨‍💻 Student Developer

Samarth Sharma

B.Tech Computer Science
Academic Minor Project

🙏 Original Project Acknowledgement

The original project and source code were developed by Aaran Tuscano.

This repository is an academic adaptation of the original project. The original work is acknowledged, and additional modifications and contributions are documented as development progresses.

Original Repository:
https://github.com/AaranTuscano/Superstore-Retail-Analytics

Original copyright notices and applicable licence terms must be respected.
