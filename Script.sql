-- ADMINISTRATION DE BASE DE DONNEES AVEC POSTGRESQL POUR L'AUTOMATISATION DE TACHE AVEC LE DECLENCHEUR DE TACHE SOUS WINDOWS

-- CREATION DE BASE DE DONNEES
CREATE DATABASE gestion_stock;

-- CREATION D'UN UTILISATEUR
CREATE USER gestionnaire_stock WITH PASSWORD "admin";

-- CREATION DES TABLES
CREATE TABLE produits (
id SERIAL PRIMARY KEY,
nom VARCHAR(100) NOT NULL,
description TEXT,
prix_unitaire NUMERIC(10, 2),
stock INT DEFAULT 0
);

CREATE TABLE fournisseurs (
id SERIAL PRIMARY KEY,
nom VARCHAR(50) NOT NULL,
contact VARCHAR(100)
);

CREATE TABLE entrees (
id SERIAL PRIMARY KEY,
produit_id INT REFERENCES produits(id),
fournisseurs_id INT REFERENCES fournisseurs(id),
quantite INT,
date_entree TIMESTAMP DEFAULT CURRENT_TIMESTAMP
 );

CREATE TABLE sorties (
id SERIAL PRIMARY KEY,
produit_id INT REFERENCES produits(id),
fournisseurs_id INT REFERENCES fournisseurs(id),
quantite INT,
date_sortie TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DROIT ET AUTORISATION

GRANT CONNECT ON DATABASE gestion_stock TO gestionnaire_stock;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA pubic TO gestionnaire_stock;
GRANT USAGE ON SCHEMA public TO gestionnaire_stock;

-- INSERTION DONNEES
INSERT INTO produits(nom, description, prix_unitaire, stock) VALUES ('Ordinateur', 'DELL portable', 250.000, 8);

INSERT INTO fournisseurs(nom, contact) VALUES ('Diop', 'diop@gmail.com');

INSERT INTO entrees (produit_id, fournisseurs_id, quantite, date_entree) VALUES(12, 42, 10, '2025-04-21');

INSERT INTO sorties (produit_id, fournisseurs_id, quantite, date_sortie) VALUES(12, 42, 10, '2025-04-21');

-- VOIR LE FICHIER insertion_stock_reel_massive.sql