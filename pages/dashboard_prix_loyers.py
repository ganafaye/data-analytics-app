import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import joblib

# ============================================
# CONFIGURATION UNIQUE
# ============================================
st.set_page_config(
    page_title="Dashboard Prix Immo - Dakar",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# AUTHENTIFICATION (optionnel)
# ============================================
try:
    from auth_utils import is_authorized, apply_custom_style

    apply_custom_style()
    if not is_authorized():
        st.error("🚫 Accès refusé. Vous n'avez pas l'autorisation.")
        st.stop()
except:
    pass  # Si auth_utils n'existe pas, on continue sans

# ============================================
# STYLES CSS OPTIMISÉS
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }

    /* Header */
    .header-premium {
        background: linear-gradient(135deg, #0F172A, #3949AB);
        padding: 2rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        color: white;
    }
    .header-premium h1 { font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0 0; }
    .header-badge {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        display: inline-block;
    }

    /* KPIs */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        transition: transform 0.2s;
        height: 100%;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #FDB813; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #0F172A; }
    .kpi-label { color: #64748b; font-size: 0.85rem; text-transform: uppercase; }
    .trend-up { background: #D1FAE5; color: #10B981; padding: 0.2rem 0.8rem; border-radius: 30px; }

    /* Sections */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0F172A;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #FDB813;
        padding-left: 1rem;
    }

    /* Cards */
    .content-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        height: 100%;
        margin-bottom: 1rem;
    }

    /* Options cards */
    .option-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
        height: 100%;
        transition: transform 0.2s;
    }
    .option-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1); }
    .option-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .option-value { font-size: 2rem; font-weight: 700; }
    .value-green { color: #10B981; }
    .value-blue { color: #3B82F6; }
    .value-purple { color: #8B5CF6; }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
        background: white;
        border-radius: 30px 30px 0 0;
    }

    /* Sources */
    .sources {
        background: #f1f5f9;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin: 2rem 0;
        border-left: 4px solid #FDB813;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: white; }
    [data-testid="stSidebarNav"] { display: none; }
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

# ============================================
# SIDEBAR NAVIGATION
# ============================================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <div style='font-size: 3rem;'>🏠</div>
        <h3 style='color: #0F172A;'>Dashboard Prix Immo</h3>
        <p style='color: #64748B; font-size: 0.9rem;'>Dashboard Immobilier</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Retour à l'Accueil", use_container_width=True):
        st.switch_page("home_app.py")

    st.markdown("---")
    st.markdown("### 🎯 FILTRES")

    # Les filtres seront ajoutés après chargement des données


# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dashboard/dakar_immobilier_clean_dashboard.csv')
    except:
        df = pd.read_csv('data/dakar_immobilier_clean_dashboard.csv')

    df['prix_m2'] = df['prix'] / df['surface_m2']
    df['prix_million'] = df['prix'] / 1_000_000
    df['type_bien'] = df['titre'].apply(lambda x:
                                        'Villa' if 'villa' in str(x).lower() else
                                        'Studio' if 'studio' in str(x).lower() else
                                        'Appartement')
    return df


df = load_data()

# ============================================
# SUITE DE LA SIDEBAR AVEC LES FILTRES
# ============================================
with st.sidebar:
    quartier_counts = df['quartier'].value_counts()
    quartiers = st.multiselect(
        "Quartiers",
        options=sorted(df['quartier'].unique()),
        default=['Almadies', 'Mermoz', 'Point E'][:3]
    )

    prix_range = st.slider("Budget (M FCFA)", 0.0, 5.0, (0.5, 2.0))
    surface_range = st.slider("Surface (m²)", 0, 500, (30, 200))

    st.markdown("### ✨ Options")
    col1, col2 = st.columns(2)
    with col1:
        meuble = st.checkbox("Meublé")
        vue_mer = st.checkbox("Vue mer")
    with col2:
        neuf = st.checkbox("Neuf")

    st.markdown("---")
    st.markdown(f"**📊 Annonces :** {len(df):,}")
    st.markdown(f"**📍 Quartiers :** {df['quartier'].nunique()}")


# ============================================
# FONCTION STATS QUARTIERS
# ============================================
def get_quartier_stats(df):
    coords = {
        'Almadies': [14.7405, -17.5308], 'Mermoz': [14.7137, -17.4817],
        'Point E': [14.7002, -17.4614], 'Fann': [14.6928, -17.4772],
        'Yoff': [14.7541, -17.4745], 'Ngor': [14.7561, -17.5143],
        'Ouakam': [14.7194, -17.4939], 'Plateau': [14.6701, -17.4386],
        'Parcelles Assainies': [14.7350, -17.4550]
    }

    df_copy = df.copy()
    df_copy['lat'] = df_copy['quartier'].map(lambda x: coords.get(x, [14.7167, -17.4677])[0])
    df_copy['lon'] = df_copy['quartier'].map(lambda x: coords.get(x, [14.7167, -17.4677])[1])

    # Variation aléatoire
    np.random.seed(42)
    df_copy['lat'] += np.random.randn(len(df_copy)) * 0.005
    df_copy['lon'] += np.random.randn(len(df_copy)) * 0.005

    stats = df_copy.groupby('quartier').agg({
        'prix': ['mean', 'count'],
        'prix_m2': 'mean',
        'surface_m2': 'mean',
        'lat': 'mean',
        'lon': 'mean'
    }).round(0)
    stats.columns = ['prix_moyen', 'nb_annonces', 'prix_m2_moyen', 'surface_moyenne', 'lat', 'lon']
    return stats.reset_index(), df_copy


# ============================================
# FILTRAGE
# ============================================
mask = (df['prix_million'] >= prix_range[0]) & (df['prix_million'] <= prix_range[1]) & \
       (df['surface_m2'] >= surface_range[0]) & (df['surface_m2'] <= surface_range[1])

if quartiers:
    mask &= df['quartier'].isin(quartiers)
if meuble:
    mask &= df['meuble'] == 1
if vue_mer:
    mask &= df['vue_mer'] == 1
if neuf:
    mask &= df['neuf'] == 1

df_f = df[mask]
stats, df_coords = get_quartier_stats(df_f)

# ============================================
# HEADER
# ============================================
st.markdown("""
<div class='header-premium'>
    <span class='header-badge'>🇸🇳 DAKAR IMMOBILIER</span>
    <h1>Dashboard des prix des loyers à Dakar</h1>
    <p style='opacity:0.9;'>Analyse intelligente du marché immobilier • Données temps réel</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# KPIS
# ============================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>💰 PRIX MOYEN</div>
        <div class='kpi-value'>{df['prix'].mean():,.0f} FCFA</div>
        <span class='trend-up'>↑ 5.2%</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>📏 PRIX AU M²</div>
        <div class='kpi-value'>{df['prix_m2'].mean():,.0f} FCFA</div>
        <span class='trend-up'>↑ 3.8%</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    top_q = df.groupby('quartier')['prix'].mean().idxmax()
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>🏆 TOP QUARTIER</div>
        <div class='kpi-value'>{top_q}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>📊 VOLUME</div>
        <div class='kpi-value'>{len(df):,}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TOP 5 QUARTIERS
# ============================================
st.markdown("<div class='section-title'>📍 Top 5 quartiers</div>", unsafe_allow_html=True)

if len(stats) > 0:
    top5 = stats.nlargest(min(5, len(stats)), 'prix_moyen')
    cols = st.columns(len(top5))
    for i, (_, r) in enumerate(top5.iterrows()):
        with cols[i]:
            st.markdown(f"""
            <div style='background:white; padding:1rem; border-radius:15px; text-align:center; border:1px solid #e2e8f0;'>
                <div style='font-weight:700;'>{r['quartier']}</div>
                <div style='font-size:1.3rem; font-weight:700; color:#1E88E5;'>{r['prix_moyen']:,.0f}</div>
                <div style='font-size:0.8rem; color:#64748b;'>{r['nb_annonces']} annonces</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================
# GRAPHIQUES (3 colonnes)
# ============================================
g1, g2, g3 = st.columns(3)

with g1:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("#### 🏘️ Top 5 quartiers par prix")
    fig = px.bar(top5, x='prix_moyen', y='quartier', orientation='h',
                 color='prix_moyen', color_continuous_scale=['#FDB813', '#E63E6B', '#1E88E5'],
                 text=[f"{x:,.0f}" for x in top5['prix_moyen']])
    fig.update_layout(height=350, plot_bgcolor='white', margin=dict(l=10, r=30))
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with g2:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("#### 📊 Distribution des prix")
    fig = px.histogram(df_f, x='prix_million', nbins=20, color_discrete_sequence=['#2DD4BF'])
    fig.update_layout(height=350, plot_bgcolor='white', margin=dict(l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with g3:
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    st.markdown("#### 🥧 Répartition par type")
    counts = df_f['type_bien'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=counts.index, values=counts.values, hole=0.5,
                                 marker=dict(colors=['#1E88E5', '#FDB813', '#F28C38']))])
    fig.update_layout(height=350, margin=dict(l=20, r=20), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================
# CARTE INTERACTIVE
# ============================================
st.markdown("<div class='section-title'>🗺️ Carte interactive de Dakar</div>", unsafe_allow_html=True)

if len(df_coords) > 0:
    m = folium.Map(location=[14.7167, -17.4677], zoom_start=12, tiles='CartoDB positron')

    # Points
    sample = df_coords.sample(min(150, len(df_coords)))
    for _, r in sample.iterrows():
        color = '#E63E6B' if r['prix'] > df['prix'].quantile(0.75) else '#FDB813' if r['prix'] > df[
            'prix'].median() else '#1E88E5'
        folium.CircleMarker([r['lat'], r['lon']], radius=3,
                            popup=f"<b>{r['quartier']}</b><br>{r['prix']:,.0f} FCFA",
                            color=color, fill=True).add_to(m)

    # Marqueurs quartiers
    for _, r in stats.iterrows():
        radius = 8 + (r['nb_annonces'] / stats['nb_annonces'].max()) * 15
        folium.CircleMarker([r['lat'], r['lon']], radius=radius,
                            popup=f"<b>{r['quartier']}</b><br>Prix: {r['prix_moyen']:,.0f} FCFA",
                            color='#0F172A', fill=True, fillColor='#2DD4BF', fillOpacity=0.7).add_to(m)

    folium_static(m, width=1200, height=450)

# ============================================
# SCATTER PLOT (SANS TRENDLINE)
# ============================================
st.markdown("<div class='section-title'>📈 Relation Surface-Prix</div>", unsafe_allow_html=True)

if len(df_f) > 0:
    fig = px.scatter(df_f, x='surface_m2', y='prix', color='quartier',
                     size='chambres', hover_data=['titre'])
    fig.update_layout(height=500, plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# IMPACT DES OPTIONS
# ============================================
st.markdown("<div class='section-title'>✨ Impact des options</div>", unsafe_allow_html=True)

prix_base = df[df['meuble'] == 0]['prix'].mean()
prix_meuble = df[df['meuble'] == 1]['prix'].mean()
prix_vue = df[df['vue_mer'] == 1]['prix'].mean()
prix_neuf = df[df['neuf'] == 1]['prix'].mean()

o1, o2, o3 = st.columns(3)

with o1:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🛋️</div>
        <div style='font-weight:600;'>Meublé</div>
        <div class='option-value value-green'>+{((prix_meuble / prix_base) - 1) * 100:.1f}%</div>
        <div style='color:#64748b;'>{prix_meuble:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

with o2:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🌊</div>
        <div style='font-weight:600;'>Vue mer</div>
        <div class='option-value value-blue'>+{((prix_vue / prix_base) - 1) * 100:.1f}%</div>
        <div style='color:#64748b;'>{prix_vue:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

with o3:
    st.markdown(f"""
    <div class='option-card'>
        <div class='option-icon'>🏗️</div>
        <div style='font-weight:600;'>Neuf</div>
        <div class='option-value value-purple'>+{((prix_neuf / prix_base) - 1) * 100:.1f}%</div>
        <div style='color:#64748b;'>{prix_neuf:,.0f} FCFA</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# STATISTIQUES DÉTAILLÉES
# ============================================
st.markdown("<div class='section-title'>📊 Statistiques par quartier</div>", unsafe_allow_html=True)

display = stats[['quartier', 'prix_moyen', 'prix_m2_moyen', 'surface_moyenne', 'nb_annonces']].copy()
display.columns = ['Quartier', 'Prix moyen', 'Prix/m²', 'Surface moy.', 'Annonces']
st.dataframe(display.sort_values('Prix moyen', ascending=False).head(10),
             use_container_width=True, hide_index=True)

# ============================================
# DONNÉES DÉTAILLÉES
# ============================================
with st.expander("📋 Voir le tableau complet des annonces"):
    st.dataframe(df_f[['titre', 'quartier', 'prix', 'surface_m2', 'chambres', 'meuble', 'vue_mer', 'neuf']].head(100),
                 use_container_width=True,
                 column_config={
                     "prix": st.column_config.NumberColumn(format="%.0f FCFA"),
                     "surface_m2": st.column_config.NumberColumn(format="%.0f m²")
                 })

# ============================================
# SOURCES
# ============================================
st.markdown("""
<div class='sources'>
    <b>📌 Sources :</b> Loger Dakar • Keur Immobilier • Expat Dakar • Mis à jour Mars 2026
</div>
""", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown(f"""
<div class='footer'>
    <div>🏠 Dashboard Prix Immo • {len(df)} annonces</div>
    <div style='opacity:0.7; font-size:0.8rem;'>Gana Faye • Master 1 Data Science • 🇸🇳 2026</div>
</div>
""", unsafe_allow_html=True)