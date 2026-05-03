# Agent Délibérations IA — Guide de démarrage

## Prérequis

- Python 3.9+ installé sur ton ordinateur
- Une clé API Anthropic (gratuite au départ) → https://console.anthropic.com

## Installation (une seule fois)

Ouvre un terminal dans ce dossier et tape :

```bash
pip install -r requirements.txt
```

## Lancer l'agent

```bash
python app.py
```

Puis ouvre ton navigateur sur : **http://localhost:5000**

## Utilisation

1. Entre ta clé API Anthropic dans le champ en haut du formulaire
2. Remplis les informations de la délibération (ou utilise un exemple rapide)
3. Clique sur "Générer la délibération"
4. Copie ou télécharge le résultat

## Pour aller plus loin

Ce prototype est la base. Les évolutions possibles :
- Connexion à une base de données de délibérations existantes pour améliorer la précision
- Déploiement en ligne (Heroku, Railway, VPS) pour partager l'outil sans installation
- Interface multi-utilisateurs avec authentification
- Génération en format Word (.docx) directement
