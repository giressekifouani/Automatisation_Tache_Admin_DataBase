# -*- coding: utf-8 -*-

import psycopg2
from datetime import datetime

# Paramètres de connexion PostgreSQL
conn = psycopg2.connect(
    dbname="gestion_stock",
    user="postgres",
    password="admin123",
    host="localhost",
    port="5432"
)

# Création du curseur
cur = conn.cursor()

# Requête SQL pour les produits à faible stock
seuil_stock = 5
cur.execute("""
    SELECT nom, stock
    FROM produits
    WHERE stock < %s
""", (seuil_stock,))

# Résultats
produits_faibles = cur.fetchall()

# Affichage ou traitement
if produits_faibles:
    print(f"\n[{datetime.now()}] 🔴 Alerte - Stock faible :")
    for produit in produits_faibles:
        print(f" - {produit[0]} → {produit[1]} en stock")
else:
    print(f"\n[{datetime.now()}] ✅ Tout est OK. Pas de stock faible.")

# Fermeture
cur.close()
conn.close()
