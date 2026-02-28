import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="Data Intelligence Hub | Ganafaye",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. STYLE CSS AMÉLIORÉ (GLASSMORPHISM & MODERN ICONS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Header Principal */
    .main-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 2.5rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .main-header::after {
        content: '📡';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    /* Sidebar Stylisée */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-header {
        padding: 1.5rem;
        text-align: center;
        background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    /* Cards de Qualité */
    .quality-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 6px solid #6366f1;
        margin-bottom: 1rem;
        color: #1e293b;
    }

    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4);
    }
    </style>
""", unsafe_allow_html=True)


# 3. FONCTIONS DE TRAITEMENT (ANCIENNE MÉTHODE DATA SCIENCE)

def clean_qualitative(df):
    """Nettoyage des var qualitatives par la mode"""
    qual_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in qual_cols:
        if df[col].isnull().any():
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
    return df


def handle_outliers_iqr(df):
    """Gestion des outliers par Capping sur var numériques"""
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df[col] = df[col].clip(lower=lower, upper=upper)
    return df


def encode_and_scale(df):
    """Encodage Bool/Obj et Standardisation"""
    # 1. Encodage Booléen
    bool_cols = df.select_dtypes(include=['bool']).columns
    df[bool_cols] = df[bool_cols].astype(int)

    # 2. Label Encoding pour le reste des objets
    le = LabelEncoder()
    obj_cols = df.select_dtypes(include=['object']).columns
    for col in obj_cols:
        df[col] = le.fit_transform(df[col].astype(str))

    # 3. Scaling
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    return pd.DataFrame(scaled_data, columns=df.columns, index=df.index)


# 4. INTERFACE PRINCIPALE
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">💎 Data Intelligence Hub</h1>
        <p style="color: #94a3b8;">Analyse, Nettoyage et Préparation IA par Ganafaye</p>
    </div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="sidebar-header"><h3>⚙️ CONFIG</h3></div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📂 Charger votre Dataset", type=['csv', 'xlsx'])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)

    tab1, tab2, tab3 = st.tabs(["🔍 Exploration", "🛠️ Nettoyage Auto", "📈 Analyse ACP"])

    with tab1:
        st.subheader("📋 Aperçu des données brutes")
        st.dataframe(df_raw.head(10), use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Lignes", df_raw.shape[0])
        c2.metric("Colonnes", df_raw.shape[1])
        c3.metric("Valeurs Manquantes", df_raw.isna().sum().sum())

    with tab2:
        st.info("🚀 Lancement du pipeline de nettoyage : Mode (Qual) -> Capping (Quant) -> Encoding")

        # 1. Nettoyage
        df_cleaned = clean_qualitative(df_raw.copy())
        # Suppression spécifique demandée
        df_cleaned = df_cleaned.drop(columns=['weight_kg', 'height_cm'], errors='ignore')
        df_cleaned = handle_outliers_iqr(df_cleaned)

        st.success("✅ Valeurs manquantes et Outliers traités.")

        # Visualisation d'un boxplot après traitement
        num_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            col_to_plot = st.selectbox("Vérifier la distribution (Boxplot)", num_cols)
            fig = px.box(df_cleaned, y=col_to_plot, title=f"Distribution de {col_to_plot} après Capping")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🧪 Préparation pour l'ACP")

        if st.button("Lancer la Standardisation & ACP"):
            # Encodage et Scaling
            df_final = encode_and_scale(df_cleaned)

            # ACP
            pca = PCA()
            pca.fit(df_final)
            exp_var_cum = np.cumsum(pca.explained_variance_ratio_) * 100

            # Graphique de la variance
            fig_pca = go.Figure()
            fig_pca.add_trace(go.Scatter(y=exp_var_cum, mode='lines+markers', name="Variance Cumulée"))
            fig_pca.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Seuil 80%")

            fig_pca.update_layout(title="Graphique des Éboulis (Scree Plot)", xaxis_title="Composantes",
                                  yaxis_title="% Variance Expliquée")
            st.plotly_chart(fig_pca, use_container_width=True)

            st.write(
                f"💡 Pour garder 80% de l'information, vous avez besoin de **{np.argmax(exp_var_cum >= 80) + 1}** composantes.")

else:
    st.markdown("""
        <div style="text-align: center; padding: 5rem;">
            <h2 style="color: #64748b;">Veuillez importer un fichier dans la sidebar pour commencer l'analyse 🚀</h2>
        </div>
    """, unsafe_allow_html=True)

# 5. FOOTER
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>© 2026 Data Intelligence Hub | Built with ❤️ by Ganafaye</p>",
    unsafe_allow_html=True)