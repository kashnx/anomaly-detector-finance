
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned financial data
df = pd.read_csv("data/Financials_CLEAN.csv")
df['Date'] = pd.to_datetime(df['Date'])

st.set_page_config(page_title='📊 Financial Forecasting Dashboard', layout='wide')

st.title("📈 Financial Forecasting & Anomaly Detection Dashboard (CSV Version)")

# ---- KPIs ----
st.header("📌 Key Performance Indicators")

total_rows = len(df)
total_revenue = df['Sales'].sum()
total_profit = df['Profit'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🧾 Total Records", f"{total_rows}")
col2.metric("💰 Total Revenue", f"${total_revenue:,.2f}")
col3.metric("📊 Total Profit", f"${total_profit:,.2f}")

# ---- Revenue by Year ----
st.header("📆 Revenue by Year")
df_year = df.groupby("Year")["Sales"].sum().reset_index()
st.line_chart(df_year.set_index("Year"))

# ---- Top 5 Countries ----
st.header("🌍 Top 5 Countries by Sales")
df_top = df.groupby("Country")["Sales"].sum().sort_values(ascending=False).head(5).reset_index()
st.bar_chart(df_top.set_index("Country"))

# ---- Monthly Trend ----
st.header("📅 Monthly Sales Trend (2014)")
# Filter for 2014
df_2014 = df[df["Year"] == 2014].copy()
# Normalize month names (strip whitespace and capitalize)
df_2014["Month Name"] = df_2014["Month Name"].str.strip().str.capitalize()
# Define month order
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
# Group and reindex
df_month = df_2014.groupby("Month Name")["Sales"].sum().reindex(month_order).fillna(0).reset_index()
# Plot
st.line_chart(df_month.set_index("Month Name"))

# ---- Anomaly Detection ----
st.header("🚨 Anomaly Detection: Sales Drop > 40%")

df_monthly = df.groupby(["Year", "Month Number"]).agg({'Sales': 'sum'}).reset_index()
df_monthly['date'] = pd.to_datetime(df_monthly['Year'].astype(str) + '-' + df_monthly['Month Number'].astype(str) + '-01')
df_monthly = df_monthly.sort_values('date')
df_monthly['prev_sales'] = df_monthly['Sales'].shift(1)
df_anomaly = df_monthly[df_monthly['Sales'] < 0.6 * df_monthly['prev_sales']]

st.dataframe(df_anomaly[['date', 'Sales', 'prev_sales']])

# ---- Anomaly Detection: Low Profit ----
st.header("📉 Low Profit Months (Bottom 10%)")
df_profit = df.groupby(["Year", "Month Number"]).agg({'Profit': 'sum'}).reset_index()
threshold = df_profit['Profit'].quantile(0.10)
df_low = df_profit[df_profit['Profit'] < threshold]
df_low['date'] = pd.to_datetime(df_low['Year'].astype(str) + '-' + df_low['Month Number'].astype(str) + '-01')

st.dataframe(df_low[['date', 'Profit']])
