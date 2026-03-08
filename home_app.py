import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from auth_utils import apply_custom_style, is_authorized, login_sidebar
apply_custom_style()
# On place la connexion tout en haut de la page
#login_sidebar()
# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Gana's AI & Data HomeLab",
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

        /* Dégradés par domaine */
        --gradient-ia: linear-gradient(135deg, #6d28d9, #8b5cf6);
        --gradient-analyse: linear-gradient(135deg, #2563eb, #3b82f6);
        --gradient-dashboard: linear-gradient(135deg, #d97706, #f59e0b);
        --gradient-immo: linear-gradient(135deg, #059669, #10b981);
        --gradient-sante: linear-gradient(135deg, #dc2626, #ef4444);
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
        background: var(--gradient-ia);
        padding: 1.5rem 1.2rem;
        margin: -1rem -1rem 1.2rem -1rem;
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .sidebar-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #f72585, #b5179e);
        opacity: 0.5;
    }

    .sidebar-header::after {
        content: '🚀';
        position: absolute;
        bottom: -15px;
        right: -15px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(-10deg);
    }

    .sidebar-header h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--white);
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .sidebar-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.8rem;
        margin: 0.3rem 0 0 0;
        font-weight: 300;
    }

    .sidebar-section {
        background: var(--light);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s ease;
    }

    .sidebar-section:hover {
        border-color: var(--primary-light);
        box-shadow: 0 5px 15px rgba(67, 97, 238, 0.1);
    }

    .sidebar-section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--gray-lighter);
    }

    .sidebar-section-title span {
        background: var(--gradient-ia);
        color: var(--white);
        width: 24px;
        height: 24px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.8rem;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    }

    .sidebar-item {
        padding: 0.4rem 0;
        color: var(--gray-dark);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.9rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }

    .sidebar-item:hover {
        transform: translateX(5px);
        color: var(--primary);
    }

    .sidebar-item-icon {
        width: 20px;
        text-align: center;
        font-size: 1rem;
    }

    .sidebar-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        background: var(--gradient-ia);
        color: var(--white);
        margin: 0.1rem;
        border: none;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    }

    /* ===== BANNIÈRE PRINCIPALE ===== */
    .hero-section {
        background: var(--white);
        padding: 2rem;
        border-radius: 30px;
        margin: 1rem 0 1.5rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.02);
        border: 1px solid var(--gray-lighter);
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-ia);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--gradient-ia);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .hero-subtitle {
        color: var(--gray);
        font-size: 1rem;
        margin: 0.8rem 0;
    }

    /* ===== BADGES TECHNOLOGIQUES ===== */
    .tech-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        background: var(--white);
        color: var(--dark);
        font-size: 0.8rem;
        margin: 0.2rem;
        border: 1px solid var(--gray-lighter);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }

    .tech-badge:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(67, 97, 238, 0.1);
    }

    /* ===== EN-TÊTE DE SECTION PAR DOMAINE ===== */
    .domain-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2.5rem 0 1.5rem 0;
        padding: 1rem 1.5rem;
        border-radius: 60px;
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 1px solid var(--gray-lighter);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }

    .domain-icon {
        font-size: 2.5rem;
    }

    .domain-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--dark);
        font-family: 'Space Grotesk', sans-serif;
        flex-grow: 1;
    }

    .domain-badge {
        background: var(--gradient-ia);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 40px;
        font-size: 0.9rem;
        font-weight: 600;
        white-space: nowrap;
    }

    .domain-badge-ia {
        background: var(--gradient-ia);
    }

    .domain-badge-analyse {
        background: var(--gradient-analyse);
    }

    .domain-badge-dashboard {
        background: var(--gradient-dashboard);
    }

    /* ===== CARTES DES APPLICATIONS ===== */
    .app-card {
        background: var(--white);
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .app-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        transition: width 0.3s ease;
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(67, 97, 238, 0.1);
    }

    .app-card:hover::before {
        width: 6px;
    }

    /* Cartes par domaine */
    .app-card-ia::before {
        background: var(--gradient-ia);
    }

    .app-card-analyse::before {
        background: var(--gradient-analyse);
    }

    .app-card-dashboard::before {
        background: var(--gradient-dashboard);
    }

    .app-card-immo::before {
        background: var(--gradient-immo);
    }

    .app-card-sante::before {
        background: var(--gradient-sante);
    }

    .app-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
    }

    .app-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 0.6rem;
        font-family: 'Space Grotesk', sans-serif;
    }

    .app-description {
        color: var(--gray);
        font-size: 0.85rem;
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }

    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0.6rem 0;
    }

    .feature-list li {
        padding: 0.3rem 0;
        color: var(--gray-dark);
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.8rem;
        border-bottom: 1px dashed var(--gray-lighter);
    }

    .feature-list li:last-child {
        border-bottom: none;
    }

    .feature-list li::before {
        content: "✨";
        color: var(--primary);
        font-size: 0.8rem;
    }

    .app-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--white);
        margin-top: 0.6rem;
    }

    .badge-ia {
        background: var(--gradient-ia);
    }

    .badge-analyse {
        background: var(--gradient-analyse);
    }

    .badge-dashboard {
        background: var(--gradient-dashboard);
    }

    .badge-immo {
        background: var(--gradient-immo);
    }

    .badge-sante {
        background: var(--gradient-sante);
    }

    /* ===== CARTES DE DASHBOARD ===== */
    .dashboard-card {
        background: linear-gradient(135deg, #ffffff, #fef9e7);
        padding: 1.2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        border: 1px solid #fed7aa;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: var(--gradient-dashboard);
        transition: width 0.3s ease;
    }

    .dashboard-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(245, 158, 11, 0.1);
        border-color: #f59e0b;
    }

    .dashboard-card:hover::before {
        width: 4px;
    }

    .dashboard-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        background: var(--gradient-dashboard);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .dashboard-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #92400e;
        margin-bottom: 0.6rem;
        font-family: 'Space Grotesk', sans-serif;
    }

    .dashboard-meta {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 0.5rem 0;
    }

    .dashboard-tag {
        background: #fef3c7;
        color: #92400e;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
    }

    /* ===== SECTION RÉALISATEUR ===== */
    .author-section {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem 1.2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(67, 97, 238, 0.15);
        box-shadow: 0 15px 35px rgba(67, 97, 238, 0.08);
        position: relative;
        overflow: hidden;
        text-align: center;
        transition: all 0.3s ease;
    }

    .author-avatar {
        position: relative;
        width: 90px;
        height: 90px;
        margin: 0 auto 0.8rem auto;
        background: var(--gradient-ia);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 15px 30px rgba(67, 97, 238, 0.3);
        border: 3px solid white;
        transition: all 0.3s ease;
        z-index: 2;
    }

    .author-avatar-icon {
        font-size: 3rem;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
    }

    .author-name {
        font-size: 1.6rem;
        font-weight: 800;
        background: var(--gradient-ia);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0 0.1rem 0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .author-title {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
        font-weight: 400;
    }

    /* ===== STATS CARDS ===== */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .stat-card {
        background: var(--white);
        padding: 1.2rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        transform: translateY(-3px);
        border-color: var(--primary-light);
        box-shadow: 0 10px 25px rgba(67, 97, 238, 0.1);
    }

    .stat-number {
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--primary);
        line-height: 1;
    }

    .stat-label {
        color: var(--gray);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.2rem;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.2rem;
        background: var(--white);
        border-radius: 20px 20px 0 0;
        margin-top: 1.5rem;
        color: var(--gray);
        font-size: 0.8rem;
        border-top: 1px solid var(--gray-lighter);
        position: relative;
        overflow: hidden;
    }

    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: var(--gradient-ia);
    }

    /* ===== BOUTONS ===== */
    .stButton > button {
        background: var(--gradient-ia);
        color: var(--white);
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.3);
    }

    .btn-analyse > button {
        background: var(--gradient-analyse) !important;
    }

    .btn-dashboard > button {
        background: var(--gradient-dashboard) !important;
    }

    .btn-immo > button {
        background: var(--gradient-immo) !important;
    }

    .btn-sante > button {
        background: var(--gradient-sante) !important;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .app-title {
            font-size: 1.2rem;
        }
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        .domain-header {
            flex-wrap: wrap;
        }
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

# --- SIDEBAR HARMONISÉE ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>🚀 Menu</h3>
            <p>Navigation par domaine</p>
        </div>
    """, unsafe_allow_html=True)
    login_sidebar()
    # Section Navigation
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>📍</span> Navigation
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">🏠</span>
                <span>Accueil</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section Applications - Intelligence Artificielle
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>🧠</span> Intelligence Artificielle
            </div>
    """, unsafe_allow_html=True)

    if st.button("🏙️ Dakar Immo AI", use_container_width=True, key="sidebar_rent"):
        st.switch_page("pages/app_prediction_prix_loyer.py")

    if st.button("🩸 Diabetes Predictor", use_container_width=True, key="sidebar_diabete"):
        st.switch_page("pages/app_prediction_diabete.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Applications - Data Analytics
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>📊</span> Data Analytics
            </div>
    """, unsafe_allow_html=True)

    if st.button("📊 Data Quality Analyzer", use_container_width=True, key="sidebar_data"):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button("🔬 PCA Vision Pro", use_container_width=True, key="sidebar_pca"):
        st.switch_page("pages/app_acp_v2.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Dashboards
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>📈</span> Dashboards
            </div>
    """, unsafe_allow_html=True)

    if st.button("📈 Travaux Dashboard", use_container_width=True, key="sidebar_dash"):
        st.switch_page("pages/dashboard_v2.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Informations
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>ℹ️</span> Informations
            </div>
            <div style='padding: 0.4rem 0; color: #334155; font-size: 0.85rem;'>
                <p><strong>Version:</strong> 5.0</p>
                <p><strong>Mise à jour:</strong> Mars 2026</p>
                <p><strong>Auteur:</strong> Gana Faye</p>
            </div>
            <div style='display: flex; flex-wrap: wrap; gap: 0.2rem; margin-top: 0.4rem;'>
                <span class='sidebar-badge'>Python</span>
                <span class='sidebar-badge'>Streamlit</span>
                <span class='sidebar-badge'>ML</span>
                <span class='sidebar-badge'>IA</span>
                <span class='sidebar-badge'>Data</span>
                <span class='sidebar-badge'>Dashboard</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer de la sidebar
    st.markdown("""
        <div class="sidebar-footer">
            <strong>Gana's AI & Data Lab</strong><br>
            <span style='font-size: 0.6rem;'>© 2026 Gana Faye</span>
        </div>
    """, unsafe_allow_html=True)

# --- INITIALISATION DU SESSION STATE ---
if 'df_analyse' not in st.session_state:
    st.session_state.df_analyse = None
if 'image_grise' not in st.session_state:
    st.session_state.image_grise = None

# --- BANNIÈRE PRINCIPALE ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🚀 Gana's AI & Data HomeLab</h1>
        <p class="hero-subtitle">Espace d'expérimentation : Intelligence Artificielle, Data Analytics, Visualisation et Machine Learning</p>
        <div style='display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; margin-top: 1.5rem;'>
            <span class='tech-badge'>🧠 IA</span>
            <span class='tech-badge'>📊 Data Analytics</span>
            <span class='tech-badge'>📈 Dashboards</span>
            <span class='tech-badge'>🤖 ML</span>
            <span class='tech-badge'>🔬 Computer Vision</span>
            <span class='tech-badge'>🩸 HealthTech</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- STATISTIQUES GLOBALES ---
st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">IA Applications</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">2</div>
            <div class="stat-label">Data Analytics</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">1</div>
            <div class="stat-label">Dashboard</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">50+</div>
            <div class="stat-label">Fonctionnalités</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SECTION 1 : INTELLIGENCE ARTIFICIELLE ---
st.markdown("""
    <div class="domain-header">
        <span class="domain-icon">🧠</span>
        <span class="domain-title">Intelligence Artificielle & Machine Learning</span>
        <span class="domain-badge domain-badge-ia">2 applications</span>
    </div>
""", unsafe_allow_html=True)

col_ia1, col_ia2 = st.columns(2)

with col_ia1:
    st.markdown("""
        <div class='app-card app-card-immo'>
            <div class='app-icon'>🏙️</div>
            <h2 class='app-title'>Dakar Immo AI</h2>
            <p class='app-description'>Prédiction intelligente des loyers à Dakar basée sur Random Forest avec visualisations interactives et analyse de marché.</p>
            <ul class='feature-list'>
                <li>Prédiction en temps réel</li>
                <li>Analyse par quartier</li>
                <li>Matrice Surface × Chambres</li>
                <li>Comparaison des options</li>
            </ul>
            <span class='app-badge badge-immo'>🏠 Immobilier</span>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 Lancer Dakar Immo", key="rent_lab", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_prediction_prix_loyer.py")
        else:
            st.warning("⚠️ Accès restreint. Veuillez vous identifier par email dans la barre latérale.")

with col_ia2:
    st.markdown("""
        <div class='app-card app-card-sante'>
            <div class='app-icon'>🩸</div>
            <h2 class='app-title'>Diabetes Predictor</h2>
            <p class='app-description'>Prédiction du risque de diabète basée sur les données cliniques avec algorithmes de machine learning.</p>
            <ul class='feature-list'>
                <li>Prédiction en temps réel</li>
                <li>Analyse des facteurs de risque</li>
                <li>Interprétation des résultats</li>
                <li>Recommandations personnalisées</li>
            </ul>
            <span class='app-badge badge-sante'>🩸 Santé</span>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🩸 Lancer Diabetes Predictor", key="diabetes_lab", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_prediction_diabete.py")
        else:
            st.warning("⚠️ Cette application nécessite une autorisation par email.")

# --- SECTION 2 : DATA ANALYTICS ---
st.markdown("""
    <div class="domain-header">
        <span class="domain-icon">📊</span>
        <span class="domain-title">Data Analytics & Traitement</span>
        <span class="domain-badge domain-badge-analyse">2 applications</span>
    </div>
""", unsafe_allow_html=True)

col_ana1, col_ana2 = st.columns(2)

with col_ana1:
    st.markdown("""
        <div class='app-card app-card-analyse'>
            <div class='app-icon'>📊</div>
            <h2 class='app-title'>Data Quality Analyzer</h2>
            <p class='app-description'>Analyse complète de la qualité des données avec détection automatique des problèmes et suggestions de nettoyage.</p>
            <ul class='feature-list'>
                <li>Classification des variables</li>
                <li>Détection des outliers</li>
                <li>Matrice de corrélation</li>
                <li>Recommandations ML</li>
            </ul>
            <span class='app-badge badge-analyse'>📈 Data Science</span>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Lancer Data Quality", key="data_lab", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/analyse_data_traitement.py")
        else:
            st.warning("⚠️ Accès réservé aux utilisateurs autorisés.")

with col_ana2:
    st.markdown("""
        <div class='app-card app-card-analyse'>
            <div class='app-icon'>🔬</div>
            <h2 class='app-title'>PCA Vision Pro</h2>
            <p class='app-description'>Analyse d'images par décomposition en composantes principales avec visualisation de la reconstruction.</p>
            <ul class='feature-list'>
                <li>Compression d'images</li>
                <li>Analyse de variance</li>
                <li>Reconstruction progressive</li>
                <li>Tests multi-niveaux</li>
            </ul>
            <span class='app-badge badge-analyse'>👁️ Computer Vision</span>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔬 Lancer PCA Vision", key="pca_lab", use_container_width=True):
        if is_authorized():
            st.switch_page("pages/app_acp_v2.py")
        else:
            st.warning("⚠️ Veuillez vous connecter pour accéder aux outils d'analyse.")

# --- SECTION 3 : DASHBOARDS ---
st.markdown("""
    <div class="domain-header">
        <span class="domain-icon">📈</span>
        <span class="domain-title">Dashboards & Visualisations</span>
        <span class="domain-badge domain-badge-dashboard">1 dashboard</span>
    </div>
""", unsafe_allow_html=True)

col_dash1, col_dash2 = st.columns([1, 1])

with col_dash1:
    st.markdown("""
        <div class='dashboard-card'>
            <div class='dashboard-icon'>📈</div>
            <h2 class='dashboard-title'>Travaux Dashboard</h2>
            <p class='app-description'>Tableau de bord interactif de Pilotage Médical. Analyse en temps réel des indicateurs de santé - République du Sénégal.</p>
            <div class='dashboard-meta'>
                <span class='dashboard-tag'>KPIs</span>
                <span class='dashboard-tag'>Graphiques</span>
                <span class='dashboard-tag'>Temps réel</span>
                <span class='dashboard-tag'>Santé</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📊 Ouvrir le Dashboard", key="dash_lab", use_container_width=True, help="Lancer Travaux Dashboard"):
        if is_authorized():
            st.switch_page("pages/dashboard_v2.py")
        else:
            st.warning("⚠️ Dashboard sécurisé. Identifiez-vous pour consulter les statistiques.")

# --- SECTION RÉALISATEUR ---
st.markdown("""
    <div class='author-section'>
        <div class='author-avatar'>
            <span class='author-avatar-icon'>👨‍🎓</span>
        </div>
        <h2 class='author-name'>Gana Faye</h2>
        <div class='author-title'>Master 1 - Système d'Information | Data Scientist & Passionné par l'IA</div>
        <div style='display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;'>
            <span class='tech-badge'>🧠 IA</span>
            <span class='tech-badge'>📊 Data</span>
            <span class='tech-badge'>📈 Dashboard</span>
            <span class='tech-badge'>🤖 ML</span>
            <span class='tech-badge'>🐍 Python</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class='footer'>
        <strong>🚀 Gana's AI & Data HomeLab</strong> · Conçu avec passion par Gana Faye<br>
        <span style='opacity: 0.7; font-size: 0.7rem;'>© {current_year} - Tous droits réservés · Version 5.0</span>
    </div>
""", unsafe_allow_html=True)