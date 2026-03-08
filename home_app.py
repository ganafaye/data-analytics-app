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

# --- STYLE CSS (Inchangé, incluant tes dégradés personnalisés) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

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
        --gradient-rent: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047);
        --gradient-dash: linear-gradient(135deg, #ff9a00, #ff5a00);
    }

    .main { background: linear-gradient(135deg, #f1f5f9 0%, #e6edf5 100%); font-family: 'Inter', sans-serif; }

    /* Style des cartes */
    .app-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .app-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(67, 97, 238, 0.1); border-color: var(--primary-light); }
    .app-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--gradient-primary); }
    .app-card-rent::before { background: var(--gradient-rent) !important; }
    .app-card-dash::before { background: var(--gradient-dash) !important; }

    .app-title { font-size: 1.3rem; font-weight: 700; color: var(--dark); margin-bottom: 0.5rem; font-family: 'Space Grotesk', sans-serif; }
    .app-icon { font-size: 2.5rem; margin-bottom: 1rem; }

    /* Masquage Header Streamlit */
    header[data-testid="stHeader"] { background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR RÉORGANISÉE ---
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h3>🚀 Menu</h3><p>Navigation Pro</p></div>', unsafe_allow_html=True)

    # Section IA
    st.markdown(
        '<div class="sidebar-section"><div class="sidebar-section-title"><span>🤖</span> Intelligence Artificielle</div>',
        unsafe_allow_html=True)
    if st.button("🏠 Dakar Immo AI", use_container_width=True): st.switch_page("pages/app_prediction_prix_loyer.py")
    if st.button("🔬 PCA Vision Pro", use_container_width=True): st.switch_page("pages/app_acp_v2.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Section Dashboards
    st.markdown(
        '<div class="sidebar-section"><div class="sidebar-section-title"><span>📊</span> Business Intelligence</div>',
        unsafe_allow_html=True)
    if st.button("📈 Dashboard Travaux", use_container_width=True): st.switch_page("pages/dashboard_v2.py")
    if st.button("🧼 Data Quality Analyzer", use_container_width=True): st.switch_page(
        "pages/analyse_data_traitement.py")
    st.markdown('</div>', unsafe_allow_html=True)

# --- BANNIÈRE PRINCIPALE ---
st.markdown("""
    <div class="hero-section" style="text-align: center; padding: 2rem; background: white; border-radius: 30px; border-bottom: 4px solid #4361ee;">
        <h1 class="hero-title" style="background: linear-gradient(135deg, #4361ee, #7209b7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem;">🚀 Gana's AI & Data HomeLab</h1>
        <p style="color: #64748b;">Master 1 Système d'Information - Espace d'innovation Data</p>
    </div>
""", unsafe_allow_html=True)

# --- SECTION 1 : INTELLIGENCE ARTIFICIELLE ---
st.markdown("### 🤖 Intelligence Artificielle & Modélisation")
col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    st.markdown("""
        <div class='app-card app-card-rent'>
            <div class='app-icon'>🏙️</div>
            <h2 class='app-title'>Dakar Immo AI</h2>
            <p class='app-description'>Prédiction des loyers à Dakar via <b>Random Forest (R² = 55%)</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer Dakar Immo", key="btn_ia_1"): st.switch_page("pages/app_prediction_prix_loyer.py")

with col_ia2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🔬</div>
            <h2 class='app-title'>PCA Vision Pro</h2>
            <p class='app-description'>Analyse d'images et réduction de dimensionnalité par composantes principales.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer PCA Vision", key="btn_ia_2"): st.switch_page("pages/app_acp_v2.py")

st.markdown("<br>", unsafe_allow_html=True)

# --- SECTION 2 : DASHBOARDS ET VISUALISATION ---
st.markdown("### 📊 Business Intelligence & Dashboards")
col_db1, col_db2 = st.columns(2)

with col_db1:
    st.markdown("""
        <div class='app-card app-card-dash'>
            <div class='app-icon'>📈</div>
            <h2 class='app-title'>Dashboard des Travaux</h2>
            <p class='app-description'>Suivi interactif des indicateurs clés (KPIs) et visualisation de données nettoyées.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Ouvrir le Dashboard", key="btn_db_1"): st.switch_page("pages/dashboard_v2.py")

with col_db2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🧼</div>
            <h2 class='app-title'>Data Quality Analyzer</h2>
            <p class='app-description'>Outil d'analyse exploratoire et de nettoyage automatique des fichiers CSV.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer l'Analyseur", key="btn_db_2"): st.switch_page("pages/analyse_data_traitement.py")

# --- STATISTIQUES ---
st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0;'>
        <div class='stat-card' style='text-align: center; background: white; padding: 1rem; border-radius: 15px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: #4361ee;'>4</div>
            <div style='font-size: 0.8rem; color: #64748b;'>Applications</div>
        </div>
        <div class='stat-card' style='text-align: center; background: white; padding: 1rem; border-radius: 15px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: #4361ee;'>Python 3.12</div>
            <div style='font-size: 0.8rem; color: #64748b;'>Moteur IA</div>
        </div>
        <div class='stat-card' style='text-align: center; background: white; padding: 1rem; border-radius: 15px;'>
            <div style='font-size: 1.5rem; font-weight: bold; color: #4361ee;'>2026</div>
            <div style='font-size: 0.8rem; color: #64748b;'>Année Master</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div style='text-align: center; color: #94a3b8; font-size: 0.8rem; margin-top: 2rem;'>
        © {datetime.now().year} Gana Faye - Data Scientist & AI Enthusiast
    </div>
""", unsafe_allow_html=True)