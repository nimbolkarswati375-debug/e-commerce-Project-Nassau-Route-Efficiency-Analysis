# ============================================================
# Factory-to-Customer Shipping Route Efficiency Analysis
# Nassau Candy Distributor Dashboard
# ============================================================

# ============================================================
# IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Factory-to-Customer Shipping Route Efficiency Dashboard",
    page_icon="🚚",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("Factory-to-Customer Shipping Route Efficiency Dashboard")
st.markdown("### Nassau Candy Distributor")
st.markdown("---")

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("Nassau_Candy_Cleaned.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])

    # Calculate Duration
    df["Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    return df


df = load_data()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

region_list = ["All"] + sorted(
    df["Route_Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    region_list
)

# ------------------------------------------------------------
# STATE FILTER
# ------------------------------------------------------------

state_list = ["All"] + sorted(
    df["State/Province"].dropna().unique().tolist()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    state_list
)

# ------------------------------------------------------------
# SHIP MODE FILTER
# ------------------------------------------------------------

ship_mode_list = st.sidebar.multiselect(
    "Select Ship Mode",
    options=sorted(df["Ship Mode"].unique()),
    default=sorted(df["Ship Mode"].unique())
)

# ------------------------------------------------------------
# DURATION FILTER
# ------------------------------------------------------------

duration_threshold = st.sidebar.slider(
    "Duration Threshold (Days)",
    min_value=int(df["Lead Time"].min()),
    max_value=int(df["Lead Time"].max()),
    value=int(df["Lead Time"].max())
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# Date Filter

if len(date_range) == 2:

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["Order Date"] <= pd.to_datetime(date_range[1]))
    ]

# Region Filter

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Route_Region"] == selected_region
    ]

# State Filter

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["State/Province"] == selected_state
    ]

# Ship Mode Filter

filtered_df = filtered_df[
    filtered_df["Ship Mode"].isin(ship_mode_list)
]

# Duration Filter

filtered_df = filtered_df[
    filtered_df["Lead Time"] <= duration_threshold
]

# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Shipments",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Average Order-to-Shipment Duration (Days)",
    f"{filtered_df['Lead Time'].mean():,.2f} Days"
)

col3.metric(
    "Average Cost",
    f"${filtered_df['Cost'].mean():,.2f}"
)

col4.metric(
    "Average Profit",
    f"${filtered_df['Gross Profit'].mean():,.2f}"
)

st.markdown("---")

# ============================================================
# ROUTE EFFICIENCY OVERVIEW
# ============================================================

st.header("Route Efficiency Overview")

route_analysis = (
    filtered_df
    .groupby("Route_State")
    .agg(
        Total_Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Lead Time", "mean"),
        Lead_Time_Variability=("Lead Time", "std")
    )
    .reset_index()
)

top_routes = (
    route_analysis
    .sort_values("Avg_Lead_Time")
    .head(10)
)

fig_routes = px.bar(

    top_routes,

    x="Avg_Lead_Time",

    y="Route_State",

    orientation="h",

    text="Avg_Lead_Time",

    title="Top 10 Shortest Order-to-Shipment Routes"

)

fig_routes.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig_routes.update_layout(

    xaxis_title="Average Duration (Days)",

    yaxis_title="Route",

    height=550

)

st.plotly_chart(

    fig_routes,

    width="stretch"

)

st.markdown("---")
# ============================================================
# GEOGRAPHIC ORDER-TO-SHIPMENT MAP
# ============================================================

st.header("Geographic Order-to-Shipment Map")

state_analysis = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Total_Shipments=("Order ID", "count")
    )
    .reset_index()
)

fig_map = px.choropleth(

    state_analysis,

    locations="State/Province",

    locationmode="USA-states",

    scope="usa",

    color="Avg_Lead_Time",

    hover_data=["Total_Shipments"],

    color_continuous_scale="Blues",

    title="US Order-to-Shipment Duration Heatmap"

)

st.plotly_chart(fig_map, width="stretch")

st.markdown("---")

# ============================================================
# REGIONAL BOTTLENECK ANALYSIS
# ============================================================

st.header("Regional Bottleneck Analysis")

region_analysis = (
    filtered_df
    .groupby("Route_Region")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Total_Shipments=("Order ID", "count")
    )
    .reset_index()
)

region_analysis["Bottleneck Score"] = (
    region_analysis["Avg_Lead_Time"]
    * region_analysis["Total_Shipments"]
)

fig_bottleneck = px.bar(

    region_analysis,

    x="Route_Region",

    y="Bottleneck Score",

    text="Bottleneck Score",

    title="Regional Bottleneck Score"

)

fig_bottleneck.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

st.plotly_chart(fig_bottleneck, width="stretch")

st.markdown("---")

# ============================================================
# SHIP MODE COMPARISON
# ============================================================

st.header("Ship Mode Comparison")

ship_mode_analysis = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Avg_Cost=("Cost", "mean"),
        Total_Shipments=("Order ID", "count")
    )
    .reset_index()
)

fig_shipmode = px.bar(

    ship_mode_analysis,

    x="Ship Mode",

    y="Avg_Lead_Time",

    text="Avg_Lead_Time",

    title="Average Order-to-Shipment Duration by Ship Mode"

)

fig_shipmode.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig_shipmode.update_layout(

    yaxis_title="Average Duration (Days)",

    xaxis_title="Ship Mode"

)

st.plotly_chart(fig_shipmode, width="stretch")

# ============================================================
# COST VS DURATION
# ============================================================

fig_scatter = px.scatter(

    ship_mode_analysis,

    x="Avg_Cost",

    y="Avg_Lead_Time",

    size="Total_Shipments",

    color="Ship Mode",

    hover_name="Ship Mode",

    title="Average Cost vs Order-to-Shipment Duration"

)

fig_scatter.update_layout(

    xaxis_title="Average Cost",

    yaxis_title="Average Duration (Days)"

)

st.plotly_chart(fig_scatter, width="stretch")

st.markdown("---")

# ============================================================
# ROUTE DRILL-DOWN
# ============================================================

st.header("Route Drill-Down")

# ------------------------------------------------------------
# STATE LEVEL PERFORMANCE
# ------------------------------------------------------------

st.subheader("State-Level Performance")

state_table = state_analysis.copy()

state_table["Avg_Lead_Time"] = (
    state_table["Avg_Lead_Time"].round(2)
)

state_table = state_table.rename(
    columns={
        "Avg_Lead_Time": "Average Duration (Days)",
        "Total_Shipments": "Total Shipments"
    }
)

st.dataframe(

    state_table.sort_values(

        by="Average Duration (Days)",

        ascending=False

    ),

    width="stretch",

    hide_index=True

)

# ------------------------------------------------------------
# ORDER LEVEL SHIPMENT TIMELINE
# ------------------------------------------------------------

st.subheader("Recent Shipment Timeline")

timeline_df = (

    filtered_df

    .sort_values(

        "Ship Date",

        ascending=False

    )

    .head(30)

)

fig_timeline = px.timeline(

    timeline_df,

    x_start="Order Date",

    x_end="Ship Date",

    y="Order ID",

    color="Ship Mode",

    title="Latest 30 Shipments"

)

st.plotly_chart(

    fig_timeline,

    width="stretch"

)

st.markdown("---")

# ============================================================
# FILTERED DATASET
# ============================================================

st.header("Filtered Dataset")

display_columns = [

    "Order ID",

    "Order Date",

    "Ship Date",

    "Lead Time",

    "Ship Mode",

    "Route_State",

    "State/Province",

    "Cost",

    "Gross Profit"

]

st.dataframe(

    filtered_df[display_columns],

    width="stretch",

    hide_index=True

)

st.markdown("---")

# ============================================================
# DASHBOARD FOOTER
# ============================================================

st.caption(
    """
**Dashboard Notes**

• Order-to-Shipment Duration is calculated directly from the Order Date and Ship Date available in the dataset.

• Dashboard filters update all KPIs, charts and tables dynamically.

• Developed using Python, Streamlit and Plotly.

**Project:** Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor
"""
)

# ============================================================
# END OF DASHBOARD
# ============================================================