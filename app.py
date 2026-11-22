"""
Superstore Retail Analytics - Streamlit dashboard
Python version of the Power BI report (5 pages as tabs).
Reads the 3 CSVs exported by superstore_python_analysis.py from data/processed/.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Superstore Analytics", page_icon="🛒", layout="wide")

DATA_DIR = Path(__file__).parent / "Data" / "Processed"
GREEN, RED, BLUE = "#59A14F", "#E15759", "#7B4FC4"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ---------------------------------------------------------------- data
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "superstore_clean.csv", parse_dates=["order_date"])
    df["year"] = df["order_date"].dt.year
    df["month_no"] = df["order_date"].dt.month
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    seg = pd.read_csv(DATA_DIR / "customer_segments.csv")
    fc = pd.read_csv(DATA_DIR / "forecast.csv", parse_dates=["month"])
    return df, seg, fc


df, seg, fc = load_data()


def money(x):
    return f"${x:,.0f}" if abs(x) < 1e6 else f"${x / 1e6:,.2f}M"


def sign_colors(series):
    return [GREEN if v >= 0 else RED for v in series]


# ------------------------------------------------------------- sidebar
st.sidebar.title("🛒 Filters")
years = st.sidebar.multiselect("Year", sorted(df["year"].unique()), default=sorted(df["year"].unique()))
regions = st.sidebar.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
segments = st.sidebar.multiselect("Segment", sorted(df["segment"].unique()), default=sorted(df["segment"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))
st.sidebar.caption("Filters apply to every tab except the customer cluster view and the forecast, which are built on the full data.")

f = df[
    df["year"].isin(years)
    & df["region"].isin(regions)
    & df["segment"].isin(segments)
    & df["category"].isin(cats)
]

st.title("Retail Performance: Executive Dashboard")
st.caption("Superstore sales, Jan 2014 to Dec 2017")

if f.empty:
    st.warning("No data for this filter combination. Widen the filters in the sidebar.")
    st.stop()

# ----------------------------------------------------------- KPI cards
sales, profit = f["sales"].sum(), f["profit"].sum()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Sales", money(sales))
c2.metric("Total Profit", money(profit))
c3.metric("Profit Margin", f"{profit / sales:.2%}")
c4.metric("Total Orders", f"{f['order_id'].nunique():,}")
c5.metric("Total Customers", f"{f['customer_id'].nunique():,}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Executive Overview", "Regional Drill-through", "Product Performance", "Customer Segmentation", "Sales Forecast"]
)

# ------------------------------------------------- 1. Executive Overview
with tab1:
    monthly = f.groupby("year_month")[["sales", "profit"]].sum().reset_index()
    fig = px.line(monthly, x="year_month", y=["sales", "profit"], markers=True,
                  title="Monthly Sales vs Profit", color_discrete_sequence=["#2BB5B0", BLUE])
    fig.update_layout(xaxis_title="Month", yaxis_title="Amount", legend_title="")
    st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)
    reg = f.groupby("region")[["sales", "profit"]].sum().reset_index().sort_values("sales")
    reg["margin"] = (reg["profit"] / reg["sales"]).map("{:.1%}".format)
    fig = px.bar(reg, x="sales", y="region", orientation="h", text_auto=".3s", hover_data=["profit", "margin"],
                 title="Sales by Region", color_discrete_sequence=[BLUE])
    left.plotly_chart(fig, width="stretch")

    cat = f.groupby("category")[["sales", "profit"]].sum().reset_index().sort_values("profit")
    fig = px.bar(cat, x="profit", y="category", orientation="h", text_auto=".3s",
                 title="Profit by Category", color_discrete_sequence=[BLUE])
    fig.update_traces(marker_color=sign_colors(cat["profit"]))
    right.plotly_chart(fig, width="stretch")

    st.subheader("Top 5 Customers by Sales")
    top = (f.groupby("customer_name")[["sales", "profit"]].sum()
           .sort_values("sales", ascending=False).head(5).reset_index())
    top["profit_margin"] = (top["profit"] / top["sales"]).map("{:.1%}".format)
    st.dataframe(top.round(2), hide_index=True, width="stretch")

# ------------------------------------------- 2. Regional Drill-through
with tab2:
    pick = st.selectbox("Drill into a region", ["All Regions"] + sorted(f["region"].unique()))
    r = f if pick == "All Regions" else f[f["region"] == pick]
    st.subheader(f"Region: {pick}")
    k1, k2, k3 = st.columns(3)
    k1.metric("Sales", money(r["sales"].sum()))
    k2.metric("Profit", money(r["profit"].sum()))
    k3.metric("Margin", f"{r['profit'].sum() / r['sales'].sum():.2%}")

    heat = f.pivot_table(index="sub_category", columns="region", values="profit", aggfunc="sum")
    fig = px.imshow(heat, text_auto=".0f", aspect="auto", color_continuous_scale="RdYlGn",
                    color_continuous_midpoint=0, title="Profitability Heatmap: Sub-Category x Region")
    fig.update_layout(height=600)
    st.plotly_chart(fig, width="stretch")

    worst = r.groupby("state")["profit"].sum().sort_values().head(10).reset_index().sort_values("profit", ascending=False)
    fig = px.bar(worst, x="profit", y="state", orientation="h", title=f"Bottom 10 States by Profit ({pick})")
    fig.update_traces(marker_color=sign_colors(worst["profit"]))
    st.plotly_chart(fig, width="stretch")

# --------------------------------------------- 3. Product Performance
with tab3:
    left, right = st.columns(2)
    prod = f.groupby("product_name")[["sales", "profit"]].sum()
    top10 = prod.sort_values("sales", ascending=False).head(10).reset_index().sort_values("sales")
    fig = px.bar(top10, x="sales", y="product_name", orientation="h", title="Top 10 Products by Sales (red = loses money)")
    fig.update_traces(marker_color=sign_colors(top10["profit"]))
    fig.update_layout(yaxis_title="")
    left.plotly_chart(fig, width="stretch")

    sub = f.groupby("sub_category")["profit"].sum().sort_values().reset_index()
    fig = px.bar(sub, x="profit", y="sub_category", orientation="h", title="Profit by Sub-Category")
    fig.update_traces(marker_color=sign_colors(sub["profit"]))
    right.plotly_chart(fig, width="stretch")

    st.subheader("Top 10 Loss-Making Products")
    loss = prod.sort_values("profit").head(10).reset_index()
    st.dataframe(loss.round(2), hide_index=True, width="stretch")

    sc = f.groupby("sub_category").agg(sales=("sales", "sum"), profit=("profit", "sum"),
                                       avg_discount=("discount", "mean")).reset_index()
    sc["margin"] = sc["profit"] / sc["sales"]
    fig = px.scatter(sc, x="avg_discount", y="margin", size="sales", hover_name="sub_category",
                     title="Discount vs Profit Margin by Sub-Category (bubble size = sales)",
                     color_discrete_sequence=[BLUE])
    fig.update_layout(xaxis_tickformat=".0%", yaxis_tickformat=".0%")
    st.plotly_chart(fig, width="stretch")

# ------------------------------------------- 4. Customer Segmentation
with tab4:
    st.caption("Built on all customers (RFM + K-Means, 4 clusters), so the sidebar filters don't apply here.")
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Customers", f"{len(seg):,}")
    a2.metric("Repeat Rate", f"{(seg['frequency'] > 1).mean():.0%}")
    a3.metric("Avg Spend per Customer", money(seg["monetary"].mean()))
    at_risk = seg[(seg["recency"] > 180) & (seg["frequency"] >= 3)]
    a4.metric("At-Risk Customers", f"{len(at_risk):,}")

    prof = seg.groupby("cluster").agg(customers=("customer_id", "count"), avg_recency=("recency", "mean"),
                                      avg_frequency=("frequency", "mean"), avg_monetary=("monetary", "mean")).round(1)
    st.subheader("Cluster profile")
    st.dataframe(prof, width="stretch")

    left, right = st.columns(2)
    sizes = prof.reset_index()
    sizes["cluster"] = sizes["cluster"].astype(str)
    left.plotly_chart(px.pie(sizes, names="cluster", values="customers", hole=0.5, title="Customers per Cluster"),
                      width="stretch")
    plot = seg.copy()
    plot["cluster"] = plot["cluster"].astype(str)
    right.plotly_chart(px.scatter(plot, x="frequency", y="monetary", color="cluster", hover_name="customer_name",
                                  title="Segment Map: Orders vs Spend"), width="stretch")

    st.subheader("Win-Back List: High-Value Customers Gone Quiet (no order in 180+ days)")
    win = seg[seg["recency"] > 180].sort_values("monetary", ascending=False)[
        ["customer_name", "recency", "frequency", "monetary"]]
    st.dataframe(win.round(2), hide_index=True, width="stretch", height=350)

# ------------------------------------------------- 5. Sales Forecast
with tab5:
    st.caption("Holt-Winters model on monthly sales, built on all data. Forecast covers the next 6 months.")
    fig = px.line(fc, x="month", y="sales", color="type", title="Monthly Sales: Actual vs 6-Month Forecast",
                  color_discrete_map={"Actual": "#2BB5B0", "Forecast": BLUE})
    for tr in fig.data:
        if tr.name == "Forecast":
            tr.update(line=dict(dash="dash"), mode="lines+markers")
    st.plotly_chart(fig, width="stretch")

    left, right = st.columns(2)
    fut = fc[fc["type"] == "Forecast"].copy()
    fut["month"] = fut["month"].dt.strftime("%b %Y")
    left.subheader("Forecast table")
    left.dataframe(fut[["month", "sales"]].round(0), hide_index=True, width="stretch")
    left.metric("6-month forecast total", money(fut["sales"].sum()))

    seas = f.groupby("month_no")["sales"].sum().reindex(range(1, 13)).fillna(0).reset_index()
    seas["month"] = [MONTHS[i - 1] for i in seas["month_no"]]
    right.plotly_chart(px.bar(seas, x="month", y="sales", title="Seasonality: Sales by Calendar Month",
                              color_discrete_sequence=[BLUE]), width="stretch")

st.divider()
st.caption("Built by Aaran Tuscano | SQL + Python + Power BI | Data: Superstore (Kaggle)")
