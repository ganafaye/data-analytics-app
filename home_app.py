import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from auth_utils import apply_custom_style, is_authorized, login_sidebar

apply_custom_style()

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Gana's AI & Data HomeLab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS MODERNE ET ÉPURÉ ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    /* ===== VARIABLES ===== */
    :root {
        --primary: #4361ee;
        --primary-dark: #3a56d4;
        --secondary: #7209b7;
        --accent: #f72585;
        --success: #4cc9f0;
        --warning: #f8961e;
        --dark: #0f172a;
        --gray-dark: #334155;
        --gray: #64748b;
        --gray-light: #94a3b8;
        --gray-lighter: #e2e8f0;
        --light: #f8fafc;
        --white: #ffffff;
    }

    /* ===== STYLE GLOBAL ===== */
    .stApp {
        background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: var(--white) !important;
        border-right: 1px solid var(--gray-lighter);
        box-shadow: 2px 0 20px rgba(0,0,0,0.02);
    }

    .sidebar-profile {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        padding: 2rem 1rem;
        margin: -1rem -1rem 1rem -1rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .sidebar-profile::after {
        content: '⚡';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 6rem;
        opacity: 0.1;
        transform: rotate(-15deg);
    }

    .sidebar-avatar {
        width: 80px;
        height: 80px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 1rem;
        font-size: 2.5rem;
        border: 3px solid rgba(255,255,255,0.3);
    }

    .sidebar-profile h3 {
        color: var(--white);
        font-weight: 600;
        margin: 0;
        font-size: 1.3rem;
    }

    .sidebar-profile p {
        color: rgba(255,255,255,0.8);
        font-size: 0.8rem;
        margin: 0.2rem 0 0;
    }

    .sidebar-section {
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    .sidebar-section-title {
        font-weight: 600;
        color: var(--dark);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sidebar-section-title span {
        background: var(--primary);
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
    }

    .nav-item {
        padding: 0.6rem 1rem;
        margin: 0.2rem 0;
        border-radius: 12px;
        color: var(--gray-dark);
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        transition: all 0.2s;
        cursor: pointer;
    }

    .nav-item:hover {
        background: var(--light);
        color: var(--primary);
        transform: translateX(5px);
    }

    .nav-item.active {
        background: linear-gradient(135deg, var(--primary)10, var(--secondary)10);
        color: var(--primary);
        font-weight: 500;
        border-left: 3px solid var(--primary);
    }

    /* ===== HEADER PRINCIPAL ===== */
    .hero-section {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        padding: 2.5rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '⚡';
        position: absolute;
        right: 20px;
        bottom: -20px;
        font-size: 10rem;
        opacity: 0.1;
        transform: rotate(10deg);
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 1.5rem;
    }

    .tech-stack {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
    }

    .tech-badge {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        color: white;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* ===== STATS CARDS ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px var(--primary)30;
        border-color: var(--primary);
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
    }

    .stat-label {
        color: var(--gray);
        font-size: 0.85rem;
        text-transform: uppercase;
        margin-top: 0.3rem;
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem;
    }

    .section-icon {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }

    .section-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--dark);
        flex-grow: 1;
    }

    .section-count {
        background: var(--light);
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        color: var(--primary);
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid var(--gray-lighter);
    }

    /* ===== CARDS APPLICATIONS ===== */
    .app-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
        margin-bottom: 1rem;
    }

    .app-card {
        background: white;
        padding: 1.5rem;
        border-radius: 24px;
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 40px -20px var(--primary)40;
        border-color: var(--primary);
    }

    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 0;
        background: linear-gradient(to bottom, var(--primary), var(--secondary));
        transition: height 0.3s;
    }

    .app-card:hover::before {
        height: 100%;
    }

    .app-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, var(--primary)10, var(--secondary)10);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin-bottom: 1rem;
        color: var(--primary);
    }

    .app-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 0.5rem;
    }

    .app-description {
        color: var(--gray);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }

    .app-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin-bottom: 1rem;
    }

    .app-tag {
        background: var(--light);
        padding: 0.2rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--gray-dark);
    }

    .app-tag.primary { background: var(--primary)10; color: var(--primary); }
    .app-tag.success { background: #10b98110; color: #10b981; }
    .app-tag.warning { background: #f59e0b10; color: #f59e0b; }

    /* ===== DASHBOARD CARDS ===== */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1.5rem;
    }

    .dashboard-card {
        background: linear-gradient(135deg, #ffffff, #fef9e7);
        padding: 1.5rem;
        border-radius: 24px;
        border: 1px solid #fed7aa;
        transition: all 0.3s;
    }

    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 40px -20px #f59e0b40;
        border-color: #f59e0b;
    }

    .dashboard-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .dashboard-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #92400e;
        margin-bottom: 0.5rem;
    }

    .dashboard-tags {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }

    .dashboard-tag {
        background: #fef3c7;
        color: #92400e;
        padding: 0.2rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 500;
    }

    /* ===== AUTHOR SECTION ===== */
    .author-section {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        padding: 2rem;
        border-radius: 30px;
        margin: 2rem 0;
        color: white;
        display: flex;
        align-items: center;
        gap: 2rem;
        position: relative;
        overflow: hidden;
    }

    .author-section::before {
        content: '👨‍🎓';
        position: absolute;
        right: 20px;
        bottom: -20px;
        font-size: 8rem;
        opacity: 0.1;
        transform: rotate(-10deg);
    }

    .author-avatar {
        width: 120px;
        height: 120px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3.5rem;
        border: 4px solid rgba(255,255,255,0.3);
    }

    .author-info {
        flex: 1;
    }

    .author-name {
        font-size: 2rem;
        font-weight: 700;
        margin: 0 0 0.2rem;
    }

    .author-title {
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }

    .author-tags {
        display: flex;
        gap: 0.8rem;
        flex-wrap: wrap;
    }

    .author-tag {
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.85rem;
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 14px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.3s;
        width: 100%;
        box-shadow: 0 4px 15px var(--primary)30;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px var(--primary)50;
    }

    .btn-outline > button {
        background: transparent;
        border: 2px solid var(--primary);
        color: var(--primary);
        box-shadow: none;
    }

    .btn-outline > button:hover {
        background: var(--primary);
        color: white;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 2rem;
        color: var(--gray);
        font-size: 0.9rem;
        border-top: 1px solid var(--gray-lighter);
        margin-top: 3rem;
        background: white;
        border-radius: 30px 30px 0 0;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .app-grid { grid-template-columns: 1fr; }
        .dashboard-grid { grid-template-columns: 1fr; }
        .author-section { flex-direction: column; text-align: center; }
        .hero-title { font-size: 2rem; }
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
    /* 1. Cibler le bouton de la Sidebar (Ouverture/Fermeture) */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        width: 45px !important;
        height: 45px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        margin-left: 10px !important;
        margin-top: 5px !important;
    }

    /* 2. Effet au survol (Hover) */
    button[data-testid="stBaseButton-headerNoPadding"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid #60a5fa !important;
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.4) !important;
    }

    /* 3. Style de l'icône à l'intérieur du bouton */
    button[data-testid="stBaseButton-headerNoPadding"] svg {
        fill: white !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* 4. Ajustement pour que l'icône reste visible */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* 5. Animation d'apparition douce */
    @keyframes fadeInIcon {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    button[data-testid="stBaseButton-headerNoPadding"] {
        animation: fadeInIcon 0.8s ease-out;
    }
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
# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class='sidebar-profile'>
            <div class='sidebar-avatar'>⚡</div>
            <h3>Gana Faye</h3>
            <p>Data Scientist • ML Engineer</p>
        </div>
    """, unsafe_allow_html=True)

    login_sidebar()

    st.markdown("""
        <div class='sidebar-section'>
            <div class='sidebar-section-title'>
                <span>🏠</span> NAVIGATION
            </div>
            <div class='nav-item active'>
                <span>📊</span> Dashboard
            </div>
            <div class='nav-item'>
                <span>📈</span> Analytics
            </div>
            <div class='nav-item'>
                <span>🤖</span> ML Models
            </div>
        </div>

        <div class='sidebar-section'>
            <div class='sidebar-section-title'>
                <span>📌</span> RACCOURCIS
            </div>
    """, unsafe_allow_html=True)

    if st.button("🏙️ Dakar Immo AI", use_container_width=True, key="sidebar_rent"):
        if is_authorized():
            st.switch_page("pages/app_prediction_prix_loyer.py")

    if st.button("🩸 Diabetes Predictor", use_container_width=True, key="sidebar_diabete"):
        if is_authorized():
            st.switch_page("pages/app_prediction_diabete.py")

    if st.button("📊 Data Quality", use_container_width=True, key="sidebar_data"):
        if is_authorized():
            st.switch_page("pages/analyse_data_traitement.py")

    if st.button("📈 Dashboard", use_container_width=True, key="sidebar_dash"):
        if is_authorized():
            st.switch_page("pages/dashboard_v2.py")

    st.markdown("""
        </div>
        <div style='padding: 1rem;'>
            <div style='background: #f1f5f9; padding: 1rem; border-radius: 16px;'>
                <p style='color: #0f172a; font-weight: 600; margin:0 0 0.5rem;'>Version</p>
                <p style='color: #64748b; font-size:0.9rem;'>5.0 • Mars 2026</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- HEADER PRINCIPAL ---
st.markdown("""
    <div class='hero-section'>
        <h1 class='hero-title'>⚡ Gana's AI & Data HomeLab</h1>
        <p class='hero-subtitle'>Espace d'expérimentation : Intelligence Artificielle, Data Analytics, Visualisation et Machine Learning</p>
        <div class='tech-stack'>
            <span class='tech-badge'>🧠 IA</span>
            <span class='tech-badge'>📊 Data Analytics</span>
            <span class='tech-badge'>📈 Dashboards</span>
            <span class='tech-badge'>🤖 Machine Learning</span>
            <span class='tech-badge'>🐍 Python</span>
            <span class='tech-badge'>🔬 Computer Vision</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STATS GLOBALES ---
st.markdown("""
    <div class='stats-grid'>
        <div class='stat-card'>
            <div class='stat-number'>4</div>
            <div class='stat-label'>Applications IA</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>2</div>
            <div class='stat-label'>Dashboards</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>3</div>
            <div class='stat-label'>Outils Analytics</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>50+</div>
            <div class='stat-label'>Fonctionnalités</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SECTION IA ---
st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>🧠</div>
        <h2 class='section-title'>Intelligence Artificielle</h2>
        <span class='section-count'>2 applications</span>
    </div>
""", unsafe_allow_html=True)

col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🏙️</div>
            <h3 class='app-title'>Dakar Immo AI</h3>
            <p class='app-description'>Prédiction intelligente des loyers à Dakar avec Random Forest et visualisations interactives.</p>
            <div class='app-tags'>
                <span class='app-tag primary'>Random Forest</span>
                <span class='app-tag success'>R²=55%</span>
                <span class='app-tag'>Immobilier</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Lancer Dakar Immo", key="rent_home", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_prediction_prix_loyer.py")
        else:
            st.warning("⚠️ Authentification requise")

with col_ia2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🩸</div>
            <h3 class='app-title'>Diabetes Predictor</h3>
            <p class='app-description'>Prédiction du risque de diabète à partir de données cliniques avec ML.</p>
            <div class='app-tags'>
                <span class='app-tag primary'>Classification</span>
                <span class='app-tag success'>HealthTech</span>
                <span class='app-tag'>Prédictif</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🩸 Lancer Diabetes", key="diabetes_home", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_prediction_diabete.py")
        else:
            st.warning("⚠️ Authentification requise")

# --- SECTION DATA ANALYTICS ---
st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>📊</div>
        <h2 class='section-title'>Data Analytics</h2>
        <span class='section-count'>2 applications</span>
    </div>
""", unsafe_allow_html=True)

col_ana1, col_ana2 = st.columns(2)

with col_ana1:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>📊</div>
            <h3 class='app-title'>Data Quality Analyzer</h3>
            <p class='app-description'>Analyse complète de la qualité des données avec détection automatique des anomalies.</p>
            <div class='app-tags'>
                <span class='app-tag primary'>Qualité</span>
                <span class='app-tag'>Outliers</span>
                <span class='app-tag'>Corrélation</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Lancer Data Quality", key="data_home", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/analyse_data_traitement.py")

with col_ana2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🔬</div>
            <h3 class='app-title'>PCA Vision Pro</h3>
            <p class='app-description'>Analyse d'images par décomposition en composantes principales.</p>
            <div class='app-tags'>
                <span class='app-tag primary'>Computer Vision</span>
                <span class='app-tag'>PCA</span>
                <span class='app-tag'>Compression</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔬 Lancer PCA Vision", key="pca_home", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_acp_v2.py")

# --- SECTION DASHBOARDS ---
st.markdown("""
    <div class='section-header'>
        <div class='section-icon'>📈</div>
        <h2 class='section-title'>Dashboards & Visualisations</h2>
        <span class='section-count'>2 dashboards</span>
    </div>
""", unsafe_allow_html=True)

col_dash1, col_dash2 = st.columns(2)

with col_dash1:
    st.markdown("""
        <div class='dashboard-card'>
            <div class='dashboard-icon'>📊</div>
            <h3 class='dashboard-title'>Travaux Dashboard</h3>
            <p class='app-description'>Tableau de bord de pilotage médical avec indicateurs de santé en temps réel.</p>
            <div class='dashboard-tags'>
                <span class='dashboard-tag'>KPIs</span>
                <span class='dashboard-tag'>Santé</span>
                <span class='dashboard-tag'>Temps réel</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Ouvrir Dashboard Médical", key="dash_med", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/dashboard_v2.py")
        else:
            st.warning("⚠️ Authentification requise")

with col_dash2:
    st.markdown("""
        <div class='dashboard-card'>
            <div class='dashboard-icon'>🏠</div>
            <h3 class='dashboard-title'>Dakar Immobilier</h3>
            <p class='app-description'>Analyse du marché immobilier dakarois avec carte interactive et tendances par quartier.</p>
            <div class='dashboard-tags'>
                <span class='dashboard-tag'>Immobilier</span>
                <span class='dashboard-tag'>Carte</span>
                <span class='dashboard-tag'>Prix/m²</span>
                <span class='dashboard-tag'>Quartiers</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🏠 Ouvrir Dashboard Immo", key="dash_immo", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/dashboard_prix_loyers.py")
        else:
            st.warning("⚠️ Authentification requise")

# --- SECTION AUTEUR ---
st.markdown("""
    <div class='author-section'>
        <div class='author-avatar'>👨‍🎓</div>
        <div class='author-info'>
            <h2 class='author-name'>Gana Faye</h2>
            <p class='author-title'>Master 1 - Système d'Information | Data Scientist & Passionné par l'IA</p>
            <div class='author-tags'>
                <span class='author-tag'>🧠 IA</span>
                <span class='author-tag'>📊 Data</span>
                <span class='author-tag'>📈 Dashboard</span>
                <span class='author-tag'>🤖 ML</span>
                <span class='author-tag'>🐍 Python</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class='footer'>
        <strong>⚡ Gana's AI & Data HomeLab</strong> · Conçu avec passion par Gana Faye<br>
        <span style='opacity: 0.7; font-size: 0.8rem;'>© {current_year} - Tous droits réservés · Version 5.0</span>
    </div>
""", unsafe_allow_html=True)