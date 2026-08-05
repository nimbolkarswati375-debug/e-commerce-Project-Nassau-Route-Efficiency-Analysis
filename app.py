# ============================================================
# FACTORY-TO-CUSTOMER SHIPPING ROUTE EFFICIENCY DASHBOARD
# Nassau Candy Distributor
# Part 1 - Imports, Configuration, Data Loading & Filtering
# ============================================================

# ============================================================
# IMPORT LIBRARIES
# ============================================================
import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Factory-to-Customer Shipping Route Efficiency Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PAGE TITLE
# ============================================================

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")
st.markdown("### Nassau Candy Distributor")
st.markdown("---")

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    csv_file = "Nassau_Candy_Cleaned.csv"

    # Check file exists
    if not os.path.exists(csv_file):
        st.error(f"{csv_file} not found.")
        st.stop()

    # Read CSV
    try:
        df = pd.read_csv(csv_file)

    except Exception as e:
        st.error(f"Unable to read dataset.\n\n{e}")
        st.stop()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Validate required columns
    required_columns = [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Factory",
        "Region",
        "State/Province",
        "Route_State",
        "Route_Region",
        "Cost",
        "Gross Profit"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        st.error(f"Missing Columns: {missing_columns}")
        st.stop()

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["Order Date", "Ship Date"])

    # Calculate Lead Time
    df["Lead Time"] = (
        df["Ship Date"] - df["Order Date"]
    ).dt.days

    # Remove negative Lead Time
    df = df[df["Lead Time"] >= 0]

    # Fill missing numeric values
    df["Cost"] = df["Cost"].fillna(df["Cost"].median())
    df["Gross Profit"] = df["Gross Profit"].fillna(df["Gross Profit"].median())

    # Fill missing categorical values
    for col in [
        "Factory",
        "Region",
        "Ship Mode",
        "State/Province",
        "Route_State",
        "Route_Region"
    ]:
        df[col] = df[col].fillna("Unknown")

    # Remove duplicates
    df = df.drop_duplicates()

    return df
        # ----------------------------------------------------
        # Remove Negative Lead Time
        # ----------------------------------------------------
    df = df[

        df["Lead Time"] >= 0

    ]
       

        # ----------------------------------------------------
        # Fill Missing Numeric Values
        # ----------------------------------------------------
    numeric_columns = [

        "Cost",

        "Gross Profit"

    ]

    for col in numeric_columns:

        df[col] = df[col].fillna(

            df[col].median()

        )

        # ----------------------------------------------------
        # Fill Missing Categorical Values
        # ----------------------------------------------------

    categorical_columns = [

        "Factory",

        "Region",

        "Ship Mode",

        "State/Province",

        "Route_State",

        "Route_Region"

    ]

    for col in categorical_columns:

        df[col] = df[col].fillna(

            "Unknown"

        )
    

# ============================================================
# LOAD DATASET
# ============================================================

df = load_data()
# Display Dataset Information
st.write("Dataset Shape :", df.shape)

st.write("Columns")

st.write(df.columns.tolist())

st.write(df.head())

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("📌 Dashboard Filters")

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

region_options = ["All"] + sorted(
    df["Route_Region"].dropna().unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    region_options
)

# ------------------------------------------------------------
# STATE FILTER
# ------------------------------------------------------------

state_options = ["All"] + sorted(
    df["State/Province"].dropna().unique().tolist()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    state_options
)

# ------------------------------------------------------------
# SHIP MODE FILTER
# ------------------------------------------------------------

ship_modes = sorted(
    df["Ship Mode"].dropna().unique().tolist()
)

selected_ship_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    options=ship_modes,
    default=ship_modes
)

# ------------------------------------------------------------
# LEAD TIME FILTER
# ------------------------------------------------------------

duration_threshold = st.sidebar.slider(
    "Maximum Lead Time (Days)",
    min_value=int(df["Lead Time"].min()),
    max_value=int(df["Lead Time"].max()),
    value=int(df["Lead Time"].max()),
    step=1
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# ------------------------------------------------------------
# DATE FILTER
# ------------------------------------------------------------

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= start_date) &
        (filtered_df["Order Date"] <= end_date)
    ]

# ------------------------------------------------------------
# REGION FILTER
# ------------------------------------------------------------

if selected_region != "All":

    filtered_df = filtered_df[
        filtered_df["Route_Region"] == selected_region
    ]

# ------------------------------------------------------------
# STATE FILTER
# ------------------------------------------------------------

if selected_state != "All":

    filtered_df = filtered_df[
        filtered_df["State/Province"] == selected_state
    ]

# ------------------------------------------------------------
# SHIP MODE FILTER
# ------------------------------------------------------------

filtered_df = filtered_df[
    filtered_df["Ship Mode"].isin(selected_ship_modes)
]

# ------------------------------------------------------------
# LEAD TIME FILTER
# ------------------------------------------------------------

filtered_df = filtered_df[
    filtered_df["Lead Time"] <= duration_threshold
]

# ------------------------------------------------------------
# REMOVE ANY MISSING VALUES (OPTIONAL)
# ------------------------------------------------------------

filtered_df = filtered_df.dropna()

# ------------------------------------------------------------
# CHECK IF FILTERED DATA EXISTS
# ------------------------------------------------------------

if filtered_df.empty:

    st.warning("⚠️ No records match the selected filters.")

    st.stop()

# ------------------------------------------------------------
# FILTER SUMMARY
# ------------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.markdown("### 📊 Filter Summary")

st.sidebar.write(f"**Records:** {len(filtered_df):,}")

st.sidebar.write(
    f"**Average Lead Time:** {filtered_df['Lead Time'].mean():.2f} Days"
)

st.sidebar.write(
    f"**States:** {filtered_df['State/Province'].nunique()}"
)

st.sidebar.write(
    f"**Routes:** {filtered_df['Route_State'].nunique()}"
)
# ============================================================
# KPI CARDS
# ============================================================

st.markdown("## 📊 Dashboard Overview")

# ------------------------------------------------------------
# Calculate KPI Values
# ------------------------------------------------------------

total_orders = len(filtered_df)

avg_lead_time = filtered_df["Lead Time"].mean()

avg_cost = filtered_df["Cost"].mean()

avg_profit = filtered_df["Gross Profit"].mean()

total_routes = filtered_df["Route_State"].nunique()

total_states = filtered_df["State/Province"].nunique()

# Delay Threshold (5 Days)
delay_threshold = 5

delay_percentage = (
    (
        filtered_df["Lead Time"] > delay_threshold
    ).mean()
) * 100

# ------------------------------------------------------------
# Create KPI Cards
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}"
    )

with col2:

    st.metric(
        label="🚚 Average Lead Time",
        value=f"{avg_lead_time:.2f} Days"
    )

with col3:

    st.metric(
        label="💰 Average Cost",
        value=f"${avg_cost:.2f}"
    )

with col4:

    st.metric(
        label="📈 Average Gross Profit",
        value=f"${avg_profit:.2f}"
    )

# ------------------------------------------------------------
# Second KPI Row
# ------------------------------------------------------------

col5, col6, col7 = st.columns(3)

with col5:

    st.metric(
        label="🛣️ Total Routes",
        value=f"{total_routes:,}"
    )

with col6:

    st.metric(
        label="🗺️ States Covered",
        value=f"{total_states:,}"
    )

with col7:

    st.metric(
        label="⏱️ Delay Percentage",
        value=f"{delay_percentage:.1f}%"
    )

st.markdown("---")

# ============================================================
# ROUTE ANALYSIS
# ============================================================

st.markdown("## 🚚 Route Performance Analysis")

# ------------------------------------------------------------
# Aggregate Route Performance
# ------------------------------------------------------------

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

# ------------------------------------------------------------
# Clean Results
# ------------------------------------------------------------

route_analysis["Avg_Lead_Time"] = (
    route_analysis["Avg_Lead_Time"].round(2)
)

route_analysis["Lead_Time_Variability"] = (
    route_analysis["Lead_Time_Variability"]
    .fillna(0)
    .round(2)
)

# ------------------------------------------------------------
# Top 10 Fastest Routes
# ------------------------------------------------------------

top_routes = (

    route_analysis

    .sort_values(

        by="Avg_Lead_Time",

        ascending=True

    )

    .head(10)

)

# ------------------------------------------------------------
# Route Performance Chart
# ------------------------------------------------------------

fig_routes = px.bar(

    top_routes,

    x="Avg_Lead_Time",

    y="Route_State",

    orientation="h",

    color="Avg_Lead_Time",

    text="Avg_Lead_Time",

    color_continuous_scale="Greens",

    title="Top 10 Fastest Factory-to-Customer Routes"

)

fig_routes.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig_routes.update_layout(

    xaxis_title="Average Lead Time (Days)",

    yaxis_title="Factory → Customer State",

    height=550,

    coloraxis_showscale=False,

    yaxis=dict(

        categoryorder="total ascending"

    )

)

st.plotly_chart(

    fig_routes,

    use_container_width=True

)

# ------------------------------------------------------------
# Route Analysis Table
# ------------------------------------------------------------

st.subheader("📋 Route Performance Summary")

st.dataframe(

    route_analysis

    .sort_values(

        by="Avg_Lead_Time"

    ),

    use_container_width=True,

    hide_index=True

)

st.markdown("---")

# ============================================================
# GEOGRAPHIC SHIPPING MAP
# ============================================================

st.markdown("## 🗺️ Geographic Shipping Performance")

# ------------------------------------------------------------
# State-wise Aggregation
# ------------------------------------------------------------

state_analysis = (

    filtered_df

    .groupby("State/Province")

    .agg(

        Total_Shipments=("Order ID","count"),

        Avg_Lead_Time=("Lead Time","mean")

    )

    .reset_index()

)

state_analysis["Avg_Lead_Time"] = (
    state_analysis["Avg_Lead_Time"].round(2)
)

# ------------------------------------------------------------
# USA State Abbreviations
# ------------------------------------------------------------

state_abbrev = {

    "Alabama":"AL",
    "Alaska":"AK",
    "Arizona":"AZ",
    "Arkansas":"AR",
    "California":"CA",
    "Colorado":"CO",
    "Connecticut":"CT",
    "Delaware":"DE",
    "District Of Columbia":"DC",
    "Florida":"FL",
    "Georgia":"GA",
    "Hawaii":"HI",
    "Idaho":"ID",
    "Illinois":"IL",
    "Indiana":"IN",
    "Iowa":"IA",
    "Kansas":"KS",
    "Kentucky":"KY",
    "Louisiana":"LA",
    "Maine":"ME",
    "Maryland":"MD",
    "Massachusetts":"MA",
    "Michigan":"MI",
    "Minnesota":"MN",
    "Mississippi":"MS",
    "Missouri":"MO",
    "Montana":"MT",
    "Nebraska":"NE",
    "Nevada":"NV",
    "New Hampshire":"NH",
    "New Jersey":"NJ",
    "New Mexico":"NM",
    "New York":"NY",
    "North Carolina":"NC",
    "North Dakota":"ND",
    "Ohio":"OH",
    "Oklahoma":"OK",
    "Oregon":"OR",
    "Pennsylvania":"PA",
    "Rhode Island":"RI",
    "South Carolina":"SC",
    "South Dakota":"SD",
    "Tennessee":"TN",
    "Texas":"TX",
    "Utah":"UT",
    "Vermont":"VT",
    "Virginia":"VA",
    "Washington":"WA",
    "West Virginia":"WV",
    "Wisconsin":"WI",
    "Wyoming":"WY"
}

# ------------------------------------------------------------
# Convert to State Codes
# ------------------------------------------------------------

state_analysis["State_Code"] = (
    state_analysis["State/Province"]
    .map(state_abbrev)
)

# Keep only USA states for the map
usa_map = state_analysis.dropna(subset=["State_Code"])

# ------------------------------------------------------------
# Choropleth Map
# ------------------------------------------------------------

fig_map = px.choropleth(

    usa_map,

    locations="State_Code",

    locationmode="USA-states",

    color="Avg_Lead_Time",

    hover_name="State/Province",

    hover_data={

        "Total_Shipments":True,

        "Avg_Lead_Time":":.2f",

        "State_Code":False

    },

    scope="usa",

    color_continuous_scale="YlOrRd",

    title="Average Shipping Lead Time Across U.S. States"

)

fig_map.update_layout(

    height=600,

    margin=dict(l=20,r=20,t=60,b=20)

)

st.plotly_chart(

    fig_map,

    use_container_width=True

)

# ------------------------------------------------------------
# State Performance Table
# ------------------------------------------------------------

st.subheader("📋 State Shipping Performance")

st.dataframe(

    state_analysis

    .sort_values(

        by="Avg_Lead_Time",

        ascending=False

    ),

    hide_index=True,

    use_container_width=True

)

st.markdown("---")
# ============================================================
# REGIONAL BOTTLENECK ANALYSIS
# ============================================================

st.markdown("## 🚧 Regional Bottleneck Analysis")

# ------------------------------------------------------------
# Aggregate Region Performance
# ------------------------------------------------------------

region_analysis = (

    filtered_df

    .groupby("Region")

    .agg(

        Total_Shipments=("Order ID", "count"),

        Avg_Lead_Time=("Lead Time", "mean"),

        Lead_Time_Variability=("Lead Time", "std")

    )

    .reset_index()

)

# ------------------------------------------------------------
# Clean Values
# ------------------------------------------------------------

region_analysis["Avg_Lead_Time"] = (
    region_analysis["Avg_Lead_Time"].round(2)
)

region_analysis["Lead_Time_Variability"] = (
    region_analysis["Lead_Time_Variability"]
    .fillna(0)
    .round(2)
)

# ------------------------------------------------------------
# Bottleneck Score
# Formula = Avg Lead Time × Total Shipments
# ------------------------------------------------------------

region_analysis["Bottleneck_Score"] = (

    region_analysis["Avg_Lead_Time"]

    *

    region_analysis["Total_Shipments"]

).round(0)

# ------------------------------------------------------------
# Classification Rules
# ------------------------------------------------------------

overall_lead = filtered_df["Lead Time"].mean()

overall_shipments = (
    filtered_df["Order ID"].count()
    /
    region_analysis.shape[0]
)

def classify_region(row):

    if (
        row["Avg_Lead_Time"] > overall_lead
        and
        row["Total_Shipments"] > overall_shipments
    ):
        return "Critical Bottleneck"

    elif row["Avg_Lead_Time"] > overall_lead:
        return "Slow but Low Volume"

    else:
        return "Efficient"

region_analysis["Category"] = (

    region_analysis

    .apply(

        classify_region,

        axis=1

    )

)

# ------------------------------------------------------------
# Sort Results
# ------------------------------------------------------------

region_analysis = region_analysis.sort_values(

    by="Bottleneck_Score",

    ascending=False

)

# ------------------------------------------------------------
# Colour Mapping
# ------------------------------------------------------------

color_map = {

    "Critical Bottleneck": "red",

    "Slow but Low Volume": "orange",

    "Efficient": "green"

}

# ------------------------------------------------------------
# Interactive Chart
# ------------------------------------------------------------

fig_region = px.bar(

    region_analysis,

    x="Region",

    y="Bottleneck_Score",

    color="Category",

    text="Bottleneck_Score",

    color_discrete_map=color_map,

    title="Regional Bottleneck Score"

)

fig_region.update_traces(

    textposition="outside"

)

fig_region.update_layout(

    yaxis_title="Bottleneck Score",

    xaxis_title="Region",

    height=500

)

st.plotly_chart(

    fig_region,

    use_container_width=True

)

# ------------------------------------------------------------
# Summary Table
# ------------------------------------------------------------

st.subheader("📋 Regional Performance Summary")

st.dataframe(

    region_analysis,

    hide_index=True,

    use_container_width=True

)

st.markdown("---")
# ============================================================
# SHIP MODE COMPARISON
# ============================================================

st.markdown("## 🚚 Ship Mode Performance Comparison")

# ------------------------------------------------------------
# Aggregate Ship Mode Performance
# ------------------------------------------------------------

ship_mode_analysis = (

    filtered_df

    .groupby("Ship Mode")

    .agg(

        Total_Shipments=("Order ID", "count"),

        Avg_Lead_Time=("Lead Time", "mean"),

        Avg_Cost=("Cost", "mean"),

        Avg_Gross_Profit=("Gross Profit", "mean"),

        Lead_Time_Variability=("Lead Time", "std")

    )

    .reset_index()

)

# ------------------------------------------------------------
# Clean Results
# ------------------------------------------------------------

ship_mode_analysis["Avg_Lead_Time"] = (
    ship_mode_analysis["Avg_Lead_Time"].round(2)
)

ship_mode_analysis["Avg_Cost"] = (
    ship_mode_analysis["Avg_Cost"].round(2)
)

ship_mode_analysis["Avg_Gross_Profit"] = (
    ship_mode_analysis["Avg_Gross_Profit"].round(2)
)

ship_mode_analysis["Lead_Time_Variability"] = (
    ship_mode_analysis["Lead_Time_Variability"]
    .fillna(0)
    .round(2)
)

# ------------------------------------------------------------
# Efficiency per Cost
# Higher value = Better Value
# ------------------------------------------------------------

ship_mode_analysis["Efficiency_per_Cost"] = (

    ship_mode_analysis["Avg_Lead_Time"]

    /

    ship_mode_analysis["Avg_Cost"]

).round(3)

# ------------------------------------------------------------
# Ship Mode Performance Chart
# ------------------------------------------------------------

fig_ship = px.bar(

    ship_mode_analysis,

    x="Ship Mode",

    y="Avg_Lead_Time",

    color="Ship Mode",

    text="Avg_Lead_Time",

    title="Average Shipping Lead Time by Ship Mode"

)

fig_ship.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig_ship.update_layout(

    height=500,

    xaxis_title="Ship Mode",

    yaxis_title="Average Lead Time (Days)",

    showlegend=False

)

st.plotly_chart(

    fig_ship,

    use_container_width=True

)

# ------------------------------------------------------------
# Shipment Distribution
# ------------------------------------------------------------

fig_pie = px.pie(

    ship_mode_analysis,

    names="Ship Mode",

    values="Total_Shipments",

    hole=0.45,

    title="Shipment Distribution by Ship Mode"

)

st.plotly_chart(

    fig_pie,

    use_container_width=True

)

# ------------------------------------------------------------
# Ship Mode Summary Table
# ------------------------------------------------------------

st.subheader("📋 Ship Mode Performance Summary")

st.dataframe(

    ship_mode_analysis.sort_values(

        by="Avg_Lead_Time"

    ),

    hide_index=True,

    use_container_width=True

)

# ------------------------------------------------------------
# Best Performing Ship Mode
# ------------------------------------------------------------

best_mode = ship_mode_analysis.loc[
    ship_mode_analysis["Avg_Lead_Time"].idxmin()
]

st.success(

    f"""
    **Best Performing Ship Mode:** {best_mode['Ship Mode']}

    • Average Lead Time : {best_mode['Avg_Lead_Time']:.2f} Days

    • Average Cost : ${best_mode['Avg_Cost']:.2f}

    • Total Shipments : {int(best_mode['Total_Shipments'])}
    """

)

st.markdown("---")

# ============================================================
# EFFICIENCY VS COST ANALYSIS
# ============================================================

st.markdown("## 💰 Efficiency vs Cost Analysis")

# ------------------------------------------------------------
# Calculate Efficiency per Cost
# Formula = Average Lead Time / Average Cost
# Higher value indicates better operational efficiency
# ------------------------------------------------------------

efficiency_vs_cost = ship_mode_analysis.copy()

efficiency_vs_cost["Efficiency_per_Cost"] = (

    efficiency_vs_cost["Avg_Lead_Time"]

    /

    efficiency_vs_cost["Avg_Cost"]

).round(3)

# ------------------------------------------------------------
# Sort by Efficiency Score
# ------------------------------------------------------------

efficiency_vs_cost = (

    efficiency_vs_cost

    .sort_values(

        by="Efficiency_per_Cost",

        ascending=False

    )

)

# ------------------------------------------------------------
# Scatter Plot
# ------------------------------------------------------------

fig_efficiency = px.scatter(

    efficiency_vs_cost,

    x="Avg_Cost",

    y="Avg_Lead_Time",

    size="Total_Shipments",

    color="Ship Mode",

    hover_name="Ship Mode",

    text="Ship Mode",

    title="Efficiency vs Cost by Ship Mode",

    labels={

        "Avg_Cost":"Average Cost ($)",

        "Avg_Lead_Time":"Average Lead Time (Days)"

    }

)

fig_efficiency.update_traces(

    textposition="top center",

    marker=dict(

        sizemode="area",

        line=dict(

            width=1,

            color="black"

        )

    )

)

fig_efficiency.update_layout(

    height=550

)

st.plotly_chart(

    fig_efficiency,

    use_container_width=True

)

# ------------------------------------------------------------
# Efficiency Ranking
# ------------------------------------------------------------

fig_rank = px.bar(

    efficiency_vs_cost,

    x="Ship Mode",

    y="Efficiency_per_Cost",

    color="Ship Mode",

    text="Efficiency_per_Cost",

    title="Efficiency per Cost Ranking"

)

fig_rank.update_traces(

    texttemplate="%{text:.3f}",

    textposition="outside"

)

fig_rank.update_layout(

    height=450,

    showlegend=False,

    xaxis_title="Ship Mode",

    yaxis_title="Efficiency per Cost"

)

st.plotly_chart(

    fig_rank,

    use_container_width=True

)

# ------------------------------------------------------------
# Summary Table
# ------------------------------------------------------------

st.subheader("📋 Efficiency vs Cost Summary")

st.dataframe(

    efficiency_vs_cost[

        [

            "Ship Mode",

            "Avg_Lead_Time",

            "Avg_Cost",

            "Total_Shipments",

            "Efficiency_per_Cost"

        ]

    ],

    hide_index=True,

    use_container_width=True

)

# ------------------------------------------------------------
# Best Value Recommendation
# ------------------------------------------------------------

best_mode = efficiency_vs_cost.iloc[0]

st.success(

    f"""

### 🏆 Best Cost-Efficient Shipping Mode

**Ship Mode:** {best_mode['Ship Mode']}

• Efficiency per Cost : **{best_mode['Efficiency_per_Cost']:.3f}**

• Average Lead Time : **{best_mode['Avg_Lead_Time']:.2f} Days**

• Average Cost : **${best_mode['Avg_Cost']:.2f}**

• Total Shipments : **{int(best_mode['Total_Shipments'])}**

This shipping mode provides the highest operational efficiency relative to its average transportation cost.

"""

)

st.markdown("---")

# ============================================================
# TIMELINE ANALYSIS
# ============================================================

st.markdown("## 📅 Shipping Timeline Analysis")

# ------------------------------------------------------------
# Create Month-Year Column
# ------------------------------------------------------------

timeline_df = filtered_df.copy()

timeline_df["Month"] = (
    timeline_df["Order Date"]
    .dt.to_period("M")
    .astype(str)
)

# ------------------------------------------------------------
# Monthly Aggregation
# ------------------------------------------------------------

timeline_analysis = (

    timeline_df

    .groupby("Month")

    .agg(

        Total_Orders=("Order ID", "count"),

        Avg_Lead_Time=("Lead Time", "mean"),

        Avg_Cost=("Cost", "mean"),

        Avg_Gross_Profit=("Gross Profit", "mean")

    )

    .reset_index()

)

# ------------------------------------------------------------
# Round Values
# ------------------------------------------------------------

timeline_analysis["Avg_Lead_Time"] = (
    timeline_analysis["Avg_Lead_Time"].round(2)
)

timeline_analysis["Avg_Cost"] = (
    timeline_analysis["Avg_Cost"].round(2)
)

timeline_analysis["Avg_Gross_Profit"] = (
    timeline_analysis["Avg_Gross_Profit"].round(2)
)

# ------------------------------------------------------------
# Monthly Order Trend
# ------------------------------------------------------------

fig_orders = px.line(

    timeline_analysis,

    x="Month",

    y="Total_Orders",

    markers=True,

    title="Monthly Order Volume"

)

fig_orders.update_layout(

    height=450,

    xaxis_title="Month",

    yaxis_title="Total Orders"

)

st.plotly_chart(

    fig_orders,

    use_container_width=True

)

# ------------------------------------------------------------
# Monthly Lead Time Trend
# ------------------------------------------------------------

fig_lead = px.line(

    timeline_analysis,

    x="Month",

    y="Avg_Lead_Time",

    markers=True,

    title="Monthly Average Shipping Lead Time"

)

fig_lead.update_layout(

    height=450,

    xaxis_title="Month",

    yaxis_title="Average Lead Time (Days)"

)

st.plotly_chart(

    fig_lead,

    use_container_width=True

)

# ------------------------------------------------------------
# Combined Trend
# ------------------------------------------------------------

fig_combo = px.bar(

    timeline_analysis,

    x="Month",

    y="Total_Orders",

    text="Total_Orders",

    title="Orders and Average Lead Time by Month"

)

fig_combo.add_scatter(

    x=timeline_analysis["Month"],

    y=timeline_analysis["Avg_Lead_Time"],

    mode="lines+markers",

    name="Average Lead Time"

)

fig_combo.update_layout(

    height=500,

    yaxis_title="Total Orders",

    xaxis_title="Month"

)

st.plotly_chart(

    fig_combo,

    use_container_width=True

)

# ------------------------------------------------------------
# Timeline Summary Table
# ------------------------------------------------------------

st.subheader("📋 Monthly Shipping Performance")

st.dataframe(

    timeline_analysis,

    hide_index=True,

    use_container_width=True

)

# ------------------------------------------------------------
# Monthly Insights
# ------------------------------------------------------------

highest_orders = timeline_analysis.loc[
    timeline_analysis["Total_Orders"].idxmax()
]

lowest_lead = timeline_analysis.loc[
    timeline_analysis["Avg_Lead_Time"].idxmin()
]

st.info(

    f"""

### 📈 Timeline Insights

• Highest shipment volume occurred in **{highest_orders['Month']}**
with **{int(highest_orders['Total_Orders'])} orders**.

• Fastest average delivery performance was achieved in
**{lowest_lead['Month']}**
with an average lead time of **{lowest_lead['Avg_Lead_Time']:.2f} days**.

"""

)

st.markdown("---")

# ============================================================
# ROUTE DRILL-DOWN ANALYSIS
# ============================================================

st.markdown("## 🔍 Route Drill-Down Analysis")

st.write(
    "Select a Factory-to-Customer route to explore detailed shipment performance."
)

# ------------------------------------------------------------
# Route Selection
# ------------------------------------------------------------

route_list = sorted(filtered_df["Route_State"].unique())

selected_route = st.selectbox(

    "Select Route",

    route_list

)

# ------------------------------------------------------------
# Filter Selected Route
# ------------------------------------------------------------

route_df = filtered_df[

    filtered_df["Route_State"] == selected_route

].copy()

# ------------------------------------------------------------
# Route KPIs
# ------------------------------------------------------------

total_shipments = len(route_df)

avg_lead = route_df["Lead Time"].mean()

avg_cost = route_df["Cost"].mean()

avg_profit = route_df["Gross Profit"].mean()

lead_variability = route_df["Lead Time"].std()

if pd.isna(lead_variability):
    lead_variability = 0

# ------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Shipments",
    f"{total_shipments:,}"
)

c2.metric(
    "Avg Lead Time",
    f"{avg_lead:.2f} Days"
)

c3.metric(
    "Avg Cost",
    f"${avg_cost:.2f}"
)

c4.metric(
    "Avg Profit",
    f"${avg_profit:.2f}"
)

c5.metric(
    "Lead Time Std",
    f"{lead_variability:.2f}"
)

# ------------------------------------------------------------
# Lead Time Distribution
# ------------------------------------------------------------

fig_hist = px.histogram(

    route_df,

    x="Lead Time",

    nbins=15,

    title=f"Lead Time Distribution<br>{selected_route}"

)

fig_hist.update_layout(

    height=450,

    xaxis_title="Lead Time (Days)",

    yaxis_title="Number of Shipments"

)

st.plotly_chart(

    fig_hist,

    use_container_width=True

)

# ------------------------------------------------------------
# Ship Mode Distribution
# ------------------------------------------------------------

ship_mode_route = (

    route_df

    .groupby("Ship Mode")

    .size()

    .reset_index(name="Shipments")

)

fig_mode = px.pie(

    ship_mode_route,

    names="Ship Mode",

    values="Shipments",

    hole=0.45,

    title="Ship Mode Distribution"

)

st.plotly_chart(

    fig_mode,

    use_container_width=True

)

# ------------------------------------------------------------
# Shipment Details
# ------------------------------------------------------------

st.subheader("📋 Shipment Details")

display_columns = [

    "Order ID",

    "Order Date",

    "Ship Date",

    "Ship Mode",

    "State/Province",

    "Cost",

    "Gross Profit",

    "Lead Time"

]

st.dataframe(

    route_df[display_columns]

    .sort_values(

        by="Order Date"

    ),

    hide_index=True,

    use_container_width=True

)

# ------------------------------------------------------------
# Route Summary
# ------------------------------------------------------------

st.success(

f"""

### Route Summary

**Selected Route:** {selected_route}

- Total Shipments: **{total_shipments:,}**

- Average Lead Time: **{avg_lead:.2f} Days**

- Average Transportation Cost: **${avg_cost:.2f}**

- Average Gross Profit: **${avg_profit:.2f}**

- Lead Time Variability: **{lead_variability:.2f} Days**

This section enables detailed operational monitoring of individual factory-to-customer routes and helps identify high-performing as well as underperforming logistics routes.

"""

)

st.markdown("---")
# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.markdown("## 📥 Download Filtered Data")

st.write(
    "Download the filtered shipment data for further analysis in Excel, Power BI, or other reporting tools."
)

# ------------------------------------------------------------
# Convert DataFrame to CSV
# ------------------------------------------------------------

@st.cache_data
def convert_to_csv(dataframe):

    return dataframe.to_csv(index=False).encode("utf-8")

csv = convert_to_csv(filtered_df)

# ------------------------------------------------------------
# Download Button
# ------------------------------------------------------------

st.download_button(

    label="📥 Download Filtered Dataset (CSV)",

    data=csv,

    file_name="Filtered_Shipping_Data.csv",

    mime="text/csv"

)

# ------------------------------------------------------------
# Dataset Summary
# ------------------------------------------------------------

st.subheader("📊 Filtered Dataset Summary")

summary = pd.DataFrame({

    "Metric":[

        "Total Records",

        "Total Routes",

        "States Covered",

        "Average Lead Time (Days)",

        "Average Cost ($)",

        "Average Gross Profit ($)"

    ],

    "Value":[

        len(filtered_df),

        filtered_df["Route_State"].nunique(),

        filtered_df["State/Province"].nunique(),

        round(filtered_df["Lead Time"].mean(),2),

        round(filtered_df["Cost"].mean(),2),

        round(filtered_df["Gross Profit"].mean(),2)

    ]

})

st.dataframe(

    summary,

    hide_index=True,

    use_container_width=True

)

st.success(
    "The downloaded CSV contains only the records matching the selected dashboard filters."
)

st.markdown("---")


"""
**Dashboard Notes**

• Order-to-Shipment Duration is calculated directly from the Order Date and Ship Date available in the dataset.

• Dashboard filters update all KPIs, charts and tables dynamically.

• Developed using Python, Streamlit and Plotly.

**Project:** Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor
"""
# ============================================================
# END OF DASHBOARD
# ============================================================
