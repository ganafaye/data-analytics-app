import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Data & Image Analytics Hub | Gana Faye",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS (repris de votre application) ---
st.markdown("""
    <style>
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Style général avec dégradé élégant */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #9f7aea 100%);
        background-size: 200% 200%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* En-tête principal */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2.5rem 3rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
    }

    .main-header::after {
        content: '🚀';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.05;
        transform: rotate(-15deg);
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #9f7aea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-subtitle {
        color: #4a5568;
        font-size: 1.2rem;
        margin-top: 1rem;
        font-weight: 300;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.03);
    }

    section[data-testid="stSidebar"] > div {
        background: white;
    }

    .sidebar-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem 1.5rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .sidebar-header::after {
        content: '🚀';
        position: absolute;
        bottom: -15px;
        right: -15px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(10deg);
    }

    .sidebar-header h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        color: white;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .sidebar-header p {
        opacity: 0.9;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
    }

    .sidebar-section {
        background: #f8fafc;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 1rem 0;
        border: 1px solid #e2e8f0;
    }

    .sidebar-section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Cartes des applications */
    .app-card {
        background: white;
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.1);
        height: 100%;
        transition: all 0.3s ease;
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
        background: linear-gradient(135deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }

    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
        border-color: #667eea;
    }

    .app-card:hover::before {
        width: 6px;
    }

    .app-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .app-description {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }

    .feature-list {
        list-style: none;
        padding: 0;
        margin: 1.5rem 0;
    }

    .feature-list li {
        padding: 0.5rem 0;
        color: #4a5568;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-size: 0.95rem;
        border-bottom: 1px dashed #e2e8f0;
    }

    .feature-list li:last-child {
        border-bottom: none;
    }

    .feature-list li::before {
        content: "✓";
        color: #48bb78;
        font-weight: bold;
        font-size: 1.1rem;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
        width: 100%;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
    }

    /* Section auteur */
    .author-section {
        background: white;
        padding: 2.5rem;
        border-radius: 30px;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.1);
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .author-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
    }

    .author-name {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .author-title {
        color: #4a5568;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }

    .author-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: linear-gradient(135deg, #667eea15, #764ba215);
        color: #667eea;
        font-size: 0.9rem;
        font-weight: 600;
        border-radius: 30px;
        border: 1px solid rgba(102, 126, 234, 0.3);
        margin-bottom: 1rem;
    }

    /* Statistiques */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .stat-item {
        text-align: center;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }

    .stat-label {
        color: #718096;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: white;
        border-radius: 30px 30px 0 0;
        margin-top: 3rem;
        color: #4a5568;
        font-size: 0.95rem;
        border-top: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
    }

    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.5rem;
        }

        .main-subtitle {
            font-size: 1rem;
        }

        .app-title {
            font-size: 1.5rem;
        }

        .author-name {
            font-size: 1.8rem;
        }

        .stats-container {
            gap: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>🚀 Navigation</h3>
            <p>Accédez aux applications</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                📍 Applications
            </div>
    """, unsafe_allow_html=True)

    # Boutons de navigation vers les applications
    if st.button("📊 Data Quality Analyzer", use_container_width=True):
        st.switch_page("pages/analyse_data_traitement.py")

    if st.button("🔬 PCA Vision Pro", use_container_width=True):
        st.switch_page("pages/app_acp_v2.py")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">
                ⚙️ Informations
            </div>
            <div style='padding: 0.5rem 0; color: #4a5568;'>
                <p><strong>Version:</strong> 4.0</p>
                <p><strong>Mise à jour:</strong> Fév 2026</p>
                <p><strong>Auteur:</strong> Gana Faye</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- EN-TÊTE PRINCIPAL ---
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🚀 Data & Image Analytics Hub</h1>
        <p class="main-subtitle">
            Accélérez vos découvertes avec des outils de pointe pour l'analyse de données complexes et la vision par ordinateur.
        </p>
    </div>
""", unsafe_allow_html=True)

# --- SECTION DES APPLICATIONS ---
st.markdown("## 📱 Nos Applications")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="app-card">
            <div class="app-icon">📊</div>
            <h2 class="app-title">DATA QUALITY ANALYZER</h2>
            <p class="app-description">
                Analyse intelligente de la qualité des données avec recommandations ML intégrées et automatisation du pipeline.
            </p>
            <ul class="feature-list">
                <li>Classification automatique</li>
                <li>Détection des outliers</li>
                <li>Feature engineering avancé</li>
                <li>Export de rapports PDF</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    if st.button("📊 Lancer l'analyseur →", key="btn_data"):
        st.switch_page("pages/analyse_data_traitement.py")

with col2:
    st.markdown("""
        <div class="app-card">
            <div class="app-icon">🔬</div>
            <h2 class="app-title">PCA VISION PRO Expert</h2>
            <p class="app-description">
                Décomposition matricielle intelligente pour l'analyse structurelle d'images haute résolution.
            </p>
            <ul class="feature-list">
                <li>Compression intelligente</li>
                <li>Analyse de variance 4K</li>
                <li>Tests multi-niveaux</li>
                <li>Matrice comparative</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔬 Ouvrir Vision Pro →", key="btn_pca"):
        st.switch_page("pages/app_acp_v2.py")

# --- SECTION AUTEUR ---
st.markdown("""
    <div class="author-section">
        <span class="author-badge">MASTER 1 - SYSTÈMES D'INFORMATION</span>
        <h2 class="author-name">Gana Faye</h2>
        <p class="author-title">Data Scientist & Passionné par l'IA</p>

        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">02</div>
                <div class="stat-label">APPLICATIONS</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">20+</div>
                <div class="stat-label">FONCTIONNALITÉS</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10+</div>
                <div class="stat-label">TYPES DE FICHIERS</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FOOTER ---
current_year = datetime.now().year
st.markdown(f"""
    <div class="footer">
        <strong>© {current_year} - Tous droits réservés • Version 4.0.0</strong>
    </div>
""", unsafe_allow_html=True)