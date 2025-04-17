# -*- coding: utf-8 -*-


import pandas as pd
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import psycopg2
import os


from sqlalchemy import create_engine  
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

EMAIL_DESTINATION = os.getenv("EMAIL_DESTINATION").strip("[]").replace("'", "").split(",")
EMAIL_ADDRESS = os.getenv("EMAIL_ADRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

#requete qui permet de renvoyer le stock inferieur a 10
#df = pd.read_sql("SELECT id, nom, prix_unitaire, stock FROM produits WHERE stock < 10 ORDER BY id", engine)

#df = pd.read_sql ("SELECT p.id, p.nom, p.prix_unitaire, p.stock, e.quantite AS quantite_entrees, s.quantite AS quantite_sortie FROM produits p, entrees e, sorties s WHERE p.id = e.produit_id AND p.id = s.produit_id AND (e.quantite_entrees - s.quantite_sortie) AS difference AND p.stock < 10 ORDER BY p.id", engine)

df = pd.read_sql("""
    SELECT 
        p.id, 
        p.nom, 
        p.prix_unitaire, 
        p.stock AS stock_initial, 
        e.quantite AS quantite_entrees, 
        s.quantite AS quantite_sortie,
        (e.quantite - s.quantite) AS difference
    FROM produits p
    JOIN entrees e ON p.id = e.produit_id
    JOIN sorties s ON p.id = s.produit_id
    
    ORDER BY p.id
""", engine)
df.to_csv("rapport_stock.csv", index=False)

# Email

msg = EmailMessage()
msg['Subject'] = 'RAPPORT JOURNALIER DE STOCK'
msg['From'] = EMAIL_ADDRESS
msg['To'] = ',' .join(EMAIL_DESTINATION)
msg.set_content("Veuillez trouver ci-joint le rapport du jour. CECI EST UN ESSAI D'UN PROJET A NE PAS PRENDRE EN COMPTE.")
with open("rapport_stock.csv", "rb") as f:
    msg.add_attachment(f.read(), maintype='application', subtype='csv', filename="rapport_stock.csv")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
