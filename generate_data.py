import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

# --- PRODUITS ---
products = [
    {"id": "P001", "name": "Acide Sulfurique",      "category": "Chimique",    "unit": "Tonne",  "reorder_point": 50,  "max_stock": 500},
    {"id": "P002", "name": "Phosphate Brut",         "category": "Matière Première", "unit": "Tonne", "reorder_point": 200, "max_stock": 2000},
    {"id": "P003", "name": "Ammoniac",               "category": "Chimique",    "unit": "Tonne",  "reorder_point": 30,  "max_stock": 300},
    {"id": "P004", "name": "Pompe Industrielle",     "category": "Équipement",  "unit": "Unité",  "reorder_point": 5,   "max_stock": 50},
    {"id": "P005", "name": "Filtre à Presse",        "category": "Équipement",  "unit": "Unité",  "reorder_point": 10,  "max_stock": 80},
    {"id": "P006", "name": "Engrais DAP",            "category": "Produit Fini","unit": "Tonne",  "reorder_point": 100, "max_stock": 1000},
    {"id": "P007", "name": "Engrais MAP",            "category": "Produit Fini","unit": "Tonne",  "reorder_point": 100, "max_stock": 1000},
    {"id": "P008", "name": "Acide Phosphorique",     "category": "Chimique",    "unit": "Tonne",  "reorder_point": 40,  "max_stock": 400},
]

# --- FOURNISSEURS ---
suppliers = ["OCP Logistique", "Maghreb Chimie", "Atlas Équipements", "IndustroPro", "ChimTech Maroc"]

# --- GÉNÉRER LES MOUVEMENTS (2 ans) ---
start_date = datetime(2023, 1, 1)
end_date   = datetime(2024, 12, 31)
records    = []

for product in products:
    current_stock = random.randint(
        int(product["max_stock"] * 0.4),
        int(product["max_stock"] * 0.7)
    )

    current_date = start_date

    while current_date <= end_date:
        # Entrée (livraison) — 2x par semaine en moyenne
        if random.random() < 0.3:
            qty_in = random.randint(
                int(product["reorder_point"] * 0.5),
                int(product["max_stock"] * 0.3)
            )
            current_stock = min(current_stock + qty_in, product["max_stock"])
            records.append({
                "Date":          current_date.strftime("%Y-%m-%d"),
                "Product ID":    product["id"],
                "Product Name":  product["name"],
                "Category":      product["category"],
                "Unit":          product["unit"],
                "Movement Type": "Entrée",
                "Quantity":      qty_in,
                "Stock Level":   current_stock,
                "Reorder Point": product["reorder_point"],
                "Max Stock":     product["max_stock"],
                "Supplier":      random.choice(suppliers),
                "Alert":         "Rupture" if current_stock < product["reorder_point"] else "Normal"
            })

        # Sortie (consommation) — quotidienne
        qty_out = random.randint(
            int(product["reorder_point"] * 0.1),
            int(product["reorder_point"] * 0.8)
        )
        current_stock = max(current_stock - qty_out, 0)
        records.append({
            "Date":          current_date.strftime("%Y-%m-%d"),
            "Product ID":    product["id"],
            "Product Name":  product["name"],
            "Category":      product["category"],
            "Unit":          product["unit"],
            "Movement Type": "Sortie",
            "Quantity":      qty_out,
            "Stock Level":   current_stock,
            "Reorder Point": product["reorder_point"],
            "Max Stock":     product["max_stock"],
            "Supplier":      None,
            "Alert":         "Rupture" if current_stock < product["reorder_point"] else "Normal"
        })

        current_date += timedelta(days=1)

df = pd.DataFrame(records)
df.to_csv("ocp_stock_data.csv", index=False)
print(f"✅ Dataset généré : {len(df):,} lignes")
print(df.head(10))
print("\nAlertes rupture:", df[df["Alert"] == "Rupture"].shape[0])
print("Produits:", df["Product Name"].nunique())