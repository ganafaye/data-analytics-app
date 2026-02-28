import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Data & Image Analytics Hub | Gana Faye",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INTÉGRATION DES GOOGLE MATERIAL ICONS ---
st.markdown("""
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Round">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Sharp">

    <style>
    /* Style de base pour les icônes */
    .material-icons, .material-icons-outlined, .material-icons-round, .material-icons-sharp {
        font-family: 'Material Icons' !important;
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        font-feature-settings: 'liga';
        vertical-align: middle;
    }

    .material-icons-outlined { font-family: 'Material Icons Outlined' !important; }
    .material-icons-round { font-family: 'Material Icons Round' !important; }
    .material-icons-sharp { font-family: 'Material Icons Sharp' !important; }

    /* Animation pour les icônes */
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .spin {
        animation: spin 2s linear infinite;
        display: inline-block;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .pulse {
        animation: pulse 2s ease infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    .bounce {
        animation: bounce 1s ease infinite;
    }
    </style>
""", unsafe_allow_html=True)


# --- FONCTION POUR LES ICÔNES ---
def icon(name, variant="outlined", size=24, color=None, animation=None):
    """Génère une icône Google Material"""
    classes = f"material-icons-{variant}"
    if animation:
        classes += f" {animation}"

    style = f"font-size: {size}px; line-height: 1; vertical-align: middle;"
    if color:
        style += f" color: {color};"

    return f"<i class='{classes}' style='{style}'>{name}</i>"


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
        content: 'dashboard';
        font-family: 'Material Icons';
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
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
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
        background: var(--gradient-primary);
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
        background: var(--gradient-primary);
        color: var(--white);
        margin: 0.1rem;
        border: none;
        box-shadow: 0 2px 8px rgba(67, 97, 238, 0.3);
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: var(--dark) !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: var(--white) !important;
        border: 1px solid var(--gray-lighter) !important;
        border-radius: 12px !important;
        padding: 0.2rem 0.8rem !important;
        transition: all 0.3s ease !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1) !important;
    }

    section[data-testid="stSidebar"] .stCheckbox > div {
        border-radius: 6px !important;
        padding: 0.2rem !important;
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
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.4);
    }

    .sidebar-footer {
        padding: 0.8rem;
        margin-top: 1.5rem;
        text-align: center;
        border-top: 1px solid var(--gray-lighter);
        font-size: 0.7rem;
        color: var(--gray);
    }

    .sidebar-footer strong {
        color: var(--primary);
        font-weight: 600;
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
        background: var(--gradient-primary);
    }

    .hero-section::after {
        content: 'analytics';
        font-family: 'Material Icons';
        position: absolute;
        bottom: -30px;
        right: -30px;
        font-size: 10rem;
        opacity: 0.02;
        transform: rotate(-15deg);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-family: 'Space Grotesk', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }

    .hero-subtitle {
        color: var(--gray);
        font-size: 1rem;
        margin: 0.8rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
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

    /* ===== CARTES DES APPLICATIONS REDIMENSIONNÉES ===== */
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
        width: 3px;
        height: 100%;
        background: var(--gradient-primary);
        transition: width 0.3s ease;
    }

    .app-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(67, 97, 238, 0.1);
        border-color: var(--primary-light);
    }

    .app-card:hover::before {
        width: 4px;
    }

    .app-icon {
        font-size: 2.2rem;
        margin-bottom: 0.8rem;
        color: var(--primary);
    }

    .app-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--dark);
        margin-bottom: 0.6rem;
        font-family: 'Space Grotesk', sans-serif;
        display: flex;
        align-items: center;
        gap: 8px;
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

    .app-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        color: var(--white);
        margin-top: 0.6rem;
    }

    .badge-primary {
        background: var(--gradient-primary);
    }

    .badge-success {
        background: var(--gradient-success);
    }

    /* ===== SECTION RÉALISATEUR REDIMENSIONNÉE ===== */
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

    .author-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 80px;
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.03) 0%, rgba(114, 9, 183, 0.03) 100%);
        border-radius: 20px 20px 50% 50%;
    }

    .author-section::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(135deg, #f72585, #b5179e);
    }

    .author-avatar {
        position: relative;
        width: 90px;
        height: 90px;
        margin: 0 auto 0.8rem auto;
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
        font-size: 3rem;
        filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
    }

    .author-badge-container {
        margin-bottom: 0.6rem;
    }

    .author-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        background: linear-gradient(135deg, rgba(67, 97, 238, 0.1), rgba(114, 9, 183, 0.1));
        color: #4361ee;
        font-size: 0.7rem;
        font-weight: 600;
        border-radius: 30px;
        border: 1px solid rgba(67, 97, 238, 0.3);
        backdrop-filter: blur(5px);
        letter-spacing: 0.5px;
    }

    .author-name {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4361ee, #7209b7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.2rem 0 0.1rem 0;
        font-family: 'Space Grotesk', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    .author-title {
        color: #64748b;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
        font-weight: 400;
        position: relative;
        display: inline-block;
    }

    .author-title::after {
        content: '';
        position: absolute;
        bottom: -6px;
        left: 25%;
        width: 50%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4361ee, #7209b7, transparent);
    }

    .author-stats {
        display: flex;
        justify-content: space-around;
        margin: 1.2rem 0;
        padding: 0.8rem 0;
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
        font-size: 1.2rem;
        font-weight: 700;
        color: #4361ee;
        line-height: 1;
    }

    .author-stats .stat-label {
        font-size: 0.6rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
    }

    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        justify-content: center;
        margin: 1rem 0;
    }

    .skill-tag {
        background: #f1f5f9;
        color: #334155;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 500;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 4px;
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
        gap: 0.6rem;
        margin: 1.2rem 0;
        flex-wrap: wrap;
    }

    .social-link {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.4rem 1rem;
        border-radius: 30px;
        background: #f8fafc;
        color: #334155;
        text-decoration: none;
        font-size: 0.8rem;
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .social-link:hover {
        background: linear-gradient(135deg, #4361ee, #7209b7);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.25);
        border-color: transparent;
    }

    .social-icon {
        font-size: 1rem;
    }

    .social-text {
        font-weight: 500;
        font-size: 0.75rem;
    }

    .author-quote {
        margin: 1.2rem 0 0.8rem 0;
        padding: 0.8rem;
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        border-radius: 16px;
        border-left: 3px solid #4361ee;
        color: #475569;
        font-style: italic;
        font-size: 0.8rem;
        line-height: 1.5;
        position: relative;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .quote-mark {
        color: #4361ee;
        font-size: 1rem;
        font-weight: 700;
        opacity: 0.5;
    }

    .author-footer {
        margin-top: 1rem;
        padding-top: 0.8rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.7rem;
        color: #64748b;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
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

    /* ===== STATS CARDS REDIMENSIONNÉES ===== */
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
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
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
        background: var(--gradient-primary);
    }

    .footer::after {
        content: 'code';
        font-family: 'Material Icons';
        position: absolute;
        bottom: -10px;
        right: -10px;
        font-size: 3rem;
        opacity: 0.03;
        transform: rotate(10deg);
    }

    /* ===== BOUTONS PRINCIPAUX ===== */
    .stButton > button {
        background: var(--gradient-primary);
        color: var(--white);
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67, 97, 238, 0.3);
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .app-title {
            font-size: 1.2rem;
        }

        .app-card {
            padding: 1rem;
        }

        .stat-card {
            padding: 1rem;
        }

        .stat-number {
            font-size: 1.4rem;
        }

        .author-avatar {
            width: 70px;
            height: 70px;
        }

        .author-avatar-icon {
            font-size: 2.5rem;
        }

        .author-name {
            font-size: 1.4rem;
        }

        .social-link {
            padding: 0.3rem 0.8rem;
            font-size: 0.7rem;
        }
    }

    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR HARMONISÉE ---
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-header">
            <h3>
                {icon('dashboard', variant='sharp', size=28)} Menu
            </h3>
            <p>Navigation et paramètres</p>
        </div>
    """, unsafe_allow_html=True)

    # Section Navigation
    st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>{icon('explore', size=16, color='white')}</span> Navigation
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">{icon('home', size=18)}</span>
                <span>Accueil</span>
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">{icon('bar_chart', size=18)}</span>
                <span>Data Quality Analyzer</span>
            </div>
            <div class="sidebar-item">
                <span class="sidebar-item-icon">{icon('scatter_plot', size=18)}</span>
                <span>PCA Vision Pro</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Section Applications
    st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>{icon('apps', size=16, color='white')}</span> Applications
            </div>
    """, unsafe_allow_html=True)

    if st.button(f"{icon('bar_chart', size=16)} Lancer Data Quality", use_container_width=True, key="sidebar_data"):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button(f"{icon('scatter_plot', size=16)} Lancer PCA Vision", use_container_width=True, key="sidebar_pca"):
        st.switch_page("pages/app_acp_v2.py")

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Paramètres
    st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>{icon('settings', size=16, color='white')}</span> Paramètres
            </div>
    """, unsafe_allow_html=True)

    theme = st.selectbox("Thème", ["Clair", "Sombre"], key="sidebar_theme")
    notifications = st.checkbox("Notifications", value=True)
    autosave = st.checkbox("Sauvegarde auto", value=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Section Informations
    st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                <span>{icon('info', size=16, color='white')}</span> Informations
            </div>
            <div style='padding: 0.4rem 0; color: #334155; font-size: 0.85rem;'>
                <p><strong>Version:</strong> 4.0</p>
                <p><strong>Mise à jour:</strong> Fév 2026</p>
                <p><strong>Auteur:</strong> Gana Faye</p>
            </div>
            <div style='display: flex; flex-wrap: wrap; gap: 0.2rem; margin-top: 0.4rem;'>
                <span class='sidebar-badge'>{icon('code', size=12)} Python</span>
                <span class='sidebar-badge'>{icon('dashboard', size=12)} Streamlit</span>
                <span class='sidebar-badge'>{icon('smart_toy', size=12)} ML</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Footer de la sidebar
    st.markdown(f"""
        <div class="sidebar-footer">
            <strong>Data & Image Hub</strong><br>
            <span style='font-size: 0.6rem; display: flex; align-items: center; justify-content: center; gap: 4px;'>
                {icon('copyright', size=12)} 2026 Gana Faye
            </span>
        </div>
    """, unsafe_allow_html=True)

# --- INITIALISATION DU SESSION STATE ---
if 'df_analyse' not in st.session_state:
    st.session_state.df_analyse = None
if 'image_grise' not in st.session_state:
    st.session_state.image_grise = None

# --- BANNIÈRE PRINCIPALE ---
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-title">
            {icon('analytics', variant='sharp', size=48)} Data & Image Analytics Hub
        </h1>
        <p class="hero-subtitle">
            {icon('insights', size=20, color='#64748b')} La plateforme ultime pour l'analyse de données et d'images
        </p>
        <div style='display: flex; justify-content: center; gap: 0.8rem; flex-wrap: wrap; margin-top: 1.5rem;'>
            <span class='tech-badge'>{icon('code', size=16)} Python 3.12</span>
            <span class='tech-badge'>{icon('dashboard', size=16)} Streamlit</span>
            <span class='tech-badge'>{icon('smart_toy', size=16)} Scikit-learn</span>
            <span class='tech-badge'>{icon('table_chart', size=16)} Pandas</span>
            <span class='tech-badge'>{icon('image', size=16)} OpenCV</span>
            <span class='tech-badge'>{icon('show_chart', size=16)} Plotly</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SECTION DES APPLICATIONS ---
st.markdown(f"## {icon('apps', size=28)} Nos Applications", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class='app-card'>
            <div class='app-icon'>{icon('bar_chart', variant='sharp', size=40, color='#4361ee')}</div>
            <h2 class='app-title'>
                {icon('bar_chart', size=24)} Data Quality Analyzer
            </h2>
            <p class='app-description'>Analyse intelligente de la qualité des données avec recommandations ML.</p>
            <ul class='feature-list'>
                <li>{icon('category', size=16)} Classification automatique</li>
                <li>{icon('emergency', size=16)} Détection des outliers</li>
                <li>{icon('build', size=16)} Feature engineering</li>
                <li>{icon('download', size=16)} Export de rapports</li>
            </ul>
            <span class='app-badge badge-primary'>
                {icon('smart_toy', size=14)} Machine Learning
            </span>
        </div>
    """, unsafe_allow_html=True)

    if st.button(f"{icon('rocket_launch', size=16)} Lancer Data Quality Analyzer", key="btn_data",
                 use_container_width=True):
        st.switch_page("pages/analyse_data_traitement.py")

with col2:
    st.markdown(f"""
        <div class='app-card'>
            <div class='app-icon'>{icon('scatter_plot', variant='sharp', size=40, color='#4361ee')}</div>
            <h2 class='app-title'>
                {icon('scatter_plot', size=24)} PCA Vision Pro
            </h2>
            <p class='app-description'>Analyse d'images par décomposition en composantes principales.</p>
            <ul class='feature-list'>
                <li>{icon('compress', size=16)} Compression intelligente</li>
                <li>{icon('analytics', size=16)} Analyse de variance</li>
                <li>{icon('layers', size=16)} Tests multi-niveaux</li>
                <li>{icon('table_chart', size=16)} Matrice comparative</li>
            </ul>
            <span class='app-badge badge-success'>
                {icon('image', size=14)} Traitement d'images
            </span>
        </div>
    """, unsafe_allow_html=True)

    if st.button(f"{icon('rocket_launch', size=16)} Lancer PCA Vision Pro", key="btn_pca", use_container_width=True):
        st.switch_page("pages/app_acp_v2.py")

# --- SECTION RÉALISATEUR COMPLÈTE ---
st.markdown(f"""
    <div class='author-section'>
        <div class='author-avatar'>
            <span class='author-avatar-icon'>{icon('school', variant='sharp', size=48)}</span>
        </div>
        <div class='author-badge-container'>
            <span class='author-badge'>{icon('school', size=12)} Master 1 - Système d'Information</span>
        </div>
        <h2 class='author-name'>
            {icon('person', size=28)} Gana Faye
        </h2>
        <div class='author-title'>Data Scientist & Passionné par l'IA</div>
""", unsafe_allow_html=True)

# --- STATISTIQUES RAPIDES ---
st.markdown(f"""
    <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin: 2rem 0;'>
        <div class='stat-card'>
            <div class='stat-number'>2</div>
            <div class='stat-label'>{icon('apps', size=14)} Applications</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>20+</div>
            <div class='stat-label'>{icon('stars', size=14)} Fonctionnalités</div>
        </div>
        <div class='stat-card'>
            <div class='stat-number'>10+</div>
            <div class='stat-label'>{icon('description', size=14)} Types de fichiers</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- COMPLÉMENT SECTION RÉALISATEUR ---
st.markdown(f"""
        <div class='skills-container'>
            <span class='skill-tag'>{icon('code', size=12)} Python</span>
            <span class='skill-tag'>{icon('dashboard', size=12)} Streamlit</span>
            <span class='skill-tag'>{icon('data_usage', size=12)} Pandas</span>
            <span class='skill-tag'>{icon('smart_toy', size=12)} Scikit-learn</span>
            <span class='skill-tag'>{icon('image', size=12)} OpenCV</span>
            <span class='skill-tag'>{icon('show_chart', size=12)} Plotly</span>
            <span class='skill-tag'>{icon('storage', size=12)} SQL</span>
            <span class='skill-tag'>{icon('insights', size=12)} DataViz</span>
        </div>

        <div class='social-links'>
            <a href='https://github.com' target='_blank' class='social-link'>
                <span class='social-icon'>{icon('code', size=18)}</span>
                <span class='social-text'>GitHub</span>
            </a>
            <a href='https://linkedin.com' target='_blank' class='social-link'>
                <span class='social-icon'>{icon('work', size=18)}</span>
                <span class='social-text'>LinkedIn</span>
            </a>
            <a href='mailto:contact@example.com' class='social-link'>
                <span class='social-icon'>{icon('email', size=18)}</span>
                <span class='social-text'>Email</span>
            </a>
        </div>

        <div class='author-quote'>
            <span class='quote-mark'>{icon('format_quote', size=24)}</span>
            "Transformer les données en insights, une ligne à la fois"
        </div>

        <div class='author-footer'>
            <span class='institution'>{icon('school', size=12)} UCAD</span>
            <span class='separator'>•</span>
            <span class='promo'>{icon('calendar_today', size=12)} Promo 2026</span>
            <span class='separator'>•</span>
            <span class='promo'>{icon('emoji_events', size=12)} Data Scientist</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER AVEC COPYRIGHT DYNAMIQUE ---
current_year = datetime.now().year
st.markdown(f"""
    <div class='footer'>
        <strong>{icon('rocket_launch', size=16)} Data & Image Analytics Hub</strong> · Conçu avec passion par Gana Faye<br>
        <span style='opacity: 0.7; font-size: 0.7rem; display: flex; align-items: center; justify-content: center; gap: 4px;'>
            {icon('copyright', size=12)} {current_year} - Tous droits réservés · Version 4.0
        </span>
    </div>
""", unsafe_allow_html=True)