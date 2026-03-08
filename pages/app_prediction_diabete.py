import streamlit as st
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import shap
from datetime import datetime
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Diabète Predict Pro | Gana Faye",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)
local_css()
# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8fafc; }
    .form-container, .results-container, .upload-container {
        background: white; border-radius: 20px; padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02); border: 1px solid #e2e8f0;
    }
    .section-header {
        font-size: 1.1rem; font-weight: 600; color: #1e293b;
        margin-bottom: 1.5rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0;
    }
    .risk-badge { display: inline-block; padding: 0.3rem 1rem; border-radius: 30px; font-size: 0.8rem; font-weight: 600; }
    .risk-high { background: #fee2e2; color: #dc2626; }
    .risk-medium { background: #fef3c7; color: #d97706; }
    .risk-low { background: #dcfce7; color: #16a34a; }
    .metric-card { background: #f8fafc; border-radius: 12px; padding: 1rem; text-align: center; border: 1px solid #e2e8f0; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #1e293b; }
    
     /* 1. On garde le header mais on le rend invisible (transparent) */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: transparent !important;
    }

    /* 2. On masque spécifiquement les boutons de droite (Deploy, Menu, etc.) */
    header[data-testid="stHeader"] div:first-child > div:nth-child(2) {
        display: none !important;
    }

    /* 3. On s'assure que le bouton de la sidebar reste visible et blanc/couleur voulue */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important; /* Change en 'black' si ton fond est clair */
    }

    /* 4. On réduit la marge pour que le contenu remonte */
    .main .block-container {
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- CHARGEMENT DES MODÈLES AVEC CORRECTIFS ---
@st.cache_resource
def load_models():
    try:
        # Utilisation de chemins relatifs pour la portabilité
        base_path = os.path.dirname(__file__)
        model_path = os.path.join(base_path, "../models/model.pkl")
        scaler_path = os.path.join(base_path, "../models/scaler.pkl")

        # Secours si les chemins relatifs échouent (ton chemin local spécifique)
        if not os.path.exists(model_path):
            model_path = "/home/gana-faye/Bureau/Python_IA/TP_ML/TP_ML_RegressionLinéaire/TP_Predict_Diabet_V1/models/model.pkl"
            scaler_path = "/home/gana-faye/Bureau/Python_IA/TP_ML/TP_ML_RegressionLinéaire/TP_Predict_Diabet_V1/models/scaler.pkl"

        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        # ✅ PATCH : Correction de l'erreur 'multi_class' pour Scikit-learn 1.6+
        if not hasattr(model, 'multi_class'):
            model.multi_class = 'auto'

        # Initialisation de SHAP (Linear ou Kernel selon le modèle)
        try:
            # On utilise une petite référence neutre (médiane ou zéros)
            X_ref = np.zeros((1, 8))
            explainer = shap.Explainer(model.predict, X_ref)
        except:
            explainer = None

        return model, scaler, explainer
    except Exception as e:
        st.error(f"Erreur critique de chargement : {e}")
        return None, None, None


model, scaler, explainer = load_models()
feature_names = ['Grossesses', 'Glucose', 'Pression', 'Pli cutané', 'Insuline', 'IMC', 'Indice héréditaire', 'Âge']

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/stethoscope.png", width=80)
    st.markdown("## 🏥 Diabète Predict Pro")
    st.markdown("---")
    st.markdown("### 📊 Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Précision", "87%")
    with col2:
        st.metric("AUC-ROC", "0.92")
    st.markdown("---")
    st.caption(f"Sync: {datetime.now().strftime('%d/%m/%Y')}")

# --- TABS PRINCIPAUX ---
tab1, tab2 = st.tabs(["📋 Diagnostic Individuel", "📂 Analyse de Groupe (CSV)"])

with tab1:
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📝 Paramètres Cliniques</div>', unsafe_allow_html=True)

        with st.expander("👤 Profil Patient", expanded=True):
            c1, c2 = st.columns(2)
            preg = c1.number_input("Grossesses", 0, 20, 0)
            age = c2.number_input("Âge", 1, 120, 30)

        with st.expander("🧪 Analyses Biologiques", expanded=True):
            gluc = st.number_input("Glycémie (mg/dL)", 0, 300, 100)
            insu = st.number_input("Insuline (μU/ml)", 0, 900, 80)
            bmi = st.number_input("IMC (kg/m²)", 0.0, 70.0, 25.0)
            pres = st.number_input("Tension Diastolique", 0, 200, 70)
            skin = st.number_input("Pli cutané (mm)", 0, 100, 20)
            pedi = st.number_input("Indice Héréditaire", 0.0, 3.0, 0.5)

        analyze_btn = st.button("🔬 ANALYSER LE RISQUE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">📊 Résultats de l\'Analyse</div>', unsafe_allow_html=True)

        if analyze_btn and model:
            # Préparation des données
            raw_data = np.array([[preg, gluc, pres, skin, insu, bmi, pedi, age]])
            data_scaled = scaler.transform(raw_data)

            # Prédiction
            prob = model.predict_proba(data_scaled)[0][1] * 100

            # Jauge Plotly
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=prob,
                gauge={'axis': {'range': [0, 100]},
                       'bar': {'color': "#2563eb"},
                       'steps': [{'range': [0, 33], 'color': "#dcfce7"},
                                 {'range': [33, 66], 'color': "#fef3c7"},
                                 {'range': [66, 100], 'color': "#fee2e2"}]},
                title={'text': "Niveau de Risque (%)"}
            ))
            fig.update_layout(height=250, margin=dict(t=30, b=0))
            st.plotly_chart(fig, use_container_width=True)

            # Facteurs d'influence (Importance locale)
            st.markdown("### 🧠 Explication du Score (SHAP)")
            if explainer:
                shap_vals = explainer(data_scaled)
                # Affichage simplifié des impacts
                impact_df = pd.DataFrame({
                    'Variable': feature_names,
                    'Impact': shap_vals.values[0]
                }).sort_values(by='Impact', ascending=False)

                for _, row in impact_df.iterrows():
                    icon = "🔺" if row['Impact'] > 0 else "🔹"
                    st.write(f"{icon} **{row['Variable']}** : {row['Impact']:.3f}")

            # Recommandation
            if prob > 66:
                st.error("🚨 Risque élevé : Consultation spécialisée requise.")
            elif prob > 33:
                st.warning("⚠️ Risque modéré : Surveillance glycémique conseillée.")
            else:
                st.success("✅ Risque faible : Maintenir une hygiène de vie saine.")
        else:
            st.info("En attente de saisie des données patient...")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📂 Traitement par Lot</div>', unsafe_allow_html=True)

    file = st.file_uploader("Charger un fichier CSV", type="csv")
    if file and model:
        df = pd.read_csv(file)
        # On suppose que le CSV suit l'ordre des features
        X_batch = scaler.transform(df)
        df['Probabilité (%)'] = (model.predict_proba(X_batch)[:, 1] * 100).round(2)
        df['Diagnostic'] = np.where(df['Probabilité (%)'] > 50, "Positif", "Négatif")

        st.dataframe(df.style.background_gradient(subset=['Probabilité (%)'], cmap='Reds'), use_container_width=True)

        # Export
        st.download_button("📥 Télécharger les résultats", df.to_csv(index=False), "resultats_diabete.csv")
    st.markdown('</div>', unsafe_allow_html=True)