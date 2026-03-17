import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from datetime import datetime
import folium
from streamlit_folium import folium_static
import random
import time
apply_custom_style()
# Vérifier l'autorisation dès le chargement
if not is_authorized():
    st.error("🚫 Accès refusé. Vous n'avez pas l'autorisation de consulter cette page directement.")
    st.info("Veuillez vous identifier sur la page d'accueil avec un email valide.")
    if st.button("Retour à l'accueil"):
        st.switch_page("home_app.py")
    st.stop() # Arrête le script ici !
# 1. Configuration de la page
st.set_page_config(
    page_title="Dashboard Prix Immo Sénégal v2.0",
    layout="wide",
    page_icon="🇸🇳",
    initial_sidebar_state="expanded"
)
# ============================================
# CONFIGURATION - THÈME DAKAR PREMIUM
# ============================================

st.set_page_config(
    page_title="Dash Prix Immo - Dakar Immobilier",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Palette de couleurs DAKAR améliorée
colors = {
    'soleil': '#FDB813',
    'ocean': '#1E88E5',
    'teranga': '#F28C38',
    'bougainvillier': '#E63E6B',
    'baobab': '#5D4037',
    'sable': '#F4E3B1',
    'vert_dakar': '#2E7D32',
    'indigo': '#3949AB',
    'night': '#0F172A',
    'turquoise': '#2DD4BF'
}

# CSS personnalisé - Version Premium avec marges ajustées
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Pacifico&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    .stApp {{
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }}

    /* Suppression des marges par défaut */
    .main .block-container {{
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }}

    /* Header Premium */
    .header-premium {{
        background: linear-gradient(135deg, {colors['night']} 0%, {colors['indigo']} 100%);
        padding: 2rem;
        border-radius: 30px;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        width: 100%;
    }}

    .header-premium::before {{
        content: "🌅";
        position: absolute;
        right: 20px;
        top: 20px;
        font-size: 6rem;
        opacity: 0.1;
        transform: rotate(10deg);
    }}

    .header-premium h1 {{
        font-family: 'Pacifico', cursive;
        font-size: 3.2rem;
        color: white;
        margin: 0;
        line-height: 1.2;
    }}

    .header-premium p {{
        color: rgba(255,255,255,0.8);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }}

    .header-badge {{
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.3);
    }}

    /* KPIs Modernes */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin: 1.5rem 0;
    }}

    .kpi-modern {{
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
        height: 100%;
    }}

    .kpi-modern::after {{
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, {colors['soleil']}20, {colors['ocean']}20);
        border-radius: 50%;
        transform: translate(30px, -30px);
    }}

    .kpi-modern:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -10px rgba(57, 73, 171, 0.15);
    }}

    .kpi-icon {{
        font-size: 2rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 1;
    }}

    .kpi-label {{
        color: #64748B;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }}

    .kpi-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {colors['night']};
        margin-bottom: 0.3rem;
    }}

    .kpi-trend {{
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.2rem 0.8rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 600;
    }}

    .trend-up {{
        background: #D1FAE5;
        color: #10B981;
    }}

    .trend-down {{
        background: #FEE2E2;
        color: #EF4444;
    }}

    /* Section Headers */
    .section-premium {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1.5rem 0 1rem 0;
    }}

    .section-premium h2 {{
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: {colors['night']};
        font-size: 1.5rem;
        margin: 0;
    }}

    .section-badge {{
        background: {colors['soleil']};
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
    }}

    /* Cards de contenu */
    .content-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.02);
        height: 100%;
        transition: box-shadow 0.3s;
        margin-bottom: 1.5rem;
        width: 100%;
    }}

    .content-card:hover {{
        box-shadow: 0 20px 40px -10px rgba(57, 73, 171, 0.1);
    }}

    /* Stats mini-cards */
    .stat-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #F1F5F9;
    }}

    .stat-row:last-child {{
        border-bottom: none;
    }}

    /* Footer */
    .footer-premium {{
        text-align: center;
        padding: 2rem;
        color: #94A3B8;
        font-size: 0.9rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
        background: white;
        border-radius: 30px 30px 0 0;
        width: 100%;
    }}

    /* Animation pour les cartes */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animated-card {{
        animation: fadeIn 0.5s ease-out;
    }}

    /* Carte pleine largeur */
    .full-width-map {{
        width: 100%;
        margin: 0;
        padding: 0;
    }}

    /* Ajustement des colonnes */
    div[data-testid="column"] {{
        padding: 0 0.5rem;
    }}

    /* Sidebar */
    .css-1d391kg {{
        background-color: white;
    }}
    /* Cards de contenu */
    .content-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.02);
        height: 100%;
        transition: box-shadow 0.3s;
        margin-bottom: 1.5rem;
        width: 100%;
    }}

    .content-card:hover {{
        box-shadow: 0 20px 40px -10px rgba(57, 73, 171, 0.1);
    }}

    /* Options cards */
    .option-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #E2E8F0;
        text-align: center;
        height: 100%;
        transition: transform 0.2s;
    }}

    .option-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px -10px rgba(57, 73, 171, 0.1);
    }}

    .option-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}

    .option-label {{
        font-weight: 600;
        color: {colors['night']};
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }}

    .option-value {{
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }}

    .value-green {{ color: #10B981; }}
    .value-blue {{ color: #3B82F6; }}
    .value-purple {{ color: #8B5CF6; }}

    .option-sub {{
        color: #64748B;
        font-size: 0.9rem;
    }}

    /* Footer */
    .footer-premium {{
        text-align: center;
        padding: 2rem;
        color: #94A3B8;
        font-size: 0.9rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 2rem;
        background: white;
        border-radius: 30px 30px 0 0;
        width: 100%;
    }}

    /* Sources */
    .sources {{
        background: #F3F4F6;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        font-size: 0.9rem;
        color: #4B5563;
        margin: 2rem 0;
        border-left: 4px solid {colors['soleil']};
    }}

    /* Ajustement des colonnes */
    div[data-testid="column"] {{
        padding: 0 0.5rem;
    }}

    /* Sidebar */
    .css-1d391kg {{
        background-color: white;
    }}
</style>
""", unsafe_allow_html=True)
st.markdown("""
        <style>
            /* 1. MASQUER LA NAVIGATION NATIVE (La liste des fichiers .py) */
            [data-testid="stSidebarNav"] {
                display: none;
            }

            /* 2. AJUSTEMENT DE L'ESPACE SUPÉRIEUR */
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 0rem;
            }

            /* 3. STYLE DES TITRES DE CATÉGORIES (IA, Outils, Dashboards) */
            .sidebar-section-title {
                font-weight: 700;
                color: #1e293b;
                margin-top: 1.2rem;
                margin-bottom: 0.6rem;
                padding-left: 0.5rem;
                border-left: 4px solid #2563eb; /* Barre bleue distinctive */
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.03em;
            }

            /* 4. STYLE DES BOUTONS DE NAVIGATION */
            .stButton > button {
                width: 100%;
                border-radius: 10px;
                text-align: left;
                padding: 0.6rem 1rem;
                border: 1px solid #e2e8f0;
                background-color: #ffffff;
                color: #334155;
                font-weight: 500;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
            }

            .stButton > button:hover {
                border-color: #2563eb;
                background-color: #f1f5f9;
                color: #2563eb;
                transform: translateX(3px); /* Petit effet de mouvement au survol */
            }

            /* 5. STYLE DES BADGES ET DU FOOTER */
            .sidebar-badge {
                background: #e2e8f0;
                color: #475569;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 0.7rem;
                font-weight: 600;
            }

            .sidebar-footer {
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid #e2e8f0;
                font-size: 0.75rem;
                color: #94a3b8;
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        'dashboard/dakar_immobilier_clean_dashboard.csv')
    df['prix_m2'] = df['prix'] / df['surface_m2']
    df['prix_million'] = df['prix'] / 1_000_000

    # Catégorisation des biens
    df['type_bien'] = df['titre'].apply(lambda x:
                                        'Villa' if 'villa' in str(x).lower() else
                                        'Studio' if 'studio' in str(x).lower() else
                                        'Appartement' if 'appartement' in str(x).lower() else
                                        'Autre'
                                        )

    return df, None


df, _ = load_data()


@st.cache_resource
def load_model():
    try:
        data = joblib.load('./models/modele_champion_55.pkl')
        return data['model'], data['features'], data['performance']
    except:
        return None, None, {'r2': 0.55, 'mae': 256845}


model, features, perf = load_model()


# ============================================
# FONCTION POUR CRÉER LES STATS PAR QUARTIER
# ============================================

def get_quartier_stats(df):
    # Coordonnées réelles des quartiers de Dakar
    quartier_coords_reelles = {
        'Almadies': [14.7405, -17.5308],
        'Mermoz': [14.7137, -17.4817],
        'Point E': [14.7002, -17.4614],
        'Fann': [14.6928, -17.4772],
        'Fann Résidence': [14.6928, -17.4772],
        'Yoff': [14.7541, -17.4745],
        'Ngor': [14.7561, -17.5143],
        'Ouakam': [14.7194, -17.4939],
        'Plateau': [14.6701, -17.4386],
        'Sicap': [14.7050, -17.4550],
        'Sicap Liberté': [14.7050, -17.4550],
        'Liberté': [14.7150, -17.4650],
        'Liberté 6': [14.7150, -17.4650],
        'Grand Dakar': [14.6950, -17.4450],
        'HLM': [14.6850, -17.4500],
        'Médina': [14.6750, -17.4600],
        'Fass': [14.6650, -17.4700],
        'Gueule Tapée': [14.6550, -17.4800],
        'Colobane': [14.6450, -17.4900],
        'Parcelles Assainies': [14.7350, -17.4550],
        'Grand Yoff': [14.7250, -17.4650],
        'Dieuppeul': [14.7150, -17.4450],
        'Mamelles': [14.7350, -17.5150],
        'Cité Keur Gorgui': [14.7050, -17.4750],
        'Sacré Cœur': [14.6950, -17.4550],
        'Fann Hock': [14.6900, -17.4750],
        'Hann Maristes': [14.7150, -17.4350],
        'Thiaroye': [14.7350, -17.4150],
        'Pikine': [14.7450, -17.4050],
        'Guediawaye': [14.7550, -17.3950],
        'Rufisque': [14.7150, -17.2650],
        'Keur Massar': [14.7750, -17.3450],
        'Diamniadio': [14.7150, -17.1950],
        'Saly': [14.4450, -17.1050],
        'Mbour': [14.4050, -16.9650],
        'Thiès': [14.7850, -16.9250],
        'Autre': [14.7167, -17.4677]
    }

    # Ajout des coordonnées au dataframe
    df_copy = df.copy()
    df_copy['lat'] = df_copy['quartier'].map(lambda x: quartier_coords_reelles.get(x, [14.7167, -17.4677])[0])
    df_copy['lon'] = df_copy['quartier'].map(lambda x: quartier_coords_reelles.get(x, [14.7167, -17.4677])[1])

    # Ajouter un peu de variation pour éviter que tous les points soient superposés
    np.random.seed(42)
    df_copy['lat'] = df_copy['lat'] + np.random.randn(len(df_copy)) * 0.005
    df_copy['lon'] = df_copy['lon'] + np.random.randn(len(df_copy)) * 0.005

    # Calcul des stats par quartier
    quartier_stats = df_copy.groupby('quartier').agg({
        'prix': ['mean', 'median', 'count', 'std'],
        'prix_m2': 'mean',
        'surface_m2': 'mean',
        'lat': 'mean',
        'lon': 'mean'
    }).round(0)
    quartier_stats.columns = ['prix_moyen', 'prix_median', 'nb_annonces', 'prix_std', 'prix_m2_moyen',
                              'surface_moyenne', 'lat', 'lon']
    quartier_stats = quartier_stats.reset_index()
    quartier_stats['color_intensity'] = (quartier_stats['prix_moyen'] - quartier_stats['prix_moyen'].min()) / (
            quartier_stats['prix_moyen'].max() - quartier_stats['prix_moyen'].min())

    return quartier_stats, df_copy


# ============================================
# SIDEBAR - INFOS MODÈLE
# ============================================

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 3rem;'>🌅</div>
        <h3 style='color: #0F172A;'>Yaka Nangu</h3>
        <p style='color: #64748B; font-size: 0.9rem;'>Version 2.0 Premium</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🎯 FILTRES RAPIDES")

    # Sélecteur de quartiers avec compteur
    quartier_counts = df['quartier'].value_counts()
    quartier_options = [f"{q} ({quartier_counts[q]} annonces)" for q in sorted(df['quartier'].unique())]
    selected_quartiers_idx = st.multiselect(
        "Quartiers",
        options=range(len(quartier_options)),
        format_func=lambda x: quartier_options[x],
        default=[0, 1, 2, 3, 4][:min(5, len(quartier_options))]
    )
    selected_quartiers = [sorted(df['quartier'].unique())[i] for i in selected_quartiers_idx]

    # Sliders de filtrage
    prix_min, prix_max = st.slider(
        "Prix (millions FCFA)",
        0.0, 5.0, (0.5, 2.0)
    )

    surface_min, surface_max = st.slider(
        "Surface (m²)",
        0, 500, (30, 200)
    )

    # Options
    st.markdown("### Options")
    col1, col2 = st.columns(2)
    with col1:
        meuble_filter = st.checkbox("Meublé")
        vue_mer_filter = st.checkbox("Vue mer")
    with col2:
        neuf_filter = st.checkbox("Neuf")

    # Stats en direct
    st.markdown("---")

    # Application des filtres pour le compteur
    mask_sidebar = (df['prix_million'] >= prix_min) & (df['prix_million'] <= prix_max) & \
                   (df['surface_m2'] >= surface_min) & (df['surface_m2'] <= surface_max)
    if selected_quartiers:
        mask_sidebar &= df['quartier'].isin(selected_quartiers)
    if meuble_filter:
        mask_sidebar &= df['meuble'] == 1
    if vue_mer_filter:
        mask_sidebar &= df['vue_mer'] == 1
    if neuf_filter:
        mask_sidebar &= df['neuf'] == 1

    df_sidebar_filtered = df[mask_sidebar]

    st.markdown(f"""
    <div style='background: #F8FAFC; padding: 1rem; border-radius: 15px;'>
        <p style='color: #0F172A; font-weight: 600; margin: 0;'>📊 Annonces filtrées</p>
        <p style='font-size: 2rem; font-weight: 700; color: {colors['ocean']}; margin: 0;'>{len(df_sidebar_filtered)}</p>
        <p style='color: #64748B; font-size: 0.9rem;'>sur {len(df)} total</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER PREMIUM
# ============================================

st.markdown("""
<div class='header-premium'>
    <span class='header-badge'>🇸🇳 MARKET INTELLIGENCE V2.0</span>
    <h1>Dashboard des prix loyer des appartements à • Dakar</h1>
    <p>Analyse intelligente du marché immobilier • Données temps réel • </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# KPIS MODERNES
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-modern'>
        <div class='kpi-icon'>💰</div>
        <div class='kpi-label'>Loyer moyen</div>
        <div class='kpi-value'>{df['prix'].mean():,.0f}</div>
        <span class='kpi-trend trend-up'>↑ 5.2%</span>
        <span style='color: #64748B; margin-left: 0.5rem;'>FCFA</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-modern'>
        <div class='kpi-icon'>📏</div>
        <div class='kpi-label'>Prix au m²</div>
        <div class='kpi-value'>{df['prix_m2'].mean():,.0f}</div>
        <span class='kpi-trend trend-up'>↑ 3.8%</span>
        <span style='color: #64748B; margin-left: 0.5rem;'>FCFA/m²</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    top_quartier = df.groupby('quartier')['prix'].mean().idxmax()
    top_prix = df.groupby('quartier')['prix'].mean().max()
    st.markdown(f"""
    <div class='kpi-modern'>
        <div class='kpi-icon'>🏆</div>
        <div class='kpi-label'>Quartier premium</div>
        <div class='kpi-value'>{top_quartier}</div>
        <span style='color: #64748B;'>{top_prix:,.0f} FCFA</span>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-modern'>
        <div class='kpi-icon'>📊</div>
        <div class='kpi-label'>Annonces actives</div>
        <div class='kpi-value'>{len(df):,}</div>
        <span style='color: #64748B;'>{df['quartier'].nunique()} quartiers</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SECTION ANALYSE PRINCIPALE
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>📈 Analyse du marché</h2>
    <span class='section-badge'>Temps réel</span>
</div>
""", unsafe_allow_html=True)

# Application des filtres
mask = (df['prix_million'] >= prix_min) & (df['prix_million'] <= prix_max) & \
       (df['surface_m2'] >= surface_min) & (df['surface_m2'] <= surface_max)

if selected_quartiers:
    mask &= df['quartier'].isin(selected_quartiers)
if meuble_filter:
    mask &= df['meuble'] == 1
if vue_mer_filter:
    mask &= df['vue_mer'] == 1
if neuf_filter:
    mask &= df['neuf'] == 1

df_filtered = df[mask]

# Obtenir les stats à jour
quartier_stats, df_with_coords = get_quartier_stats(df_filtered)

# ============================================
# PREMIÈRE LIGNE DE GRAPHIQUES (3 graphiques)
# ============================================

col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("<div class='content-card animated-card'>", unsafe_allow_html=True)
    st.markdown("#### 🏘️ Top 5 quartiers par prix")

    top5_prix = quartier_stats.nlargest(5, 'prix_moyen')[['quartier', 'prix_moyen', 'prix_m2_moyen']]

    fig = px.bar(
        top5_prix,
        x='prix_moyen',
        y='quartier',
        orientation='h',
        color='prix_moyen',
        color_continuous_scale=['#FDB813', '#E63E6B', '#1E88E5'],
        text=[f"{x:,.0f} FCFA" for x in top5_prix['prix_moyen']],
        title=""
    )

    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#E2E8F0', title=""),
        yaxis=dict(gridcolor='#E2E8F0', title=""),
        showlegend=False,
        margin=dict(l=10, r=30, t=10, b=10)
    )
    fig.update_traces(textposition='outside')

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_g2:
    st.markdown("<div class='content-card animated-card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Distribution des prix")

    fig = px.histogram(
        df_filtered,
        x='prix_million',
        nbins=20,
        color_discrete_sequence=[colors['turquoise']],
        marginal='box',
        labels={'prix_million': 'Prix (millions FCFA)'}
    )

    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        xaxis=dict(gridcolor='#E2E8F0'),
        yaxis=dict(gridcolor='#E2E8F0', title="Nombre d'annonces"),
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_g3:
    st.markdown("<div class='content-card animated-card'>", unsafe_allow_html=True)
    st.markdown("#### 🥧 Répartition par type")

    type_counts = df_filtered['type_bien'].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=type_counts.index,
        values=type_counts.values,
        hole=0.5,
        marker=dict(colors=[colors['ocean'], colors['soleil'], colors['bougainvillier'], colors['teranga']]),
        textinfo='label+percent',
        textposition='outside',
        pull=[0.05 if i == 0 else 0 for i in range(len(type_counts))]
    )])

    fig.update_layout(
        height=350,
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# CARTE INTERACTIVE PLEINE LARGEUR
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>🗺️ Carte interactive de Dakar</h2>
    <span class='section-badge'>Heatmap</span>
</div>
""", unsafe_allow_html=True)

# Carte sans card pour qu'elle prenne toute la largeur
from folium.plugins import HeatMap

# Centrer la carte sur Dakar
m = folium.Map(location=[14.7167, -17.4677], zoom_start=12, tiles='OpenStreetMap')

# Ajout des markers pour chaque annonce (échantillon pour ne pas surcharger)
sample_size = min(200, len(df_with_coords))
df_sample = df_with_coords.sample(sample_size)

for idx, row in df_sample.iterrows():
    # Déterminer la couleur selon le prix
    if row['prix'] > df_with_coords['prix'].quantile(0.75):
        color = '#E63E6B'  # rose pour les plus chers
    elif row['prix'] > df_with_coords['prix'].median():
        color = '#FDB813'  # jaune pour les moyens
    else:
        color = '#1E88E5'  # bleu pour les accessibles

    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        popup=f"<b>{row['quartier']}</b><br>{row['prix']:,.0f} FCFA<br>{row['surface_m2']}m²<br>{row['type_bien']}",
        tooltip=f"{row['quartier']} - {row['prix']:,.0f} FCFA",
        color=color,
        fill=True,
        fillColor=color,
        fillOpacity=0.6
    ).add_to(m)

# Ajout des marqueurs principaux pour chaque quartier
for idx, row in quartier_stats.iterrows():
    if not pd.isna(row['lat']) and not pd.isna(row['lon']):
        # Taille basée sur le nombre d'annonces
        radius = 8 + (row['nb_annonces'] / quartier_stats['nb_annonces'].max()) * 15

        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=radius,
            popup=folium.Popup(f"""
            <div style='font-family: Arial; min-width: 200px;'>
                <h4 style='margin:0; color:#0F172A;'>{row['quartier']}</h4>
                <hr style='margin:5px 0;'>
                <p><b>💰 Prix moyen:</b> {row['prix_moyen']:,.0f} FCFA</p>
                <p><b>📏 Prix/m²:</b> {row['prix_m2_moyen']:,.0f} FCFA</p>
                <p><b>📋 Annonces:</b> {row['nb_annonces']:.0f}</p>
                <p><b>📐 Surface moy.:</b> {row['surface_moyenne']:.0f} m²</p>
            </div>
            """, max_width=300),
            tooltip=f"🏙️ {row['quartier']}",
            color='#0F172A',
            weight=2,
            fill=True,
            fillColor='#2DD4BF',
            fillOpacity=0.7
        ).add_to(m)

# Ajout de la heatmap
heat_data = [[row['lat'], row['lon'], row['nb_annonces']] for idx, row in quartier_stats.iterrows() if
             not pd.isna(row['lat'])]
if heat_data:
    HeatMap(heat_data, radius=25, blur=15, max_zoom=13,
            gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(m)

# Affichage de la carte pleine largeur
folium_static(m, width=1200, height=550)

# Légende
st.markdown("""
<div style='display: flex; justify-content: center; gap: 2rem; margin: 1rem 0; font-size: 0.9rem; flex-wrap: wrap;'>
    <div><span style='color: #E63E6B;'>●</span> Quartiers premium (>75%)</div>
    <div><span style='color: #FDB813;'>●</span> Quartiers moyens (50-75%)</div>
    <div><span style='color: #1E88E5;'>●</span> Quartiers accessibles (<50%)</div>
    <div><span style='color: #2DD4BF;'>●</span> Taille = nombre d'annonces</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# TROISIÈME LIGNE - TOP 5 QUARTIERS AVEC ANIMATION
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>📍 Top 5 quartiers - Vue détaillée</h2>
    <span class='section-badge'>Animé</span>
</div>
""", unsafe_allow_html=True)

# Animation avec st.empty() pour faire défiler les quartiers
placeholder = st.empty()

# Récupérer les top 5 quartiers
top5_display = quartier_stats.nlargest(5, 'prix_moyen').to_dict('records')

for i in range(5):  # Boucle d'animation réduite
    for quartier in top5_display:
        with placeholder.container():
            st.markdown(f"""
            <div class='content-card animated-card' style='text-align: center; padding: 2rem; background: linear-gradient(135deg, {colors['indigo']}, {colors['night']}); color: white;'>
                <div style='font-size: 4rem; margin-bottom: 1rem;'>🏆</div>
                <h1 style='color: white; font-size: 3rem; margin: 0;'>{quartier['quartier']}</h1>
                <p style='font-size: 1.2rem; opacity: 0.9;'>Top {top5_display.index(quartier) + 1} des quartiers les plus chers</p>
                <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2rem; flex-wrap: wrap;'>
                    <div>
                        <p style='font-size: 0.9rem; opacity: 0.7;'>Prix moyen</p>
                        <p style='font-size: 2rem; font-weight: 700;'>{quartier['prix_moyen']:,.0f} FCFA</p>
                    </div>
                    <div>
                        <p style='font-size: 0.9rem; opacity: 0.7;'>Prix au m²</p>
                        <p style='font-size: 2rem; font-weight: 700;'>{quartier['prix_m2_moyen']:,.0f} FCFA</p>
                    </div>
                    <div>
                        <p style='font-size: 0.9rem; opacity: 0.7;'>Annonces</p>
                        <p style='font-size: 2rem; font-weight: 700;'>{quartier['nb_annonces']:.0f}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(1.2)
# Afficher le dernier quartier en statique

# ============================================
# SCATTER PLOT INTERACTIF
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>🎯 Relation Surface-Prix par quartier</h2>
    <span class='section-badge'>Analyse</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='content-card'>", unsafe_allow_html=True)

fig = px.scatter(
    df_filtered,
    x='surface_m2',
    y='prix',
    color='quartier',
    size='chambres',
    hover_data=['titre', 'type_bien'],
    trendline='ols',
    title=""
)

fig.update_layout(
    height=550,
    plot_bgcolor='white',
    xaxis=dict(gridcolor='#E2E8F0', title="Surface (m²)"),
    yaxis=dict(gridcolor='#E2E8F0', title="Prix (FCFA)"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# ✨ IMPACT DES OPTIONS (NOUVELLE SECTION)
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>✨ Impact des options</h2>
    <span class='section-badge'>Plus-value</span>
</div>
""", unsafe_allow_html=True)

# Calcul des impacts
prix_base = df[df['meuble']==0]['prix'].mean()
prix_meuble = df[df['meuble']==1]['prix'].mean()
prix_vue = df[df['vue_mer']==1]['prix'].mean()
prix_neuf = df[df['neuf']==1]['prix'].mean()

col_o1, col_o2, col_o3 = st.columns(3)

with col_o1:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🛋️</div>
        <div class='option-label'>Meublé</div>
        <div class='option-value value-green'>+{((prix_meuble/prix_base)-1)*100:.1f}%</div>
        <div class='option-sub'>{prix_meuble:,.0f} FCFA vs {prix_base:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

with col_o2:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🌊</div>
        <div class='option-label'>Vue mer</div>
        <div class='option-value value-blue'>+{((prix_vue/prix_base)-1)*100:.1f}%</div>
        <div class='option-sub'>{prix_vue:,.0f} FCFA vs {prix_base:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

with col_o3:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🏗️</div>
        <div class='option-label'>Neuf</div>
        <div class='option-value value-purple'>+{((prix_neuf/prix_base)-1)*100:.1f}%</div>
        <div class='option-sub'>{prix_neuf:,.0f} FCFA vs {prix_base:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# STATISTIQUES DÉTAILLÉES
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>📊 Statistiques par quartier</h2>
    <span class='section-badge'>Top 10</span>
</div>
""", unsafe_allow_html=True)

display = quartier_stats[['quartier', 'prix_moyen', 'prix_m2_moyen', 'surface_moyenne', 'nb_annonces']].copy()
display.columns = ['Quartier', 'Prix moyen', 'Prix/m²', 'Surface moy.', 'Annonces']
display = display.sort_values('Prix moyen', ascending=False).head(10)

st.dataframe(display, use_container_width=True, hide_index=True,
             column_config={
                 "Prix moyen": st.column_config.NumberColumn(format="%.0f FCFA"),
                 "Prix/m²": st.column_config.NumberColumn(format="%.0f FCFA"),
                 "Surface moy.": st.column_config.NumberColumn(format="%.0f m²"),
                 "Annonces": st.column_config.NumberColumn(format="%d")
             })

# ============================================
# 📋 DONNÉES DÉTAILLÉES (NOUVELLE SECTION)
# ============================================

st.markdown("""
<div class='section-premium'>
    <h2>📋 Données détaillées</h2>
    <span class='section-badge'>Explorer</span>
</div>
""", unsafe_allow_html=True)

with st.expander("🔍 Voir le tableau complet des annonces", expanded=False):
    st.dataframe(
        df_filtered[['titre', 'quartier', 'prix', 'surface_m2', 'chambres', 'meuble', 'vue_mer', 'neuf']].head(100),
        use_container_width=True,
        column_config={
            "prix": st.column_config.NumberColumn(format="%.0f FCFA"),
            "surface_m2": st.column_config.NumberColumn(format="%.0f m²")
        }
    )

# ============================================
# SOURCES DES DONNÉES
# ============================================

st.markdown("""
<div class='sources'>
    <b>📌 Sources des données :</b>
    <ul style='margin-top:0.5rem; margin-bottom:0;'>
        <li>Loger Dakar - Annonces immobilières</li>
        <li>Keur Immobilier - Base de données</li>
        <li>Expat Dakar - Annonces immobilières</li>
        <li>Dernière mise à jour : Mars 2026</li>
    </ul>
</div>
""", unsafe_allow_html=True)
# ============================================
# FOOTER PREMIUM
# ============================================

st.markdown(f"""
<div class='footer-premium'>
    <div style='margin-bottom: 1rem;'>
        <span style='margin: 0 1rem;'>🌅 Dashboard Prix Immo</span>
        <span style='margin: 0 1rem;'>|</span>
        <span style='margin: 0 1rem;'>|</span>
        <span style='margin: 0 1rem;'>|</span>
        <span style='margin: 0 1rem;'>📊 {len(df)} annonces</span>
    </div>
    <div style='opacity: 0.7; font-size: 0.9rem;'>
        Gana Faye • Master 1 Data Science 
    </div>
    <div style='margin-top: 1rem; font-size: 1.5rem; letter-spacing: 0.5rem;'>
        🇸🇳 🇸🇳 🇸🇳
    </div>
</div>
""", unsafe_allow_html=True)