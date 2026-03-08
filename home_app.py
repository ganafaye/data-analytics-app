import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Data & Image Analytics Hub | Gana Faye",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS AVEC CARTES REDIMENSIONNÉES ---
st.markdown("""
    <style>
    /* Import des polices premium */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ===== PALETTE DE COULEURS HARMONISÉE ===== */
    :root {
        --primary: #4361ee;
        --primary-dark: #3a56d4;
        --primary-light: #6c8aff;
        --secondary: #7209b7;
        --secondary-light: #9d4edd;
        --accent: #f72585;
        --success: #4cc9f0;
        --warning: #f8961e;
        --dark: #1e293b;
        --gray-dark: #334155;
        --gray: #64748b;
        --gray-light: #94a3b8;
        --gray-lighter: #e2e8f0;
        --light: #f8fafc;
        --white: #ffffff;
        --gradient-primary: linear-gradient(135deg, #4361ee, #7209b7);
        --gradient-accent: linear-gradient(135deg, #f72585, #b5179e);
        --gradient-success: linear-gradient(135deg, #4cc9f0, #4895ef);
    }

    /* ===== MASQUAGE DES ÉLÉMENTS INDÉSIRABLES ===== */
    .css-1dp5vir, .css-1v3fvcr, .css-1v3fvcr a,
    section[data-testid="stSidebar"] .css-1v3fvcr,
    section[data-testid="stSidebar"] .st-emotion-cache-1v3fvcr,
    section[data-testid="stSidebar"] .st-emotion-cache-1dp5vir,
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"] ul,
    section[data-testid="stSidebar"] div[data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] .st-emotion-cache-1wrcr25 {
        display: none !important;
    }

    section[data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
    }

    /* ===== STYLE GÉNÉRAL ===== */
    .main {
        background: linear-gradient(135deg, #f1f5f9 0%, #e6edf5 100%);
        font-family: 'Inter', sans-serif;
    }

    /* ===== SIDEBAR HARMONISÉE ===== */
    section[data-testid="stSidebar"] {
        background: var(--white) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-right: 1px solid var(--gray-lighter);
        box-shadow: 5px 0 30px rgba(67, 97, 238, 0.05);
    }

    .sidebar-header {
        background: var(--gradient-primary);
        padding: 1.5rem 1.2rem;
        margin: -1rem -1rem 1.2rem -1rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .sidebar-header h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--white);
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .sidebar-section {
        background: var(--light);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        border: 1px solid var(--gray-lighter);
    }

    .sidebar-section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sidebar-item {
        padding: 0.4rem 0;
        color: var(--gray-dark);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.9rem;
    }

    /* ===== CARTES DES APPLICATIONS ===== */
    .app-card {
        background: var(--white);
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        border: 1px solid var(--gray-lighter);
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .app-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 3px; height: 100%;
        background: var(--gradient-primary);
    }

    .app-icon { font-size: 2.2rem; margin-bottom: 0.8rem; }
    .app-title { font-size: 1.3rem; font-weight: 700; color: var(--dark); font-family: 'Space Grotesk', sans-serif; }
    .app-description { color: var(--gray); font-size: 0.85rem; line-height: 1.5; }

    /* Hero Section */
    .hero-section {
        background: var(--white);
        padding: 2rem;
        border-radius: 30px;
        margin: 1rem 0 1.5rem 0;
        text-align: center;
        border: 1px solid var(--gray-lighter);
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Boutons */
    .stButton > button {
        background: var(--gradient-primary);
        color: var(--white);
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }

    header[data-testid="stHeader"] { background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR HARMONISÉE ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>🚀 Menu</h3>
            <p>Navigation et paramètres</p>
        </div>
    """, unsafe_allow_html=True)

    # Section Navigation
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title"><span>📍</span> Navigation</div>
            <div class="sidebar-item">🏠 Accueil</div>
            <div class="sidebar-item">📊 Data Quality Analyzer</div>
            <div class="sidebar-item">🔬 PCA Vision Pro</div>
            <div class="sidebar-item">🏙️ Dakar Rent AI</div>
        </div>
    """, unsafe_allow_html=True)

    # Section Applications
    st.markdown("""<div class="sidebar-section"><div class="sidebar-section-title"><span>🚀</span> Applications</div>""",
                unsafe_allow_html=True)

    if st.button("🏙️ Lancer Dakar Rent AI", use_container_width=True, key="sidebar_rent"):
        st.switch_page("pages/app_prediction_prix_loyer.py")

    if st.button("📊 Lancer Data Quality", use_container_width=True, key="sidebar_data"):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button("🔬 Lancer PCA Vision", use_container_width=True, key="sidebar_pca"):
        st.switch_page("pages/app_acp_v2.py")
    st.markdown("</div>", unsafe_allow_html=True)

    # Section Paramètres
    st.markdown("""<div class="sidebar-section"><div class="sidebar-section-title"><span>⚙️</span> Paramètres</div>""",
                unsafe_allow_html=True)
    st.selectbox("Thème", ["Clair", "Sombre"], key="sidebar_theme")
    st.checkbox("Notifications", value=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Section Informations
    st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-section-title"><span>ℹ️</span> Informations</div>
            <p style='font-size: 0.85rem;'><strong>Auteur:</strong> Gana Faye<br><strong>Version:</strong> 4.0</p>
        </div>
        <div class="sidebar-footer"><strong>Data & Image Hub</strong><br>© {datetime.now().year} Gana Faye</div>
    """, unsafe_allow_html=True)

# --- BANNIÈRE PRINCIPALE ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚀 Data & Image Analytics Hub</h1>
        <p class="hero-subtitle">La plateforme ultime pour l'analyse de données et la prédiction immobilière à Dakar</p>
    </div>
""", unsafe_allow_html=True)

# --- SECTION DES APPLICATIONS ---
st.markdown("## ✨ Nos Applications")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🏙️</div>
            <h2 class='app-title'>Dakar Rent AI</h2>
            <p class='app-description'>Estimation intelligente des loyers à Dakar basée sur le Machine Learning.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Lancer Dakar Rent AI", key="btn_rent", use_container_width=True):
        st.switch_page("pages/app_prediction_prix_loyer.py")

with col2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>📊</div>
            <h2 class='app-title'>Data Quality Analyzer</h2>
            <p class='app-description'>Analyse de la qualité des données et nettoyage automatique.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Lancer Data Quality", key="btn_data", use_container_width=True):
        st.switch_page("pages/analyse_data_traitement.py")

with col3:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🔬</div>
            <h2 class='app-title'>PCA Vision Pro</h2>
            <p class='app-description'>Analyse d'images par décomposition en composantes principales.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔬 Lancer PCA Vision Pro", key="btn_pca", use_container_width=True):
        st.switch_page("pages/app_acp_v2.py")

# --- SECTION RÉALISATEUR ---
st.markdown("""
    <div class='author-section' style='text-align:center; padding:2rem; background:white; border-radius:20px; border:1px solid #e2e8f0; margin-top:2rem;'>
        <h2>👨‍🎓 Gana Faye</h2>
        <p>Master 1 - Système d'Information | Data Scientist</p>
    </div>
""", unsafe_allow_html=True)