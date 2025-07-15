import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Set up postgresql://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a/financial_project connection
engine = create_engine("postgresql://financial_project_user:zfNTcqmE0n5DUznuFzpIYJzm7LkGM2id@dpg-d1r5pmruibrs73f6f7ig-a.oregon-postgres.render.com/financial_project")

st.set_page_config(page_title='📊 Financial Forecasting Dashboard', layout='wide')
st.title("📈 Financial Forecasting & Anomaly Detection Dashboard")

# ---- KPIs ----
st.header("📌 Key Performance Indicators")

kpi_query = '''
SELECT
    COUNT(*) AS total_rows,
    ROUND(SUM("Sales")::numeric, 2) AS total_revenue,
    ROUND(SUM("Profit")::numeric, 2) AS total_profit
FROM financials;
'''
df_kpi = pd.read_sql(kpi_query, engine)

col1, col2, col3 = st.columns(3)
col1.metric("🧾 Total Records", f"{df_kpi['total_rows'][0]}")
col2.metric("💰 Total Revenue", f"${df_kpi['total_revenue'][0]:,.2f}")
col3.metric("📊 Total Profit", f"${df_kpi['total_profit'][0]:,.2f}")

# ---- Revenue by Year ----
st.header("📆 Revenue by Year")
rev_query = '''
SELECT "Year", SUM("Sales") AS total_revenue
FROM financials
GROUP BY "Year"
ORDER BY "Year";
'''
df_rev = pd.read_sql(rev_query, engine)
st.line_chart(df_rev.set_index("Year"))

# ---- Top 5 Countries ----
st.header("🌍 Top 5 Countries by Sales")
top_query = '''
SELECT "Country", SUM("Sales") AS total_sales
FROM financials
GROUP BY "Country"
ORDER BY total_sales DESC
LIMIT 5;
'''
df_top = pd.read_sql(top_query, engine)
st.bar_chart(df_top.set_index("Country"))

# ---- Monthly Trend ----
st.header("📅 Monthly Sales Trend (2014)")
monthly_query = '''
SELECT "Month Number", "Month Name", SUM("Sales") AS monthly_sales
FROM financials
WHERE "Year" = 2014
GROUP BY "Month Number", "Month Name"
ORDER BY "Month Number";
'''
df_month = pd.read_sql(monthly_query, engine)
st.line_chart(df_month.set_index("Month Name"))

# ---- Anomaly Detection: Sales Drop > 40% ----
st.header("🚨 Anomaly Detection: Sales Drop > 40%")
drop_query = '''
WITH monthly_sales AS (
    SELECT TO_DATE(CONCAT("Year", '-', "Month Number", '-01'), 'YYYY-MM-DD') AS date,
           SUM("Sales") AS total_sales
    FROM financials
    GROUP BY "Year", "Month Number"
),
sales_with_lag AS (
    SELECT date, total_sales,
           LAG(total_sales) OVER (ORDER BY date) AS prev_sales
    FROM monthly_sales
)
SELECT date, total_sales, prev_sales
FROM sales_with_lag
WHERE prev_sales IS NOT NULL AND total_sales < prev_sales * 0.6;
'''
df_anomaly = pd.read_sql(drop_query, engine)
st.dataframe(df_anomaly)

# ---- Anomaly Detection: Low Profit ----
st.header("📉 Low Profit Months (Bottom 10%)")
profit_query = '''
WITH profit_stats AS (
    SELECT TO_DATE(CONCAT("Year", '-', "Month Number", '-01'), 'YYYY-MM-DD') AS date,
           SUM("Profit") AS profit
    FROM financials
    GROUP BY "Year", "Month Number"
),
threshold AS (
    SELECT PERCENTILE_CONT(0.10) WITHIN GROUP (ORDER BY profit) AS low_profit_threshold
    FROM profit_stats
)
SELECT p.*
FROM profit_stats p, threshold t
WHERE p.profit < t.low_profit_threshold;
'''
df_low = pd.read_sql(profit_query, engine)
st.dataframe(df_low)

