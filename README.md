
# 🚀 Gana's Datalab : Data & Real Estate Analytics Hub

Bienvenue dans **Gana's Datalab** — une plateforme analytique avancée conçue pour l'exploration de données, l'analyse d'images via SVD, et l'étude prédictive du marché immobilier à Dakar.

🔗 **Accès Live :** [https://ganafaye-analytics-data.streamlit.app/](https://ganafaye-analytics-data.streamlit.app/)

---

## 🛡️ Nouveauté : Sécurité & UI Premium

L'application intègre désormais un système d'authentification sécurisé et une interface **Glassmorphism** moderne :

* **Contrôle d'accès :** Restriction par Whitelist d'emails (via Streamlit Secrets).
* **Interface Intuitive :** Sidebar personnalisée avec menu de connexion escamotable (Popover).
* **Indicateurs d'état :** Badge de session active avec monitoring "Live" (🟢).

---

## 📌 Fonctionnalités Clés

### 🏙️ Analyse Immobilière (Dakar)

Module dédié à l'étude du marché local sénégalais :

* **Nettoyage Avancé :** Traitement des valeurs aberrantes (ex: loyers plafonnés à 2M FCFA).
* **Exploration Statistique :** Visualisation des prix par quartier (Almadies, Plateau, Mamelles, etc.).
* **Modélisation Prédictive :** Estimation des prix via algorithmes **Random Forest** et **KNN**.

### 📊 Analyse de Datasets (Général)

* **Auto-Détection :** Identification intelligente des types (Numérique, Catégorique, Datetime).
* **Qualité des Données :** Rapport sur les valeurs manquantes et distribution.
* **Visualisation Scientifique :** Heatmaps de corrélation et graphiques interactifs Plotly.

### 🔬 Traitement d'Images & SVD

Utilisation de la Décomposition en Valeurs Singulières (SVD) pour la compression :

* **Reconstruction Matricielle :** $X_k = U_k \Sigma_k V_k^T$.
* **Métriques de Qualité :** Calcul de la variance expliquée et du **PSNR**.
* **Analyse des Résidus :** Comparaison entre image originale et compressée.

---

## 🛠️ Stack Technique

| Domaine | Technologie |
| --- | --- |
| **Framework Web** | Streamlit (Python) |
| **Data Science** | Pandas, NumPy, Scikit-Learn |
| **Visualisation** | Plotly, Matplotlib, Seaborn |
| **Image Processing** | OpenCV |
| **Sécurité** | Streamlit Secrets (TOML) |
| **DevOps** | GitHub Actions (CI/CD) |

---

## 📂 Architecture du Projet

```text
├── home_app.py              # Point d'entrée principal (Datalab)
├── auth_utils.py            # Module de sécurité & UI Glassmorphism
├── pages/
│   ├── dakar_immo.py        # Analyse immobilière Dakar
│   ├── analyse_traitement.py # Exploration de datasets
│   └── app_acp_v2.py        # SVD & Compression d'images
├── requirements.txt         # Dépendances Python
└── README.md                # Documentation

```

---

## 🚀 Installation & Test Local

1. **Clonage :**
```bash
git clone https://github.com/ganafaye/data-analytics-app.git
cd data-analytics-app

```


2. **Configuration des secrets (Optionnel pour test local) :**



3. **Lancement :**
```bash
streamlit run home_app.py

```



---

## 📄 Auteur

**Gana Faye** *Master en Informatique* Expert en Data Engineering & Systèmes d'Information

📍 Dakar, Sénégal

---
