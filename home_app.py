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

# --- STYLE CSS HARMONISÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #4361ee;
        --primary-dark: #3a56d4;
        --secondary: #7209b7;
        --accent: #f72585;
        --dark: #1e293b;
        --white: #ffffff;
        --gradient-primary: linear-gradient(135deg, #4361ee, #7209b7);
    }

    /* Masquage du menu par défaut pour un look Custom */
    [data-testid="stSidebarNav"] {display: none !important;}

    .main {
        background: linear-gradient(135deg, #f1f5f9 0%, #e6edf5 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Styles de la Sidebar */
    .sidebar-header {
        background: var(--gradient-primary);
        padding: 1.5rem;
        margin: -1rem -1rem 1rem -1rem;
        color: white;
        text-align: center;
    }

    .sidebar-section {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }

    .sidebar-section-title {
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 0.8rem;
        color: var(--dark);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .sidebar-item {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.9rem;
        padding: 0.3rem 0;
        color: #475569;
    }

    /* Cartes des Applications */
    .app-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        height: 100%;
        transition: 0.3s;
    }
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(67, 97, 238, 0.1);
    }
    .app-icon { font-size: 2.5rem; margin-bottom: 1rem; }
    .app-title { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--dark); }

    /* Hero Section */
    .hero-section {
        background: white;
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Badges */
    .tech-badge {
        padding: 0.4rem 1rem;
        background: #f1f5f9;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR HARMONISÉE ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>🚀 Menu Pro</h3>
            <p>Master 1 - Gana Faye</p>
        </div>
    """, unsafe_allow_html=True)

    # Section Navigation
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">📍 Navigation</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🏠 Accueil</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🏙️ Dakar Rent AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📊 Data Quality</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🔬 PCA Vision</div></div>', unsafe_allow_html=True)

    # Section Applications (Boutons de switch)
    st.markdown('<div class="sidebar-section"><div class="sidebar-section-title">🚀 Lancer une App</div>',
                unsafe_allow_html=True)

    if st.button("🏙️ Dakar Rent AI", use_container_width=True, key="side_rent"):
        st.switch_page("pages/app_prediction_prix_loyer.py")

    if st.button("📊 Data Quality", use_container_width=True, key="side_data"):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button("🔬 PCA Vision Pro", use_container_width=True, key="side_pca"):
        st.switch_page("pages/app_acp_v2.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Infos Auteur
    st.markdown(f"""
        <div class="sidebar-section" style="text-align:center;">
            <p style="font-size:0.8rem; color:gray;">© {datetime.now().year} Gana Faye</p>
            <span class="tech-badge">Python 3.12</span>
        </div>
    """, unsafe_allow_html=True)

# --- CONTENU PRINCIPAL ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Data & Image Analytics Hub</h1>
        <p style="color:#64748b; font-size:1.1rem;">Intelligence Artificielle et Analyse de Données Immobilières à Dakar</p>
        <div style="display:flex; justify-content:center; gap:10px; margin-top:20px;">
            <span class="tech-badge">Random Forest</span>
            <span class="tech-badge">PCA / ACP</span>
            <span class="tech-badge">Computer Vision</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- GRILLE DES APPLICATIONS ---
st.markdown("## ✨ Mes Applications")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
        <div class="app-card">
            <div class="app-icon">🏙️</div>
            <h3 class="app-title">Dakar Rent AI</h3>
            <p style="font-size:0.85rem; color:#64748b;">Estimation prédictive des loyers à Dakar via Random Forest.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer Rent AI", key="main_rent"):
        st.switch_page("pages/app_prediction_prix_loyer.py")

with c2:
    st.markdown("""
        <div class="app-card">
            <div class="app-icon">📊</div>
            <h3 class="app-title">Data Quality</h3>
            <p style="font-size:0.85rem; color:#64748b;">Analyse et nettoyage complet de vos datasets complexes.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer Data Quality", key="main_data"):
        st.switch_page("pages/analyse_data_traitement.py")

with c3:
    st.markdown("""
        <div class="app-card">
            <div class="app-icon">🔬</div>
            <h3 class="app-title">PCA Vision Pro</h3>
            <p style="font-size:0.85rem; color:#64748b;">Compression et analyse d'image par réduction de dimension.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Lancer PCA Vision", key="main_pca"):
        st.switch_page("pages/app_acp_v2.py")

# --- FOOTER STATS ---
st.write("##")
st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;'>
        <div style='background:white; padding:1.5rem; border-radius:15px; text-align:center; border:1px solid #e2e8f0;'>
            <h2 style='color:#4361ee; margin:0;'>3</h2>
            <p style='color:gray; font-size:0.8rem; margin:0;'>Apps Intégrées</p>
        </div>
        <div style='background:white; padding:1.5rem; border-radius:15px; text-align:center; border:1px solid #e2e8f0;'>
            <h2 style='color:#4361ee; margin:0;'>12k+</h2>
            <p style='color:gray; font-size:0.8rem; margin:0;'>Data Points</p>
        </div>
        <div style='background:white; padding:1.5rem; border-radius:15px; text-align:center; border:1px solid #e2e8f0;'>
            <h2 style='color:#4361ee; margin:0;'>M1</h2>
            <p style='color:gray; font-size:0.8rem; margin:0;'>Promotion 2026</p>
        </div>
    </div>
""", unsafe_allow_html=True)