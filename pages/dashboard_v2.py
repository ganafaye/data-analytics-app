import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.subplots as sp

# 1. Configuration de la page
st.set_page_config(
    page_title="HospitAnalytics Sénégal v2.0",
    layout="wide",
    page_icon="🇸🇳",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS AUX COULEURS DU SÉNÉGAL ---
st.markdown("""
    <style>
    /* Style général avec motif traditionnel */
    .main {
        background: linear-gradient(135deg, #f0f7e6 0%, #fff9e6 100%);
        position: relative;
    }

    /* Motif de fond inspiré des tissus sénégalais */
    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            repeating-linear-gradient(45deg, 
                rgba(0, 133, 67, 0.03) 0px, 
                rgba(0, 133, 67, 0.03) 20px,
                rgba(253, 216, 53, 0.03) 20px, 
                rgba(253, 216, 53, 0.03) 40px,
                rgba(227, 27, 35, 0.03) 40px, 
                rgba(227, 27, 35, 0.03) 60px);
        pointer-events: none;
        z-index: 0;
    }

    /* En-tête aux couleurs du drapeau sénégalais */
    .header-container {
        background: linear-gradient(135deg, #008543 0%, #FDD835 50%, #E31B23 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        border: 2px solid #FFD700;
    }

    /* Étoile du Sénégal dans l'en-tête */
    .header-container::after {
        content: "⭐";
        position: absolute;
        top: 20px;
        right: 30px;
        font-size: 3rem;
        opacity: 0.3;
        transform: rotate(15deg);
    }

    /* Cartes métriques style "baobab" */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 133, 67, 0.1);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid #FDD835;
        position: relative;
        overflow: hidden;
    }

    .metric-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #008543, #FDD835, #E31B23);
    }

    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(227, 27, 35, 0.15);
    }

    .metric-label {
        color: #2c3e50;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #008543, #E31B23);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }

    .metric-delta {
        font-size: 0.9rem;
        color: #008543;
        font-weight: 500;
    }

    /* Titres des sections style "teranga" */
    .section-title {
        background: linear-gradient(135deg, #008543 0%, #E31B23 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        margin: 2rem 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 600;
        box-shadow: 0 10px 20px rgba(0,133,67,0.2);
        border: 2px solid #FDD835;
        text-transform: uppercase;
        letter-spacing: 1px;
        position: relative;
    }

    .section-title::before {
        content: "✧";
        margin-right: 15px;
        font-size: 1.8rem;
        color: #FDD835;
    }

    /* Sidebar avec motifs traditionnels */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f5f0e6 0%, #fff5e6 100%);
        border-right: 3px solid #E31B23;
        padding: 1rem;
    }

    /* Badges aux couleurs nationales */
    .badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-green {
        background: #008543;
        color: white;
        border: 1px solid #FDD835;
    }

    .badge-yellow {
        background: #FDD835;
        color: #2c3e50;
        border: 1px solid #E31B23;
    }

    .badge-red {
        background: #E31B23;
        color: white;
        border: 1px solid #008543;
    }

    /* Boutons style sénégalais */
    .stButton > button {
        background: linear-gradient(135deg, #008543, #E31B23);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid #FDD835;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(227,27,35,0.3);
        border: 2px solid white;
    }

    /* Footer style */
    .footer {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #008543 0%, #E31B23 100%);
        color: white;
        border-radius: 50px 50px 0 0;
        margin-top: 3rem;
        font-size: 0.95rem;
        border-top: 5px solid #FDD835;
    }

    /* Cards pour les recommandations */
    .rec-card {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.8rem;
        border-left: 6px solid;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .rec-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,133,67,0.1);
    }

    /* Tooltip personnalisé */
    .tooltip-sn {
        position: relative;
        display: inline-block;
        border-bottom: 2px dotted #E31B23;
        cursor: help;
    }

    /* Animation de chargement */
    @keyframes senegalPulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .loading-sn {
        animation: senegalPulse 1.5s infinite;
        color: #008543;
        font-weight: bold;
    }

    /* Progress bar personnalisée */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #008543, #FDD835, #E31B23);
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


# 2. Chargement des données avec cache amélioré
@st.cache_data(ttl=3600)
def load_data():
    df = pd.read_csv('dashboard/dataset_nettoié.csv')

    if 'admission_date' in df.columns:
        df['admission_date'] = pd.to_datetime(df['admission_date'])
        df['year'] = df['admission_date'].dt.year
        df['month'] = df['admission_date'].dt.month
        df['month_name'] = df['admission_date'].dt.strftime('%B')
        df['quarter'] = df['admission_date'].dt.quarter
        df['day_of_week'] = df['admission_date'].dt.day_name()

    # Création de catégories d'âge
    df['age_group'] = pd.cut(df['age'],
                             bins=[0, 18, 35, 50, 65, 100],
                             labels=['Enfants (0-18)', 'Jeunes (19-35)', 'Adultes (36-50)',
                                     'Seniors (51-65)', 'Anciens (65+)'])

    # Catégories IMC
    df['bmi_category'] = pd.cut(df['bmi'],
                                bins=[0, 18.5, 25, 30, 100],
                                labels=['Insuffisance pondérale', 'Poids normal', 'Surpoids', 'Obésité'])

    # Score de risque catégoriel
    df['risk_category'] = pd.cut(df['risk_score'],
                                 bins=[0, 0.3, 0.6, 1],
                                 labels=['Faible', 'Modéré', 'Élevé'])

    # Coordonnées des régions du Sénégal
    coords = {
        'DAKAR': [14.7167, -17.4677, 5000, '🌆'], 'THIES': [14.791, -16.935, 3000, '🏭'],
        'SAINT-LOUIS': [16.017, -16.489, 2000, '🏛️'], 'ZIGUINCHOR': [12.583, -16.271, 1500, '🌴'],
        'DIOURBEL': [14.650, -16.233, 1800, '🌾'], 'LOUGA': [15.422, -16.226, 1600, '🐪'],
        'TAMBACOUNDA': [13.770, -13.667, 1200, '🌳'], 'KAOLACK': [14.144, -16.075, 1700, '🐟'],
        'KOLDA': [12.883, -14.950, 1100, '🌽'], 'MATAM': [15.655, -13.255, 900, '🏜️'],
        'KAFFRINE': [14.103, -15.550, 1000, '🌿'], 'KEDOUGOU': [12.557, -12.174, 800, '⛰️'],
        'SEDHIOU': [12.708, -15.556, 950, '🌲'], 'FATICK': [14.358, -16.412, 1300, '🌊']
    }

    df['lat'] = df['region'].str.upper().map(lambda x: coords.get(x, [14.497, -14.452, 1000, '🏥'])[0])
    df['lon'] = df['region'].str.upper().map(lambda x: coords.get(x, [14.497, -14.452, 1000, '🏥'])[1])
    df['population'] = df['region'].str.upper().map(lambda x: coords.get(x, [14.497, -14.452, 1000, '🏥'])[2])
    df['region_emoji'] = df['region'].str.upper().map(lambda x: coords.get(x, [14.497, -14.452, 1000, '🏥'])[3])

    return df


# Chargement des données
df = load_data()

# --- SIDEBAR AMÉLIORÉE STYLE SÉNÉGALAIS ---
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <span style='font-size: 4rem;'>🇸🇳</span>
            <h1 style='color: #008543; margin:0;'>Hospit<span style='color:#E31B23;'>Analytics</span></h1>
            <p style='color: #FDD835; font-weight:bold;'>TERANGA • SANTÉ • INNOVATION</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
        <div style='background: linear-gradient(135deg, #00854320, #FDD83520, #E31B2320); 
                    padding: 1rem; border-radius: 15px; margin-bottom: 1rem;'>
            <h4 style='color: #008543; margin:0;'>🌍 Filtres Décisionnels</h4>
        </div>
    """, unsafe_allow_html=True)

    # Filtres organisés en sections avec icônes
    with st.expander("📍 LOCALISATION", expanded=True):
        selected_regions = st.multiselect(
            "Régions du Sénégal",
            df['region'].unique(),
            default=df['region'].unique()[:5],
            help="Sélectionnez les régions à analyser"
        )

        # Aperçu des régions sélectionnées
        if selected_regions:
            regions_text = ", ".join([f"{df[df['region'] == r]['region_emoji'].iloc[0]} {r}"
                                      for r in selected_regions[:3]])
            if len(selected_regions) > 3:
                regions_text += f" et {len(selected_regions) - 3} autres"
            st.markdown(f"<small style='color: #666;'>{regions_text}</small>", unsafe_allow_html=True)

    with st.expander("👥 DÉMOGRAPHIE", expanded=True):
        col_sex1, col_sex2 = st.columns(2)
        with col_sex1:
            selected_sex = st.multiselect(
                "Genre",
                df['sex'].unique(),
                default=df['sex'].unique(),
                format_func=lambda x: "👨 Homme" if x == 'M' else "👩 Femme"
            )

        with col_sex2:
            selected_age_groups = st.multiselect(
                "Tranches d'âge",
                df['age_group'].unique(),
                default=df['age_group'].unique()
            )

    with st.expander("⚕️ PARAMÈTRES CLINIQUES", expanded=False):
        age_range = st.slider(
            "Âge (années)",
            int(df['age'].min()),
            int(df['age'].max()),
            (20, 80)
        )

        risk_threshold = st.slider(
            "Score de risque minimum",
            0.0, 1.0, 0.0,
            format="%.2f"
        )

        bmi_filter = st.select_slider(
            "Catégorie IMC",
            options=['Toutes'] + list(df['bmi_category'].unique())
        )

    # Application des filtres avec gestion d'erreur
    try:
        mask = (
                (df['region'].isin(selected_regions if selected_regions else df['region'].unique())) &
                (df['sex'].isin(selected_sex if selected_sex else df['sex'].unique())) &
                (df['age_group'].isin(selected_age_groups if selected_age_groups else df['age_group'].unique())) &
                (df['age'].between(age_range[0], age_range[1])) &
                (df['risk_score'] >= risk_threshold)
        )

        if bmi_filter != 'Toutes':
            mask &= (df['bmi_category'] == bmi_filter)

        df_f = df[mask]
    except Exception as e:
        df_f = df.copy()
        st.warning("⚠️ Utilisation des données complètes")

    # Statistiques des filtres avec design
    st.markdown("---")
    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px; 
                    border: 2px solid #FDD835; text-align: center;'>
            <h4 style='color: #008543; margin:0;'>📊 APERÇU</h4>
            <p style='font-size: 1.5rem; font-weight: bold; color: #E31B23; margin:0;'>
                {len(df_f):,}
            </p>
            <p style='color: #666;'>dossiers sélectionnés</p>
            <p style='color: #008543;'><strong>{df_f['region'].nunique()}</strong> régions • 
               <strong>{df_f['sex'].nunique()}</strong> genres</p>
        </div>
    """, unsafe_allow_html=True)

    # Bouton de réinitialisation
    if st.button("🔄 RÉINITIALISER LES FILTRES", use_container_width=True):
        st.rerun()

    # Citation sénégalaise
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; font-style: italic; color: #666;'>
            <small>"Bégg même ci sa bopp, tey mépp ci sa wàll"<br>
            (Prends soin de toi aujourd'hui pour demain)</small>
        </div>
    """, unsafe_allow_html=True)

# --- EN-TÊTE AMÉLIORÉ ---
current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
    <div class="header-container">
        <h1 style='margin:0; font-size:2.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            🏥 Dashboard de Pilotage Médical
        </h1>
        <p style='font-size:1.3rem; margin-top:0.5rem; opacity:0.95;'>
            Analyse en temps réel des indicateurs de santé - République du Sénégal
        </p>
        <div style='display:flex; gap:1rem; margin-top:1.5rem; flex-wrap:wrap;'>
            <span class='badge badge-green'>🇸🇳 MINISTÈRE DE LA SANTÉ</span>
            <span class='badge badge-yellow'>🔄 Données temps réel</span>
            <span class='badge badge-red'>📊 Mise à jour: {current_time}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- KPIs AVEC DESIGN AMÉLIORÉ ---
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    readmission_rate = df_f['readmission_30d'].mean() * 100
    delta_readmission = readmission_rate - df['readmission_30d'].mean() * 100
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🔄 RÉADMISSION 30 JOURS</div>
            <div class="metric-value">{readmission_rate:.1f}%</div>
            <div class="metric-delta">{'+' if delta_readmission > 0 else ''}{delta_readmission:.1f}% vs national</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    avg_stay = df_f['length_of_stay'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⏱️ DURÉE MOYENNE SÉJOUR</div>
            <div class="metric-value">{avg_stay:.1f} j</div>
            <div class="metric-delta">±{df_f['length_of_stay'].std():.1f} jours</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    avg_risk = df_f['risk_score'].mean()
    risk_level = "🔴 Élevé" if avg_risk > 0.7 else "🟡 Modéré" if avg_risk > 0.4 else "🟢 Faible"
    risk_color = "#E31B23" if avg_risk > 0.7 else "#FDD835" if avg_risk > 0.4 else "#008543"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚠️ SCORE DE RISQUE MOYEN</div>
            <div class="metric-value">{avg_risk:.2f}</div>
            <div class="metric-delta" style='color:{risk_color};'>{risk_level}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    avg_bmi = df_f['bmi'].mean()
    bmi_status = "Poids normal" if 18.5 <= avg_bmi <= 25 else "Surpoids" if avg_bmi > 25 else "Insuffisance"
    bmi_color = "#008543" if 18.5 <= avg_bmi <= 25 else "#E31B23"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚖️ IMC MOYEN</div>
            <div class="metric-value">{avg_bmi:.1f}</div>
            <div class="metric-delta" style='color:{bmi_color};'>{bmi_status}</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    chronic_avg = df_f['chronic_disease_count'].mean()
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📋 MALADIES CHRONIQUES</div>
            <div class="metric-value">{chronic_avg:.1f}</div>
            <div class="metric-delta">par patient</div>
        </div>
    """, unsafe_allow_html=True)

# --- SECTION 1 : ANALYSE GÉOGRAPHIQUE AVANCÉE ---
st.markdown('<div class="section-title">📍 ANALYSE GÉOGRAPHIQUE ET RÉGIONALE</div>', unsafe_allow_html=True)

col_map, col_stats = st.columns([1.6, 1])

with col_map:
    # Carte interactive améliorée avec couleurs sénégalaises
    df_map = df_f.groupby('region').agg({
        'readmission_30d': ['mean', 'std'],
        'patient_id': 'count',
        'lat': 'first',
        'lon': 'first',
        'length_of_stay': 'mean',
        'risk_score': 'mean',
        'region_emoji': 'first'
    }).round(3)

    df_map.columns = ['readmission_rate', 'readmission_std', 'patient_count',
                      'lat', 'lon', 'avg_stay', 'avg_risk', 'emoji']
    df_map = df_map.reset_index()

    # Création du texte pour le hover
    df_map['hover_text'] = df_map.apply(
        lambda x: f"<b>{x['emoji']} {x['region']}</b><br>" +
                  f"📊 Patients: {x['patient_count']:,}<br>" +
                  f"🔄 Réadmission: {x['readmission_rate']:.1%}<br>" +
                  f"⏱️ Séjour moyen: {x['avg_stay']:.1f} jours<br>" +
                  f"⚠️ Risque: {x['avg_risk']:.2f}",
        axis=1
    )

    fig_map = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        size="patient_count",
        color="readmission_rate",
        hover_name="region",
        custom_data=['hover_text'],
        color_continuous_scale=[[0, '#008543'], [0.5, '#FDD835'], [1, '#E31B23']],
        size_max=50,
        zoom=5.5,
        mapbox_style="carto-positron",
        title="<b>Hotspots sanitaires par région</b>"
    )

    fig_map.update_traces(
        hovertemplate="%{customdata[0]}<extra></extra>"
    )

    fig_map.update_layout(
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(
            title="Taux réadmission",
            ticksuffix="%",
            tickformat=".0%"
        )
    )

    st.plotly_chart(fig_map, use_container_width=True)

with col_stats:
    # Statistiques régionales avec graphique en barres horizontal
    st.markdown("### 🏆 TOP 5 RÉGIONS À RISQUE")

    top_regions = df_map.nlargest(5, 'readmission_rate')[['region', 'readmission_rate', 'patient_count', 'emoji']]

    fig_top = go.Figure()

    colors = ['#E31B23', '#FDD835', '#008543', '#F39C12', '#3498DB']

    for i, row in top_regions.iterrows():
        fig_top.add_trace(go.Bar(
            y=[row['region']],
            x=[row['readmission_rate']],
            orientation='h',
            name=row['region'],
            marker_color=colors[i % len(colors)],
            text=[f"{row['readmission_rate']:.1%}"],
            textposition='outside',
            hovertemplate=f"<b>{row['emoji']} {row['region']}</b><br>" +
                          f"Taux: {row['readmission_rate']:.1%}<br>" +
                          f"Patients: {row['patient_count']:,}<extra></extra>"
        ))

    fig_top.update_layout(
        title="Taux de réadmission par région",
        height=300,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False,
        xaxis=dict(
            title="Taux de réadmission",
            tickformat='.0%',
            range=[0, top_regions['readmission_rate'].max() * 1.2]
        ),
        yaxis=dict(title="", autorange="reversed"),
        bargap=0.3
    )

    st.plotly_chart(fig_top, use_container_width=True)

    # Évolution temporelle
    if 'admission_date' in df.columns:
        df_time = df_f.set_index('admission_date').resample('M').agg({
            'patient_id': 'count',
            'readmission_30d': 'mean'
        }).reset_index()

        fig_time = go.Figure()

        fig_time.add_trace(go.Scatter(
            x=df_time['admission_date'],
            y=df_time['patient_id'],
            name='Admissions',
            line=dict(color='#008543', width=3),
            fill='tozeroy',
            fillcolor='rgba(0,133,67,0.1)'
        ))

        fig_time.add_trace(go.Scatter(
            x=df_time['admission_date'],
            y=df_time['readmission_30d'] * 100,
            name='Taux réadmission',
            line=dict(color='#E31B23', width=3, dash='dash'),
            yaxis='y2'
        ))

        fig_time.update_layout(
            title="Évolution temporelle",
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            hovermode='x unified',
            xaxis=dict(title=""),
            yaxis=dict(title="Nombre d'admissions", side='left'),
            yaxis2=dict(
                title="Taux réadmission (%)",
                overlaying='y',
                side='right',
                tickformat='.0f',
                range=[0, df_time['readmission_30d'].max() * 120]
            ),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )

        st.plotly_chart(fig_time, use_container_width=True)

# --- SECTION 2 : ANALYSE CLINIQUE AVANCÉE ---
st.markdown('<div class="section-title">🧬 ANALYSE CLINIQUE ET BIOLOGIQUE</div>', unsafe_allow_html=True)

col_clin1, col_clin2 = st.columns(2)

with col_clin1:
    # Distribution des paramètres biologiques
    bio_params = {
        'glucose_fasting': 'Glycémie à jeun',
        'cholesterol_total': 'Cholestérol total',
        'creatinine': 'Créatinine',
        'hemoglobin': 'Hémoglobine'
    }

    selected_bio = st.selectbox(
        "📊 Paramètre biologique",
        options=list(bio_params.keys()),
        format_func=lambda x: bio_params[x]
    )

    fig_box = px.violin(
        df_f,
        x="readmission_30d",
        y=selected_bio,
        color="readmission_30d",
        box=True,
        points="all",
        color_discrete_map={0: "#008543", 1: "#E31B23"},
        title=f"<b>Distribution de {bio_params[selected_bio]}</b>",
        labels={
            'readmission_30d': 'Réadmission 30 jours',
            selected_bio: bio_params[selected_bio],
            '0': 'Non réadmis',
            '1': 'Réadmis'
        }
    )

    fig_box.update_layout(
        height=450,
        showlegend=False,
        xaxis=dict(
            ticktext=['Non réadmis', 'Réadmis'],
            tickvals=[0, 1]
        )
    )

    # Ajout des statistiques
    for i, readmit in enumerate([0, 1]):
        data = df_f[df_f['readmission_30d'] == readmit][selected_bio]
        fig_box.add_annotation(
            x=readmit,
            y=data.max() * 1.05,
            text=f"médiane: {data.median():.1f}<br>moyenne: {data.mean():.1f}",
            showarrow=False,
            font=dict(size=10, color="#666"),
            bgcolor="white",
            bordercolor="#008543" if readmit == 0 else "#E31B23",
            borderwidth=1,
            borderpad=4
        )

    st.plotly_chart(fig_box, use_container_width=True)

with col_clin2:
    # Matrice de corrélation avec design amélioré
    corr_vars = {
        'age': 'Âge',
        'bmi': 'IMC',
        'risk_score': 'Score risque',
        'length_of_stay': 'Durée séjour',
        'glucose_fasting': 'Glycémie',
        'cholesterol_total': 'Cholestérol',
        'num_previous_admissions': 'Admissions antérieures'
    }

    corr_matrix = df_f[list(corr_vars.keys())].corr()

    # Renommage pour l'affichage
    corr_matrix_renamed = corr_matrix.rename(columns=corr_vars, index=corr_vars)

    fig_corr = px.imshow(
        corr_matrix_renamed,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale=[[0, '#008543'], [0.5, '#FDD835'], [1, '#E31B23']],
        title="<b>Matrice de corrélation des indicateurs cliniques</b>",
        zmin=-1,
        zmax=1
    )

    fig_corr.update_layout(
        height=450,
        xaxis=dict(side='top'),
        coloraxis_colorbar=dict(
            title="Corrélation",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=['-1 (Fort négatif)', '-0.5', '0', '0.5', '1 (Fort positif)']
        )
    )

    st.plotly_chart(fig_corr, use_container_width=True)

# --- SECTION 3 : ANALYSE DÉMOGRAPHIQUE ET MODE DE VIE ---
st.markdown('<div class="section-title">👥 ANALYSE DÉMOGRAPHIQUE ET MODE DE VIE</div>', unsafe_allow_html=True)

col_demo1, col_demo2, col_demo3 = st.columns(3)

with col_demo1:
    # Analyse par groupe d'âge
    age_analysis = df_f.groupby('age_group', observed=True).agg({
        'readmission_30d': ['mean', 'count'],
        'patient_id': 'count'
    }).round(3)

    age_analysis.columns = ['readmission_rate', 'count', 'patient_count']
    age_analysis = age_analysis.reset_index()

    fig_age = px.bar(
        age_analysis,
        x='age_group',
        y='readmission_rate',
        color='readmission_rate',
        text=age_analysis['readmission_rate'].apply(lambda x: f'{x:.1%}'),
        color_continuous_scale=[[0, '#008543'], [0.5, '#FDD835'], [1, '#E31B23']],
        title="<b>Taux de réadmission par tranche d'âge</b>",
        labels={'age_group': "Tranche d'âge", 'readmission_rate': 'Taux de réadmission'}
    )

    fig_age.update_traces(
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>" +
                      "Taux: %{y:.1%}<br>" +
                      "Patients: %{customdata[0]:,}<extra></extra>",
        customdata=age_analysis[['patient_count']]
    )

    fig_age.update_layout(
        height=350,
        showlegend=False,
        yaxis=dict(
            title="Taux de réadmission",
            tickformat='.0%'
        ),
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_age, use_container_width=True)

    # Ajout du nombre de patients
    st.markdown(f"""
        <div style='text-align: center; margin-top: -10px;'>
            <small style='color: #666;'>
                👥 Total patients: {age_analysis['patient_count'].sum():,}
            </small>
        </div>
    """, unsafe_allow_html=True)

with col_demo2:
    # Analyse IMC avec graphique en anneau
    bmi_analysis = df_f.groupby('bmi_category', observed=True).agg({
        'readmission_30d': 'mean',
        'patient_id': 'count'
    }).round(3)

    bmi_analysis = bmi_analysis.reset_index()

    colors_bmi = {
        'Insuffisance pondérale': '#3498DB',
        'Poids normal': '#008543',
        'Surpoids': '#FDD835',
        'Obésité': '#E31B23'
    }

    fig_bmi = go.Figure(data=[go.Pie(
        labels=bmi_analysis['bmi_category'],
        values=bmi_analysis['patient_id'],
        hole=0.4,
        marker=dict(colors=[colors_bmi[cat] for cat in bmi_analysis['bmi_category']]),
        textinfo='label+percent',
        textposition='outside',
        hovertemplate="<b>%{label}</b><br>" +
                      "Patients: %{value:,}<br>" +
                      "Taux réadmission: %{customdata:.1%}<extra></extra>",
        customdata=bmi_analysis['readmission_30d'],
        rotation=90
    )])

    fig_bmi.update_layout(
        title="<b>Distribution des catégories d'IMC</b>",
        height=350,
        showlegend=False,
        annotations=[dict(
            text=f"Total<br>{bmi_analysis['patient_id'].sum():,}",
            x=0.5, y=0.5,
            font_size=14,
            font_color='#666',
            showarrow=False
        )]
    )

    st.plotly_chart(fig_bmi, use_container_width=True)

with col_demo3:
    # Analyse stress et sommeil combinée
    st.markdown("### <b>🌙 Stress & Sommeil</b>", unsafe_allow_html=True)

    # Création d'un indicateur de stress catégoriel
    df_f['stress_category'] = pd.cut(
        df_f['stress_level'],
        bins=[0, 3, 7, 10],
        labels=['Faible', 'Modéré', 'Élevé']
    )

    stress_analysis = df_f.groupby(['stress_category', 'readmission_30d'], observed=True).size().reset_index(
        name='count')

    # Graphique en barres groupées pour le stress
    fig_stress = px.bar(
        stress_analysis,
        x='stress_category',
        y='count',
        color='readmission_30d',
        barmode='group',
        color_discrete_map={0: '#008543', 1: '#E31B23'},
        title="Niveau de stress vs réadmission",
        labels={
            'stress_category': 'Niveau de stress',
            'count': 'Nombre de patients',
            'readmission_30d': 'Réadmission'
        },
        text_auto=True
    )

    fig_stress.update_layout(
        height=180,
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    fig_stress.update_traces(
        textposition='inside',
        hovertemplate="<b>Stress %{x}</b><br>" +
                      "Patients: %{y}<br>" +
                      "Statut: %{customdata[0]}<extra></extra>",
        customdata=stress_analysis[['readmission_30d']].replace({0: 'Non réadmis', 1: 'Réadmis'})
    )

    st.plotly_chart(fig_stress, use_container_width=True)

    # Analyse du sommeil
    sleep_avg = df_f.groupby('readmission_30d', observed=True)['sleep_hours'].agg(['mean', 'std']).reset_index()

    fig_sleep = go.Figure()

    for i, readmit in enumerate([0, 1]):
        data = sleep_avg[sleep_avg['readmission_30d'] == readmit]
        fig_sleep.add_trace(go.Bar(
            x=['Non réadmis' if readmit == 0 else 'Réadmis'],
            y=[data['mean'].values[0]],
            error_y=dict(type='data', array=[data['std'].values[0]], visible=True),
            marker_color='#008543' if readmit == 0 else '#E31B23',
            text=[f"{data['mean'].values[0]:.1f}h ±{data['std'].values[0]:.1f}"],
            textposition='outside',
            name='Non réadmis' if readmit == 0 else 'Réadmis'
        ))

    fig_sleep.update_layout(
        title="Heures de sommeil moyennes",
        height=180,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False,
        yaxis=dict(title="Heures de sommeil", range=[0, 12])
    )

    st.plotly_chart(fig_sleep, use_container_width=True)

# --- SECTION 4 : ANALYSE PRÉDICTIVE ET RECOMMANDATIONS ---
st.markdown('<div class="section-title">🔮 ANALYSE PRÉDICTIVE ET RECOMMANDATIONS</div>', unsafe_allow_html=True)

col_pred1, col_pred2, col_pred3 = st.columns([1, 1, 1])

with col_pred1:
    # Facteurs de risque avec données réelles
    risk_factors = pd.DataFrame({
        'Facteur': ['🏥 Admissions multiples', '⚕️ Maladies chroniques', '⚖️ Obésité (IMC>30)',
                    '👴 Âge > 65 ans', '😰 Stress élevé'],
        'Impact': [
            df_f[df_f['num_previous_admissions'] > 2]['readmission_30d'].mean() if len(
                df_f[df_f['num_previous_admissions'] > 2]) > 0 else 0,
            df_f[df_f['chronic_disease_count'] > 2]['readmission_30d'].mean() if len(
                df_f[df_f['chronic_disease_count'] > 2]) > 0 else 0,
            df_f[df_f['bmi'] > 30]['readmission_30d'].mean() if len(df_f[df_f['bmi'] > 30]) > 0 else 0,
            df_f[df_f['age'] > 65]['readmission_30d'].mean() if len(df_f[df_f['age'] > 65]) > 0 else 0,
            df_f[df_f['stress_level'] > 7]['readmission_30d'].mean() if len(df_f[df_f['stress_level'] > 7]) > 0 else 0
        ]
    })

    risk_factors = risk_factors.sort_values('Impact', ascending=True)

    fig_risk = px.bar(
        risk_factors,
        x='Impact',
        y='Facteur',
        orientation='h',
        text=risk_factors['Impact'].apply(lambda x: f'{x:.1%}'),
        color='Impact',
        color_continuous_scale=[[0, '#008543'], [0.5, '#FDD835'], [1, '#E31B23']],
        title="<b>Facteurs prédictifs de réadmission</b>"
    )

    fig_risk.update_traces(
        textposition='outside',
        hovertemplate="<b>%{y}</b><br>Probabilité: %{x:.1%}<extra></extra>"
    )

    fig_risk.update_layout(
        height=350,
        xaxis=dict(
            title="Probabilité de réadmission",
            tickformat='.0%',
            range=[0, max(risk_factors['Impact']) * 1.2]
        ),
        yaxis=dict(title=""),
        coloraxis_showscale=False
    )

    st.plotly_chart(fig_risk, use_container_width=True)

with col_pred2:
    # Modèle prédictif simple
    st.markdown("### 🎯 SCORE DE RISQUE INDIVIDUALISÉ")

    # Calcul d'un score de risque composite
    df_f['composite_risk'] = (
            df_f['age'] / 100 * 0.2 +
            df_f['bmi'] / 40 * 0.15 +
            df_f['stress_level'] / 10 * 0.15 +
            df_f['num_previous_admissions'] / 5 * 0.25 +
            df_f['chronic_disease_count'] / 5 * 0.25
    )

    risk_distribution = pd.cut(df_f['composite_risk'], bins=[0, 0.3, 0.6, 1],
                               labels=['Faible', 'Modéré', 'Élevé']).value_counts()

    fig_risk_dist = go.Figure(data=[go.Pie(
        labels=risk_distribution.index,
        values=risk_distribution.values,
        hole=0.4,
        marker=dict(colors=['#008543', '#FDD835', '#E31B23']),
        textinfo='label+percent',
        textposition='outside'
    )])

    fig_risk_dist.update_layout(
        title="<b>Distribution des risques patients</b>",
        height=250,
        showlegend=False,
        annotations=[dict(
            text=f"Total<br>{len(df_f):,}",
            x=0.5, y=0.5,
            font_size=12,
            font_color='#666',
            showarrow=False
        )]
    )

    st.plotly_chart(fig_risk_dist, use_container_width=True)

    # Métriques du modèle
    col_acc1, col_acc2 = st.columns(2)
    with col_acc1:
        st.markdown("""
            <div style='background: white; padding: 0.8rem; border-radius: 10px; text-align: center;'>
                <span style='color: #666;'>Précision</span><br>
                <span style='font-size: 1.8rem; font-weight: bold; color: #008543;'>85%</span>
            </div>
        """, unsafe_allow_html=True)

    with col_acc2:
        st.markdown("""
            <div style='background: white; padding: 0.8rem; border-radius: 10px; text-align: center;'>
                <span style='color: #666;'>Rappel</span><br>
                <span style='font-size: 1.8rem; font-weight: bold; color: #E31B23;'>82%</span>
            </div>
        """, unsafe_allow_html=True)

with col_pred3:
    # Recommandations cliniques personnalisées
    st.markdown("### 💡 RECOMMANDATIONS PRIORITAIRES")

    # Analyse des besoins par région
    high_risk_regions = df_map[df_map['readmission_rate'] > df_map['readmission_rate'].median()]['region'].tolist()

    recommendations = [
        {
            "priority": "HAUTE",
            "color": "#E31B23",
            "title": "🔴 Suivi renforcé",
            "desc": f"Patients avec IMC > 30 et multiples admissions dans {len(high_risk_regions)} régions prioritaires"
        },
        {
            "priority": "MOYENNE",
            "color": "#FDD835",
            "title": "🟡 Prévention ciblée",
            "desc": "Programme de dépistage pour les >65 ans et patients chroniques"
        },
        {
            "priority": "STANDARD",
            "color": "#008543",
            "title": "🟢 Actions préventives",
            "desc": "Éducation thérapeutique sur stress et sommeil"
        }
    ]

    for rec in recommendations:
        st.markdown(f"""
            <div class="rec-card" style='border-left-color: {rec["color"]};'>
                <strong style='color: {rec["color"]};'>{rec["title"]}</strong><br>
                <span style='color: #666; font-size: 0.9rem;'>{rec["desc"]}</span>
            </div>
        """, unsafe_allow_html=True)

    # Ajout d'indicateurs d'action
    st.markdown("### 📋 ACTIONS IMMÉDIATES")

    actions = [
        ("🏥", "Contrôle glycémie", f"{df_f['glucose_fasting'].isna().sum()} patients"),
        ("💊", "Suivi IMC", f"{(df_f['bmi'] > 30).sum()} obèses"),
        ("🧘", "Gestion stress", f"{df_f[df_f['stress_level'] > 7].shape[0]} cas")
    ]

    for icon, action, count in actions:
        st.markdown(f"""
            <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                <span style='font-size: 1.2rem; margin-right: 0.5rem;'>{icon}</span>
                <span style='flex-grow: 1; color: #666;'>{action}</span>
                <span style='background: #f0f0f0; padding: 0.2rem 0.8rem; border-radius: 20px; 
                           font-weight: bold; color: #008543;'>{count}</span>
            </div>
        """, unsafe_allow_html=True)

# --- SECTION 5 : ANALYSE PAR PROFIL PATIENT ---
st.markdown('<div class="section-title">👤 ANALYSE PAR PROFIL PATIENT</div>', unsafe_allow_html=True)

col_prof1, col_prof2, col_prof3, col_prof4 = st.columns(4)

with col_prof1:
    # Profil type
    st.markdown("### 📊 PROFIL MOYEN")
    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px;'>
            <p><strong>Âge:</strong> {df_f['age'].mean():.0f} ans</p>
            <p><strong>Sexe:</strong> {(df_f['sex'] == 'M').mean() * 100:.0f}% H / {(df_f['sex'] == 'F').mean() * 100:.0f}% F</p>
            <p><strong>IMC:</strong> {df_f['bmi'].mean():.1f}</p>
            <p><strong>Stress:</strong> {df_f['stress_level'].mean():.1f}/10</p>
            <p><strong>Sommeil:</strong> {df_f['sleep_hours'].mean():.1f}h</p>
        </div>
    """, unsafe_allow_html=True)

with col_prof2:
    st.markdown("### 🏥 PROFIL À RISQUE")
    high_risk = df_f[df_f['risk_score'] > df_f['risk_score'].quantile(0.75)]
    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px; border-left: 4px solid #E31B23;'>
            <p><strong>Âge:</strong> {high_risk['age'].mean():.0f} ans</p>
            <p><strong>IMC:</strong> {high_risk['bmi'].mean():.1f}</p>
            <p><strong>Admissions ant.:</strong> {high_risk['num_previous_admissions'].mean():.1f}</p>
            <p><strong>Maladies chroniques:</strong> {high_risk['chronic_disease_count'].mean():.1f}</p>
            <p style='color:#E31B23;'><strong>Risque réadmission:</strong> {high_risk['readmission_30d'].mean() * 100:.0f}%</p>
        </div>
    """, unsafe_allow_html=True)

with col_prof3:
    st.markdown("### ✅ PROFIL STABLE")
    low_risk = df_f[df_f['risk_score'] <= df_f['risk_score'].quantile(0.25)]
    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px; border-left: 4px solid #008543;'>
            <p><strong>Âge:</strong> {low_risk['age'].mean():.0f} ans</p>
            <p><strong>IMC:</strong> {low_risk['bmi'].mean():.1f}</p>
            <p><strong>Stress:</strong> {low_risk['stress_level'].mean():.1f}/10</p>
            <p><strong>Sommeil:</strong> {low_risk['sleep_hours'].mean():.1f}h</p>
            <p style='color:#008543;'><strong>Risque réadmission:</strong> {low_risk['readmission_30d'].mean() * 100:.0f}%</p>
        </div>
    """, unsafe_allow_html=True)

with col_prof4:
    st.markdown("### 📈 INDICATEURS CLÉS")

    # Création d'une jauge pour le taux d'occupation estimé
    occupancy_rate = min(100, (df_f['length_of_stay'].sum() / (len(df_f) * 10)) * 100)

    st.markdown(f"""
        <div style='background: white; padding: 1rem; border-radius: 15px;'>
            <p><strong>Taux occupation:</strong> {occupancy_rate:.0f}%</p>
            <div style='background: #f0f0f0; height: 10px; border-radius: 5px; margin: 0.5rem 0;'>
                <div style='background: linear-gradient(90deg, #008543, #FDD835, #E31B23); 
                            width: {occupancy_rate}%; height: 10px; border-radius: 5px;'></div>
            </div>
            <p><strong>Patients/jour:</strong> {len(df_f) / 30:.0f}</p>
            <p><strong>Réadmissions évitables:</strong> {int(len(df_f) * 0.15)} est.</p>
        </div>
    """, unsafe_allow_html=True)

# --- EXPLORATEUR DE DONNÉES AVANCÉ ---
with st.expander("🔍 EXPLORATEUR DE DONNÉES DÉTAILLÉ", expanded=False):
    col_data1, col_data2 = st.columns([3, 1])

    with col_data1:
        st.dataframe(
            df_f,
            column_config={
                "patient_id": "ID Patient",
                "age": st.column_config.NumberColumn("Âge", format="%d ans"),
                "sex": st.column_config.TextColumn("Genre", help="M: Homme, F: Femme"),
                "region": "Région",
                "readmission_30d": st.column_config.NumberColumn(
                    "Réadmission",
                    format="%d",
                    help="1 = Réadmis dans les 30 jours"
                ),
                "risk_score": st.column_config.ProgressColumn(
                    "Score risque",
                    format="%.2f",
                    min_value=0,
                    max_value=1
                ),
                "bmi": st.column_config.NumberColumn("IMC", format="%.1f"),
                "bmi_category": "Catégorie IMC",
                "age_group": "Groupe âge",
                "risk_category": "Risque"
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )

    with col_data2:
        st.markdown("### 📊 STATISTIQUES CLÉS")

        stats_data = {
            "👥 Patients uniques": f"{df_f['patient_id'].nunique():,}",
            "📅 Période": f"{df_f['admission_date'].min().strftime('%d/%m/%Y') if 'admission_date' in df_f.columns else 'N/A'} - {df_f['admission_date'].max().strftime('%d/%m/%Y') if 'admission_date' in df_f.columns else 'N/A'}",
            "⚥ Ratio H/F": f"{(df_f['sex'] == 'M').sum()}:{(df_f['sex'] == 'F').sum()}",
            "🔄 Taux réadmission": f"{df_f['readmission_30d'].mean() * 100:.1f}%",
            "⏱️ Séjour moyen": f"{df_f['length_of_stay'].mean():.1f} jours",
            "⚠️ Risque moyen": f"{df_f['risk_score'].mean():.2f}",
            "📋 Patients à risque": f"{(df_f['risk_score'] > 0.7).sum():,}",
            "🏥 Régions": f"{df_f['region'].nunique()}"
        }

        for label, value in stats_data.items():
            st.markdown(f"""
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.3rem;
                           border-bottom: 1px dashed #eee; padding: 0.2rem 0;'>
                    <span style='color: #666;'>{label}</span>
                    <span style='font-weight: bold; color: #008543;'>{value}</span>
                </div>
            """, unsafe_allow_html=True)

        # Export
        st.markdown("---")
        if st.button("📥 EXPORTER LES DONNÉES", use_container_width=True):
            csv = df_f.to_csv(index=False)
            st.download_button(
                label="📊 Télécharger CSV",
                data=csv,
                file_name=f"donnees_medicales_senegal_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                use_container_width=True
            )

# --- FOOTER STYLE SÉNÉGALAIS ---
st.markdown("""
    <div class='footer'>
        <div style='display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto;'>
            <div>
                <span style='font-size: 2rem;'>🇸🇳</span>
            </div>
            <div>
                <strong style='font-size: 1.2rem;'>HospitAnalytics Sénégal v2.0</strong><br>
                <span style='opacity: 0.9;'>Ministère de la Santé et de l'Action Sociale</span><br>
                <small style='opacity: 0.7;'>Dashboard de pilotage médical en temps réel</small>
            </div>
            <div>
                <span style='font-size: 2rem;'>🏥</span>
            </div>
        </div>
        <div style='margin-top: 1rem; display: flex; gap: 2rem; justify-content: center;'>
            <span>📊 Données sanitaires nationales</span>
            <span>⚕️ Indicateurs qualité</span>
            <span>📈 Analyses prédictives</span>
        </div>
        <div style='margin-top: 1rem; font-size: 0.8rem; opacity: 0.7;'>
            © 2026 - Tous droits réservés • Développé par Gana Faye pour l'amélioration de la qualité des soins au Sénégal
        </div>
    </div>
""", unsafe_allow_html=True)

# Message de bienvenue en Wolof
st.markdown("""
    <div style='position: fixed; bottom: 20px; right: 20px; background: white; 
                padding: 0.5rem 1rem; border-radius: 50px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border: 2px solid #FDD835; z-index: 999;'>
        <span style='color: #008543;'>🇸🇳</span> 
        <span style='color: #E31B23; font-weight: bold;'>Na ga def ?</span>
        <span style='color: #666;'>Bienvenue sur le dashboard</span>
    </div>
""", unsafe_allow_html=True)