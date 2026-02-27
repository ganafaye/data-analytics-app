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

# --- STYLE CSS AVEC COULEURS HARMONISÉES ---
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
        padding: 2rem 1.5rem;
        margin: -1rem -1rem 1.5rem -1rem;
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
        background: var(--gradient-accent);
        opacity: 0.5;
    }

    .sidebar-header::after {
        content: '🚀';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 5rem;
        opacity: 0.1;
        transform: rotate(-10deg);
    }

    .sidebar-header h3 {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--white);
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }

    .sidebar-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }

    .sidebar-section {
        background: var(--light);
        border-radius: 20px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--gray-lighter);
        transition: all 0.3s ease;
    }

    .sidebar-section:hover {
        border-color: var(--primary-light);
        box-shadow: 0 5px 15px rgba(67, 97, 238, 0.1);
    }

    .sidebar-section-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--gray-lighter);
    }

    .sidebar-section-title span {
        background: var(--gradient-primary);
        color: var(--white);
        width: 28px;
        height: 28px;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    }

    .sidebar-item {
        padding: 0.5rem 0;
        color: var(--gray-dark);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-size: 0.95rem;
        border-radius: 12px;
        transition: all 0.2s ease;
    }

    .sidebar-item:hover {
        transform: translateX(5px);
        color: var(--primary);
    }

    .sidebar-item-icon {
        width: 24px;
        text-align: center;
        font-size: 1.1rem;
    }

    .sidebar-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 500;
        background: var(--gradient-primary);
        color: var(--white);
        margin: 0.2rem;
        border: none;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: var(--dark) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: var(--white) !important;
        border: 1px solid var(--gray-lighter) !important;
        border-radius: 16px !important;
        padding: 0.3rem 1rem !important;
        transition: all 0.3s ease !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1) !important;
    }

    section[data-testid="stSidebar"] .stCheckbox > div {
        border-radius: 8px !important;
        padding: 0.3rem !important;
    }

    section[data-testid="stSidebar"] .stCheckbox > div:hover {
        background: rgba(67, 97, 238, 0.05) !important;
    }

    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        background: var(--gradient-primary) !important;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: var(--gradient-primary);
        color: var(--white);
        border: none;
        border-radius: 16px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.4);
    }

    .sidebar-footer {
        padding: 1rem;
        margin-top: 2rem;
        text-align: center;
        border-top: 1px solid var(--gray-lighter);
        font-size: 0.8rem;
        color: var(--gray);
    }

    .sidebar-footer strong {
        color: var(--primary);
        font-weight: 600;
    }

    /* ===== BANNIÈRE PRINCIPALE ===== */
    .hero-section {
        background: var(--white);
        padding: 3rem;
        border-radius: 40px;
        margin: 1rem 0 2rem 0;
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
        background: var(--gradient-primary);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
    }

    .hero-subtitle {
        color: var(--gray);
        font-size: 1.2rem;
        margin: 1rem 0;
    }

    /* ===== BADGES TECHNOLOGIQUES ===== */
    .tech-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.2rem;
        border-radius: 40px;
        background: var(--white);
        color: var(--dark);
        font-size: 0.9rem;
        margin: 0.3rem;
        border: 1px solid var(--gray-lighter);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }

    .tech-badge:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(67, 97, 238, 0.1);
    }

    /* ===== CARTES DES APPLICATIONS ===== */
    .app-card {
        background: var(--white);
        padding: 2rem;
        border-radius: 30px;
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
        background: var(--gradient-primary);
        transition: width 0.3s ease;
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(67, 97, 238, 0.1);
        border-color: var(--primary-light);
    }

    .app-card:hover::before {
        width: 6px;
    }

    .app-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 1rem;
        font-family: 'Space Grotesk', sans-serif;
    }

    .app-description {
        color: var(--gray);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .feature-list {
        list-style: none;
        padding: 0;
        margin: 1rem 0;
    }

    .feature-list li {
        padding: 0.5rem 0;
        color: var(--gray-dark);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
        border-bottom: 1px dashed var(--gray-lighter);
    }

    .feature-list li:last-child {
        border-bottom: none;
    }

    .feature-list li::before {
        content: "✨";
        color: var(--primary);
    }

    .app-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 40px;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--white);
        margin-top: 1rem;
    }

    .badge-primary {
        background: var(--gradient-primary);
    }

    .badge-success {
        background: var(--gradient-success);
    }

   /* ===== SECTION RÉALISATEUR CORRIGÉE ===== */
.author-section {
    background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
    padding: 2rem 1.5rem;
    border-radius: 30px;
    margin: 2rem 0;
    border: 1px solid rgba(67, 97, 238, 0.15);
    box-shadow: 0 15px 35px rgba(67, 97, 238, 0.08);
    position: relative;
    overflow: hidden;
    text-align: center;
    transition: all 0.3s ease;
}

.author-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 100px;
    background: linear-gradient(135deg, rgba(67, 97, 238, 0.03) 0%, rgba(114, 9, 183, 0.03) 100%);
    border-radius: 30px 30px 50% 50%;
}

.author-section::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(135deg, #f72585, #b5179e);
}

.author-avatar {
    position: relative;
    width: 110px;
    height: 110px;
    margin: 0 auto 1rem auto;
    background: linear-gradient(135deg, #4361ee, #7209b7);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 15px 30px rgba(67, 97, 238, 0.3);
    border: 3px solid white;
    transition: all 0.3s ease;
    z-index: 2;
}

.author-avatar:hover {
    transform: scale(1.05);
    box-shadow: 0 20px 40px rgba(67, 97, 238, 0.4);
}

.author-avatar-icon {
    font-size: 3.5rem;
    filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
}

.author-badge-container {
    margin-bottom: 0.8rem;
}

.author-badge {
    display: inline-block;
    padding: 0.4rem 1.2rem;
    background: linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(114, 9, 183, 0.1));
    color: #4361ee;
    font-size: 0.8rem;
    font-weight: 600;
    border-radius: 40px;
    border: 1px solid rgba(67, 97, 238, 0.3);
    backdrop-filter: blur(5px);
    letter-spacing: 0.5px;
}

.author-name {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4361ee, #7209b7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.3rem 0 0.2rem 0;
    font-family: 'Space Grotesk', sans-serif;
}

.author-title {
    color: #64748b;
    font-size: 1rem;
    margin-bottom: 1.5rem;
    font-weight: 400;
    position: relative;
    display: inline-block;
}

.author-title::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 25%;
    width: 50%;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4361ee, #7209b7, transparent);
}

.author-stats {
    display: flex;
    justify-content: space-around;
    margin: 1.5rem 0;
    padding: 1rem 0;
    border-top: 1px dashed rgba(67, 97, 238, 0.2);
    border-bottom: 1px dashed rgba(67, 97, 238, 0.2);
}

.author-stats .stat-item {
    text-align: center;
    transition: all 0.3s ease;
}

.author-stats .stat-item:hover {
    transform: translateY(-3px);
}

.author-stats .stat-number {
    font-size: 1.4rem;
    font-weight: 700;
    color: #4361ee;
    line-height: 1;
}

.author-stats .stat-label {
    font-size: 0.7rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.2rem;
}

.skills-container {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    justify-content: center;
    margin: 1.2rem 0;
}

.skill-tag {
    background: #f1f5f9;
    color: #334155;
    padding: 0.3rem 1rem;
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 500;
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
}

.skill-tag:hover {
    background: linear-gradient(135deg, #4361ee, #7209b7);
    color: white;
    border-color: transparent;
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
}

.social-links {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.social-link {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1.2rem;
    border-radius: 40px;
    background: #f8fafc;
    color: #334155;
    text-decoration: none;
    font-size: 0.85rem;
    border: 1px solid #e2e8f0;
    transition: all 0.3s ease;
}

.social-link:hover {
    background: linear-gradient(135deg, #4361ee, #7209b7);
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(67, 97, 238, 0.25);
    border-color: transparent;
}

.social-icon {
    font-size: 1.1rem;
}

.social-text {
    font-weight: 500;
}

.author-quote {
    margin: 1.5rem 0 1rem 0;
    padding: 1rem;
    background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    border-radius: 20px;
    border-left: 3px solid #4361ee;
    color: #475569;
    font-style: italic;
    font-size: 0.9rem;
    line-height: 1.6;
    position: relative;
}

.quote-mark {
    color: #4361ee;
    font-size: 1.2rem;
    font-weight: 700;
    opacity: 0.5;
    margin: 0 0.2rem;
}

.author-footer {
    margin-top: 1.2rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    font-size: 0.8rem;
    color: #64748b;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.institution {
    font-weight: 500;
    color: #4361ee;
}

.separator {
    color: #cbd5e1;
}

.promo {
    font-weight: 400;
}

/* Responsive */
@media (max-width: 768px) {
    .author-avatar {
        width: 90px;
        height: 90px;
    }
    
    .author-avatar-icon {
        font-size: 3rem;
    }
    
    .author-name {
        font-size: 1.6rem;
    }
    
    .social-link {
        padding: 0.4rem 1rem;
        font-size: 0.8rem;
    }
}
    /* ===== STATS CARDS ===== */
    .stat-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: 30px;
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
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
    }

    .stat-label {
        color: var(--gray);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: var(--white);
        border-radius: 30px 30px 0 0;
        margin-top: 2rem;
        color: var(--gray);
        font-size: 0.9rem;
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
        background: var(--gradient-primary);
    }

    /* ===== BOUTONS PRINCIPAUX ===== */
    .stButton > button {
        background: var(--gradient-primary);
        color: var(--white);
        border: none;
        border-radius: 30px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.3);
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }

        .app-title {
            font-size: 1.5rem;
        }
    }

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
            <div class="sidebar-section-title">
                <span>📍</span> Navigation
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">🏠</span>
                <span>Accueil</span>
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">📊</span>
                <span>Data Quality Analyzer</span>
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">🔬</span>
                <span>PCA Vision Pro</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section Applications
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>🚀</span> Applications
            </div>
    """, unsafe_allow_html=True)

    if st.button("📊 Lancer Data Quality", width='stretch', key="sidebar_data"):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button("🔬 Lancer PCA Vision", width='stretch', key="sidebar_pca"):
        st.switch_page("pages/app_acp_v2.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Paramètres
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>⚙️</span> Paramètres
            </div>
    """, unsafe_allow_html=True)

    theme = st.selectbox("Thème", ["Clair", "Sombre"], key="sidebar_theme")
    notifications = st.checkbox("Notifications", value=True)
    autosave = st.checkbox("Sauvegarde auto", value=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Informations
    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>ℹ️</span> Informations
            </div>
            <div style='padding: 0.5rem 0; color: #334155; font-size: 0.9rem;'>
                <p><strong>Version:</strong> 4.0</p>
                <p><strong>Mise à jour:</strong> Février 2026</p>
                <p><strong>Auteur:</strong> Gana Faye</p>
            </div>
            <div style='display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.5rem;'>
                <span class='sidebar-badge'>Python</span>
                <span class='sidebar-badge'>Streamlit</span>
                <span class='sidebar-badge'>ML</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer de la sidebar
    st.markdown("""
        <div class="sidebar-footer">
            <strong>Data & Image Analytics Hub</strong><br>
            <span style='font-size: 0.7rem;'>© 2026 Gana Faye</span>
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
        <h1 class="hero-title">🚀 Data & Image Analytics Hub</h1>
        <p class="hero-subtitle">La plateforme ultime pour l'analyse de données et d'images</p>
        <div style='display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;'>
            <span class='tech-badge'>🐍 Python 3.12</span>
            <span class='tech-badge'>📊 Streamlit</span>
            <span class='tech-badge'>🤖 Scikit-learn</span>
            <span class='tech-badge'>📈 Pandas</span>
            <span class='tech-badge'>🔬 OpenCV</span>
            <span class='tech-badge'>🎨 Plotly</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SECTION DES APPLICATIONS ---
st.markdown("## ✨ Nos Applications")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>📊</div>
            <h2 class='app-title'>Data Quality Analyzer</h2>
            <p class='app-description'>Analyse intelligente de la qualité des données avec recommandations ML et feature engineering avancé.</p>
            <ul class='feature-list'>
                <li>Classification automatique des variables</li>
                <li>Détection des outliers et valeurs manquantes</li>
                <li>Recommandations de feature engineering</li>
                <li>Préparation pour l'ACP</li>
                <li>Export de rapports HTML/CSV</li>
            </ul>
            <span class='app-badge badge-primary'>🤖 Machine Learning</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Lancer Data Quality Analyzer", key="btn_data", width='stretch'):
        st.switch_page("pages/analyse_data_traitement.py")

with col2:
    st.markdown("""
        <div class='app-card'>
            <div class='app-icon'>🔬</div>
            <h2 class='app-title'>PCA Vision Pro</h2>
            <p class='app-description'>Analyse d'images par décomposition en composantes principales avec compression intelligente.</p>
            <ul class='feature-list'>
                <li>Compression intelligente d'images</li>
                <li>Analyse de la variance expliquée</li>
                <li>Visualisation des résidus</li>
                <li>Tests progressifs multi-niveaux</li>
                <li>Matrice numérique comparative</li>
            </ul>
            <span class='app-badge badge-success'>🔬 Traitement d'images</span>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔬 Lancer PCA Vision Pro", key="btn_pca", width='stretch'):
        st.switch_page("pages/app_acp_v2.py")

# --- SECTION RÉALISATEUR CORRIGÉE ---
st.markdown("""
    <div class='author-section'>
        <div class='author-avatar'>
            <span class='author-avatar-icon'>👨‍🎓</span>
        </div>
        <div class='author-badge-container'>
            <span class='author-badge'>Master 1 - Système d'Information</span>
        </div>
        <h2 class='author-name'>Gana Faye</h2>
        <div class='author-title'>Data Scientist & Passionné par l'IA</div>
        
        
    </div>
""", unsafe_allow_html=True)

# --- STATISTIQUES RAPIDES ---
st.markdown("""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin: 3rem 0;'>
        <div class='stat-card'>
            <div class='stat-number'>2</div>
            <div class='stat-label'>Applications</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>20+</div>
            <div class='stat-label'>Fonctionnalités</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>10+</div>
            <div class='stat-label'>Types de fichiers</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER AVEC COPYRIGHT DYNAMIQUE ---
current_year = datetime.now().year
st.markdown(f"""
    <div class='footer'>
        <strong>🚀 Data & Image Analytics Hub</strong> · Conçu avec passion par Gana Faye<br>
        <span style='opacity: 0.7; font-size: 0.8rem;'>© {current_year} - Tous droits réservés · Version 4.0</span>
    </div>
""", unsafe_allow_html=True)