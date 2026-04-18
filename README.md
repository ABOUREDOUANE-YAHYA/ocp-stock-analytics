# OCP Stock Analytics Dashboard

> Simulation et analyse de la gestion de stock d'un entrepôt industriel OCP,
> avec suivi des mouvements, alertes de rupture et KPIs opérationnels.

---

## Context

During my internship at OCP Group (one of the world's largest phosphate producers),
I worked on a stock management system. This project adds an **analytical layer**
on top of that experience, simulating realistic warehouse data and building
an interactive dashboard to monitor stock performance.

---

## Problem Statement

How can a warehouse manager at OCP:
- Detect **stock shortage risks** before they cause production stops ?
- Track **monthly inflows vs outflows** per product category ?
- Identify which products trigger the **most rupture alerts** ?

---

## Key KPIs

|       KPI         |         Value        |
|-------------------|----------------------|
| Total Movements   |         7,648        |
| Rupture Alerts    |         252          |
| Alert Rate        |         3.3%         |
| Products Tracked  |         8            |
| Period            |  Jan 2023 → Dec 2024 |

---

## Dashboard Features

- **Stock level evolution** per product over time
- **Rupture alerts** ranking by product
- **Monthly inflows vs outflows** comparison
- **Average stock level** by category
- **Live alerts table** showing the 10 most recent shortages
- **Interactive filters** by category, product, movement type and date range

---

## Tech Stack

|       Tool        |            Usage           |
|-------------------|----------------------------|
| Python            | Data simulation & analysis |
| pandas            | Data manipulation          |
| matplotlib        | Data visualization         |
| Streamlit         | Interactive dashboard      |

---

## Project Structure
OCP_STOCK_ANALYTICS/
├── generate_data.py        # Realistic data simulation script
├── ocp_stock_data.csv      # Generated dataset
├── dashboard.py            # Streamlit dashboard
└── README.md               # You are here
---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/ABOUREDOUANE-YAHYA/ocp-stock-analytics.git
cd ocp-stock-analytics

# 2. Install dependencies
pip install pandas matplotlib streamlit

# 3. Generate the data
python generate_data.py

# 4. Launch the dashboard
streamlit run dashboard.py
```

---

## Why This Project Matters

This project bridges two sides of my hybrid profile:
- **Industrial Engineering** — stock management, reorder points, rupture alerts
- **Data Science** — simulation, analysis, interactive visualization

---

## 👤 Author

**Yahya Abouredouane**
Master IMI — FSTS Settat
[LinkedIn](https://www.linkedin.com/in/yahya-abouredouane-v200420/) · [GitHub](https://github.com/ABOUREDOUANE-YAHYA)
