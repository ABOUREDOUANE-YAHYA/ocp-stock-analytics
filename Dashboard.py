import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="OCP Stock Dashboard", layout="wide", page_icon="")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FC; }
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #E8ECF0;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: 600; color: #1A1A2E; }
    [data-testid="stMetricLabel"] { font-size: 13px; color: #6B7280; font-weight: 500; }
    [data-testid="stSidebar"] { background-color: #1A1A2E; }
    [data-testid="stSidebar"] * { color: white !important; }
    hr { border-color: #E8ECF0; }
    </style>
""", unsafe_allow_html=True)

# --- LOAD ---
@st.cache_data
def load_data():
    df = pd.read_csv("ocp_stock_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Month_dt"] = pd.to_datetime(df["Month"])
    return df

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("Filtres")

selected_categories = st.sidebar.multiselect(
    "Catégorie", options=sorted(df["Category"].unique()), default=[]
)
selected_products = st.sidebar.multiselect(
    "Produit", options=sorted(df["Product Name"].unique()), default=[]
)
selected_movements = st.sidebar.multiselect(
    "Type de mouvement", options=["Entrée", "Sortie"], default=[]
)

date_min = df["Date"].min().date()
date_max = df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Période", value=(date_min, date_max),
    min_value=date_min, max_value=date_max
)

if st.sidebar.button("🔄 Reset"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption(f"{len(df):,} mouvements au total")

# --- FILTRES ---
filtered = df.copy()
if selected_categories:
    filtered = filtered[filtered["Category"].isin(selected_categories)]
if selected_products:
    filtered = filtered[filtered["Product Name"].isin(selected_products)]
if selected_movements:
    filtered = filtered[filtered["Movement Type"].isin(selected_movements)]
if len(date_range) == 2:
    filtered = filtered[
        (filtered["Date"].dt.date >= date_range[0]) &
        (filtered["Date"].dt.date <= date_range[1])
    ]

if len(filtered) == 0:
    st.warning("Aucun résultat pour ces filtres.")
    st.stop()

# --- HEADER ---
st.title("OCP — Dashboard Gestion de Stock")
st.caption(f"Période : {filtered['Date'].min().date()} → {filtered['Date'].max().date()} · {len(filtered):,} mouvements")

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)

total_entrees = filtered[filtered["Movement Type"] == "Entrée"]["Quantity"].sum()
total_sorties = filtered[filtered["Movement Type"] == "Sortie"]["Quantity"].sum()
alertes      = filtered[filtered["Alert"] == "Rupture"].shape[0]
taux_alerte  = alertes / len(filtered) * 100

col1.metric("Total Entrées",      f"{total_entrees:,.0f}")
col2.metric("Total Sorties",      f"{total_sorties:,.0f}")
col3.metric("Alertes Rupture",    f"{alertes:,}")
col4.metric("Taux d'Alerte",      f"{taux_alerte:.1f}%")

st.markdown("---")

# --- ROW 1: Evolution stock + Alertes par produit ---
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Évolution du Niveau de Stock")
    # Un produit par ligne, groupé par mois
    stock_trend = (
        filtered.groupby(["Month", "Product Name"])["Stock Level"]
        .mean().reset_index()
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    for product in stock_trend["Product Name"].unique():
        subset = stock_trend[stock_trend["Product Name"] == product]
        ax.plot(subset["Month"], subset["Stock Level"], marker="o",
                markersize=3, linewidth=1.5, label=product)
    ax.set_xticks(stock_trend["Month"].unique()[::2])
    ax.set_xticklabels(stock_trend["Month"].unique()[::2], rotation=45, fontsize=8)
    ax.set_ylabel("Niveau moyen de stock")
    ax.legend(fontsize=7, loc="upper right")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)

with col_b:
    st.subheader("Alertes de Rupture par Produit")
    alertes_prod = (
        filtered[filtered["Alert"] == "Rupture"]
        .groupby("Product Name")
        .size().sort_values(ascending=False).reset_index()
    )
    alertes_prod.columns = ["Produit", "Nombre d'alertes"]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(alertes_prod["Produit"], alertes_prod["Nombre d'alertes"],
            color="#E24B4A")
    ax.invert_yaxis()
    ax.set_xlabel("Nombre d'alertes")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# --- ROW 2: Entrées vs Sorties + Stock par catégorie ---
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Entrées vs Sorties par Mois")
    mv_monthly = (
        filtered.groupby(["Month", "Movement Type"])["Quantity"]
        .sum().reset_index()
    )
    entrees = mv_monthly[mv_monthly["Movement Type"] == "Entrée"]
    sorties = mv_monthly[mv_monthly["Movement Type"] == "Sortie"]
    months  = sorted(mv_monthly["Month"].unique())
    x = range(len(months))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - width/2 for i in x],
           [entrees[entrees["Month"] == m]["Quantity"].sum() for m in months],
           width, label="Entrées", color="#1D9E75")
    ax.bar([i + width/2 for i in x],
           [sorties[sorties["Month"] == m]["Quantity"].sum() for m in months],
           width, label="Sorties", color="#E24B4A")
    ax.set_xticks(list(x))
    ax.set_xticklabels(months, rotation=45, fontsize=8)
    ax.set_ylabel("Quantité")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)

with col_d:
    st.subheader("Niveau de Stock Moyen par Catégorie")
    cat_stock = (
        filtered.groupby("Category")["Stock Level"]
        .mean().sort_values(ascending=False).reset_index()
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(cat_stock["Category"], cat_stock["Stock Level"],
           color=["#378ADD", "#7F77DD", "#1D9E75", "#E24B4A"])
    ax.set_ylabel("Niveau moyen de stock")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    st.pyplot(fig)

st.markdown("---")

# --- TABLE ALERTES RÉCENTES ---
st.subheader("Dernières Alertes de Rupture")
recent_alerts = (
    filtered[filtered["Alert"] == "Rupture"]
    [["Date", "Product Name", "Category", "Stock Level", "Reorder Point", "Movement Type"]]
    .sort_values("Date", ascending=False)
    .head(10)
)
st.dataframe(recent_alerts, use_container_width=True)

st.markdown("---")
st.caption("Built by Yahya Abouredouane · OCP Stock Analytics — Portfolio Project")
