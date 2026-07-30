# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Project Overview

The **Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor** is an interactive data analytics application developed using **Python** and **Streamlit**. The project analyzes supply chain and shipping performance to identify delivery delays, regional bottlenecks, congestion-prone states, and shipping cost efficiency.

The dashboard enables business users to monitor key logistics metrics, compare shipping modes, and make data-driven decisions to improve operational efficiency.

---
# Project Objectives

- Analyze shipping lead time across different regions.
- Evaluate shipping mode performance.
- Identify congestion-prone states.
- Detect regional supply chain bottlenecks.
- Compare shipping efficiency against shipping cost.
- Develop interactive KPI dashboards.
- Generate actionable business recommendations.

---

# Dataset Information

**Dataset:** `Nassau_Candy_Cleaned.csv`

The cleaned dataset contains approximately **10,000 shipment records** with logistics and sales information.

### Main Features

- Order ID
- Order Date
- Ship Date
- Lead Time
- Ship Mode
- Customer Information
- Product Information
- Sales
- Cost
- Gross Profit
- Region
- State
- Factory
- Route Details

---

# Project Workflow

```text
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Exploratory Data Analysis (EDA)
      │
      ▼
KPI Development
      │
      ▼
Data Visualization
      │
      ▼
Business Insights
      │
      ▼
Interactive Streamlit Dashboard
```

---

# Technology Stack

### Programming Language
- Python

### Libraries
- Pandas
- NumPy
- Plotly
- Matplotlib
- Streamlit

### Development Tools
- Visual Studio Code
- Git
- GitHub

---

#  Key Performance Indicators (KPIs)

The dashboard includes the following business KPIs:

1. Shipping Lead Time
2. On-Time Delivery Performance
3. Average Shipping Cost
4. Regional Bottleneck Score
5. Congestion-Prone States
6. Ship Mode Performance
7. Efficiency vs Cost Ratio
8. Route Efficiency Analysis

---

# Dashboard Features

The Streamlit dashboard provides:

- Executive Overview
- KPI Cards
- Shipping Lead Time Analysis
- Regional Performance Dashboard
- Ship Mode Comparison
- Congestion Analysis
- Bottleneck Analysis
- Efficiency vs Cost Analysis
- Business Recommendations
- Interactive Filters

---

# Dashboard Screenshots

images/
│
├── dashboard_home.png
├── kpi_dashboard.png
├── regional_analysis.png
├── ship_mode_analysis.png
├── bottleneck_analysis.png
└── recommendations.png
```


---

# Key Findings

The analysis revealed several important supply chain insights:

- Average Shipping Lead Time is approximately **4.49 days**.
- The **Pacific Region** recorded the highest operational bottleneck score due to its large shipment volume.
- **California** experienced the highest shipment congestion.
- **Standard Class** handled the largest number of shipments.
- **Same Day** achieved the highest Efficiency vs Cost ratio within the processed dataset.
- **Second Class** showed the lowest efficiency relative to shipping cost.

---

# Business Recommendations

Based on the analysis:

- Optimize shipping routes in high-volume regions.
- Reduce delivery delays in congestion-prone states.
- Improve warehouse processing for long lead-time shipments.
- Monitor Second Class shipping performance.
- Continue using Standard Class for routine deliveries while reserving expedited shipping for urgent orders.

---

#  Project Structure

```
Nassau_Streamlit_Dashboard/
│
├── app.py
├── Nassau_Candy_Cleaned.csv
├── requirements.txt
├── README.md
│
├── images/
│
├── pages/
│   ├── 1_Home.py
│   ├── 2_KPI_Dashboard.py
│   ├── 3_Lead_Time_Analysis.py
│   ├── 4_Regional_Analysis.py
│   ├── 5_Ship_Mode_Analysis.py
│   ├── 6_Bottleneck_Analysis.py
│   ├── 7_Congestion_Analysis.py
│   └── 8_Recommendations.py
│
└── assets/
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone https://github.com/SwatiNimbolkar/Nassau_Streamlit_Dashboard.git
```

## Navigate to the Project Folder

```bash
cd Nassau_Streamlit_Dashboard
```

## Install Required Libraries

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Dashboard

```bash
streamlit run app.py
```

The application will open automatically in your default web browser.

If not, open:

```
http://localhost:8501
```

---

# Skills Demonstrated

This project demonstrates practical skills in:

- Data Cleaning
- Data Wrangling
- Exploratory Data Analysis (EDA)
- Business KPI Development
- Data Visualization
- Interactive Dashboard Development
- Supply Chain Analytics
- Business Intelligence
- Python Programming
- Streamlit Application Development
- Git & GitHub

---

# Future Enhancements

Potential future improvements include:

- Machine Learning-Based Delay Prediction
- Demand Forecasting
- Route Optimization Algorithms
- Real-Time Data Integration
- Cloud Deployment (AWS/Azure/GCP)
- Power BI Dashboard
- Automated Report Generation

---

# Author

**Swati J. Nimbolkar**

AI & Machine Learning Engineer

Mumbai, India

**GitHub:** https://github.com/yourusername

**LinkedIn:** Your LinkedIn URL

---

# License

This project is intended for educational, research, and portfolio purposes.

---

# Acknowledgements

Special thanks to the open-source community and the developers of:

- Python
- Streamlit
- Pandas
- Plotly
- NumPy
- Matplotlib

Their tools made this project possible.

---

ss**If you found this project useful, consider giving it a star on GitHub!**