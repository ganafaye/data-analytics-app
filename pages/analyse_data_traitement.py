import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest
from scipy.stats import shapiro
import io
import re
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Gana's Data Lab | Master Informatique",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS (Ton design Glassmorphisme) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #9f7aea 100%); font-family: 'Inter', sans-serif; }

    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .quality-card {
        background: white;
        padding: 1.5rem;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        text-align: center;
        border-left: 5px solid #667eea;
    }

    .quality-score { font-size: 3rem; font-weight: 800; color: #764ba2; }

    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] { background: white; padding: 10px; border-radius: 50px; }
    </style>
""", unsafe_allow_html=True)


# --- FONCTIONS LOGIQUES ---

def charger_fichier(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    try:
        if ext == 'csv':
            return pd.read_csv(uploaded_file), None
        elif ext in ['xlsx', 'xls']:
            return pd.read_excel(uploaded_file), None
        return pd.read_csv(uploaded_file), None
    except Exception as e:
        return None, str(e)


def classifier_variables(df):
    quant = df.select_dtypes(include=[np.number]).columns.tolist()
    qual = df.select_dtypes(exclude=[np.number]).columns.tolist()
    return {'quantitative': quant, 'qualitative': qual}


def analyser_qualite_dataset(df):
    total_lignes = len(df)
    total_cells = df.size
    missing = df.isnull().sum().sum()
    dups = df.duplicated().sum()

    pct_missing = (missing / total_cells * 100) if total_cells > 0 else 0
    pct_dups = (dups / total_lignes * 100) if total_lignes > 0 else 0

    quality_score = max(0, 100 - (pct_missing * 2) - (pct_dups * 3))

    category = "EXCELLENT" if quality_score > 90 else "BON" if quality_score > 75 else "MOYEN" if quality_score > 50 else "FAIBLE"
    badge = "badge-excellent" if quality_score > 90 else "badge-good"

    return {
        'quality_score': quality_score,
        'category': category,
        'badge': badge,
        'missing': missing,
        'dups': dups
    }


def appliquer_nettoyage(df, options):
    df_c = df.copy()
    if options['std_names']:
        df_c.columns = [re.sub(r'\W+', '_', col.lower()).strip('_') for col in df_c.columns]
    if options['rm_dup']:
        df_c = df_c.drop_duplicates()
    if options['missing'] == "Supprimer":
        df_c = df_c.dropna()
    elif options['missing'] == "Imputer (Médiane/Mode)":
        for col in df_c.columns:
            if df_c[col].dtype in [np.float64, np.int64]:
                df_c[col] = df_c[col].fillna(df_c[col].median())
            else:
                df_c[col] = df_c[col].fillna(df_c[col].mode()[0] if not df_c[col].mode().empty else np.nan)
    if options['auto_encode']:
        for col in df_c.select_dtypes(include=['object']).columns:
            df_c[col] = df_c[col].astype('category').cat.codes
    return df_c


# --- INTERFACE PRINCIPALE ---

def main():
    st.markdown(
        '<div class="main-header"><h1 class="main-title">Gana\'s Data Lab</h1><p>Analyse de Qualité & Pré-traitement de Données</p></div>',
        unsafe_allow_html=True)

    with st.sidebar:
        st.header("📁 Importation")
        uploaded_file = st.file_uploader("Fichier CSV ou Excel", type=['csv', 'xlsx'])

        if uploaded_file:
            st.markdown("---")
            st.header("🛠️ Options de Nettoyage")
            std_names = st.checkbox("Standardiser noms", value=True)
            rm_dup = st.checkbox("Supprimer doublons", value=True)
            missing_strat = st.selectbox("Valeurs manquantes", ["Garder", "Supprimer", "Imputer (Médiane/Mode)"])
            auto_encode = st.checkbox("Encodage ML", value=False)

            options = {
                'std_names': std_names, 'rm_dup': rm_dup,
                'missing': missing_strat, 'auto_encode': auto_encode
            }

            if st.button("🚀 Appliquer le Traitement", use_container_width=True):
                st.session_state['processed'] = True

    if uploaded_file:
        if 'df_init' not in st.session_state:
            df, err = charger_fichier(uploaded_file)
            st.session_state['df_init'] = df

        df_active = st.session_state['df_init']

        if st.session_state.get('processed', False):
            df_active = appliquer_nettoyage(st.session_state['df_init'], options)
            st.session_state['df_final'] = df_active

        # Dashboard de Qualité
        stats = analyser_qualite_dataset(df_active)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f'<div class="quality-card"><div class="quality-score">{stats["quality_score"]:.0f}%</div><div>Score Qualité</div></div>',
                unsafe_allow_html=True)
        with col2:
            st.metric("Lignes", len(df_active))
        with col3:
            st.metric("Doublons", stats['dups'])
        with col4:
            st.metric("Catégorie", stats['category'])

        # Onglets d'analyse
        tab1, tab2, tab3 = st.tabs(["🔍 Inspection", "🧪 Analyse Avancée", "📤 Export"])

        with tab1:
            st.dataframe(df_active.head(100), use_container_width=True)
            st.write("**Statistiques Descriptives**")
            st.dataframe(df_active.describe(), use_container_width=True)

        with tab2:
            st.subheader("Analyse Statistique de Master")
            c_a, c_b = st.columns(2)

            with c_a:
                st.write("**🔥 Matrice de Corrélation**")


[Image of correlation matrix heatmap]

df_num = df_active.select_dtypes(include=[np.number])
if not df_num.empty:
    fig_corr = px.imshow(df_num.corr(), text_auto='.2f', color_continuous_scale='RdBu_r')
    st.plotly_chart(fig_corr, use_container_width=True)

with c_b:
    st.write("**📊 Test de Normalité (Shapiro)**")
    if not df_num.empty:
        target_col = st.selectbox("Sélectionner une variable :", df_num.columns)
        stat, p = shapiro(df_num[target_col].dropna())
        st.write(f"P-Value : `{p:.4f}`")
        if p > 0.05:
            st.success("Distribution Normale")
        else:
            st.error("Distribution non-normale")

st.markdown("---")
st.write("**🤖 Détection d'Anomalies (Isolation Forest)**")
if len(df_num) > 10:
    iso = IsolationForest(contamination=0.05, random_state=42)
    preds = iso.fit_predict(df_num.fillna(0))
    nb_outliers = (preds == -1).sum()
    st.warning(f"Algorithme : {nb_outliers} anomalies multivariées détectées.")

with tab3:
    st.subheader("Téléchargement")
    csv = df_active.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger le CSV Nettoyé", data=csv, file_name="gana_lab_cleaned.csv", mime="text/csv",
                       use_container_width=True)

else:
st.info("👋 Bienvenue Gana ! Charge un fichier pour commencer l'analyse.")

if __name__ == "__main__":
    main()