# 🚀 Data & Image Analytics Hub

Bienvenue dans **Data & Image Analytics Hub** — une application web interactive pour l’analyse avancée des datasets et des images, avec **détection automatisée de types de variables**, **exploration statistique**, **Analyse en Composantes Principales (ACP/SVD)**, et **visualisation scientifique**.

🔗 **App en ligne :**  
👉 https://ganafaye-analytics-data.streamlit.app/

---

## 📌 Fonctionnalités Principales

### 📊 Analyse de Datasets

L’application analyse des données tabulaires pour :

- 👁️ Détecter automatiquement :
  - Types de variables (numérique / catégorique / datetime / texte)
  - Valeurs manquantes
  - Outliers (valeurs aberrantes)
- 📈 Fournir des métriques statistiques détaillées
- 🔍 Préparer les données pour l’ACP
- 🧠 Explorer les relations entre variables

📌 Exemple de formats supportés :  
`CSV`, `Excel`, `TSV`, etc.

---

### 🔬 Analyse d’Images et ACP

Pour les **images médicales ou standards** :

- 📥 Import de fichiers image
- 🧮 Décomposition matricielle SVD (ACP appliqué à l’image)
- 🔢 Choix du nombre de composantes principales
- 🖼 Reconstruction de l’image compressée
- 📊 Visualisation des résidus et histogrammes
- 📈 Indicateurs de qualité :
  - Variance expliquée
  - PSNR (Peak Signal-to-Noise Ratio)
  - Matrice différence

---

## 🧠 Principe Méthodologique

### 📊 ACP pour les datasets

L’Analyse en Composantes Principales transforme un jeu de variables potentiellement corrélées en un ensemble de composantes non corrélées :

\[
X_{centré} = X - \bar{X}
\]
\[
Z = X_{centré} \cdot V
\]

où \(Z\) est le jeu de données projeté sur les axes optimaux.

---

### 🧮 ACP sur Images via SVD

Pour une image représentée par une matrice \(X \in \mathbb{R}^{m \times n}\), l’ACP s’appuie sur :

\[
X = U \Sigma V^T
\]

et la reconstruction partielle :

\[
X_k = U_k \Sigma_k V_k^T
\]

Les premières composantes capturent l’essentiel de l’information (formes, structures), tandis que les dernières contiennent bruit et petits détails.

---

## 🛠️ Technologies Utilisées

| Catégorie | Stack |
|-----------|-------|
| Langage | Python 3 |
| Web App | Streamlit |
| Data | Pandas, NumPy |
| ML / DSP | Scikit-Learn, OpenCV |
| Visualisation | Plotly, Matplotlib |
| DevOps | GitHub Actions (CI) |
| Déploiement | Streamlit Community Cloud |

---

## 📂 Organisation du Répertoire
