import streamlit as st
import numpy as np
import cv2
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import io

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(
    page_title="PCA Vision Pro Expert | Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
local_css()
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
        border: 1px solid #60a5fa !important; /* Bordure bleue comme ton titre */
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.4) !important;
    }

    /* 3. Style de l'icône à l'intérieur du bouton */
    button[data-testid="stBaseButton-headerNoPadding"] svg {
        fill: white !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* 4. Ajustement pour que l'icône reste visible même si le header est transparent */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Optionnel : Animation d'apparition douce */
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
# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    .main { background: #f8f9fa; font-family: 'Plus Jakarta Sans', sans-serif; }
    .main-header { background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); margin-bottom: 2rem; border-bottom: 4px solid #667eea; }
    .main-title { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem; font-weight: 800; margin:0;}
    .metric-container { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.2rem; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(102,126,234,0.2); }
    .metric-value { font-size: 1.8rem; font-weight: 800; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 10px 10px 0 0; gap: 1px; padding-top: 10px; }
    .stTabs [aria-selected="true"] { background-color: #667eea; color: white; }
    </style>
""", unsafe_allow_html=True)


# --- FONCTIONS TECHNIQUES ---
@st.cache_data
def executer_pca(img_norm, n_comp):
    pca = PCA(n_components=n_comp)
    img_proj = pca.fit_transform(img_norm)
    img_rec = pca.inverse_transform(img_proj)
    return np.clip(img_rec * 255, 0, 255).astype(np.uint8), pca


def analyser_image(img_bgr, img_gray):
    b, g, r = cv2.split(img_bgr)
    diff = np.mean([np.abs(b.astype(float) - g.astype(float)), np.abs(g.astype(float) - r.astype(float))])
    type_label = "Médicale / N&B" if diff < 10 else "Couleur Standard"
    edges = cv2.Canny(img_gray, 100, 200)
    complexite = (np.sum(edges > 0) / edges.size) * 100
    return type_label, complexite


# --- BARRE LATÉRALE ---
with st.sidebar:
    st.markdown("### 🎛️ Panneau de Contrôle")
    uploaded_file = st.file_uploader("Charger une image", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        type_img, comp_val = analyser_image(img_bgr, img_gray)
        st.success(f"Détecté : {type_img}")

        n_max = min(img_gray.shape)
        n_comp = st.slider("Nombre de composantes ACP", 1, min(n_max, 250), 30)

        st.markdown("### 🎨 Affichage")
        cmap_choice = st.selectbox("Palette de couleurs", ["gray", "bone", "viridis", "magma", "hot"])
        show_residue = st.checkbox("Afficher les résidus (Erreur)", value=False)

# --- EN-TÊTE ---
st.markdown(
    '<div class="main-header"><h1 class="main-title">🔬 PCA Vision Pro Expert</h1><p style="color:#6b7280">Analyse structurelle et décomposition matricielle intelligente</p></div>',
    unsafe_allow_html=True)

if uploaded_file:
    img_norm = img_gray / 255.0
    img_final, pca_obj = executer_pca(img_norm, n_comp)
    var_info = np.sum(pca_obj.explained_variance_ratio_) * 100

    # 1. MÉTRIQUES CLÉS
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(
        f'<div class="metric-container"><div class="metric-value">{var_info:.1f}%</div><div style="font-size:0.7rem">INFO CONSERVÉE</div></div>',
        unsafe_allow_html=True)
    m2.markdown(
        f'<div class="metric-container"><div class="metric-value">{n_comp}</div><div style="font-size:0.7rem">COMPOSANTES</div></div>',
        unsafe_allow_html=True)
    m3.markdown(
        f'<div class="metric-container"><div class="metric-value">{comp_val:.1f}%</div><div style="font-size:0.7rem">COMPLEXITÉ</div></div>',
        unsafe_allow_html=True)
    m4.markdown(
        f'<div class="metric-container"><div class="metric-value">{(1 - n_comp / n_max) * 100:.1f}%</div><div style="font-size:0.7rem">COMPRESSION</div></div>',
        unsafe_allow_html=True)

    st.write("##")

    # 2. ONGLETS D'ANALYSE
    tab1, tab2, tab3, tab4 = st.tabs([
        "📸 Visualisation",
        "📈 Analyse Technique",
        "🧪 Tests Progressifs",
        "🔢 Matrice Numérique"
    ])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🖼️ Originale (N&B)")
            st.image(img_gray, width='stretch', clamp=True)
        with c2:
            if not show_residue:
                st.subheader(f"🔄 Reconstruction (n={n_comp})")
                fig_rec = px.imshow(img_final, color_continuous_scale=cmap_choice if cmap_choice != "bone" else "gray")
                fig_rec.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, b=0, t=0))
                st.plotly_chart(fig_rec, width='stretch')
            else:
                st.subheader("🔍 Résidus (Erreur)")
                residue = cv2.absdiff(img_gray, img_final)
                residue = cv2.equalizeHist(residue)  # Améliore la visibilité de l'erreur
                st.image(residue, width='stretch')

        is_success, buffer = cv2.imencode(".jpg", img_final)
        st.download_button("💾 Télécharger la reconstruction", buffer.tobytes(), "reconstruction.jpg", "image/jpeg")

    with tab2:
        st.subheader("📈 Variance Cumulée et Importance des Composantes")
        pca_full = PCA(n_components=min(150, n_max)).fit(img_norm)
        cum_var = np.cumsum(pca_full.explained_variance_ratio_) * 100

        fig_var = go.Figure()
        fig_var.add_trace(go.Scatter(y=cum_var, mode='lines', line=dict(color='#667eea', width=4), fill='tozeroy',
                                     name="Variance Cumulée"))
        fig_var.add_vline(x=n_comp, line_dash="dash", line_color="orange", annotation_text="Position")
        fig_var.update_layout(xaxis_title="Nombre de composantes", yaxis_title="% Information", height=400)
        st.plotly_chart(fig_var, width='stretch')

    with tab3:
        st.subheader("🧪 Simulation de compression multi-niveaux")
        paliers = [2, 10, 30, 80, 150]
        paliers = [p for p in paliers if p < n_max]
        cols_p = st.columns(len(paliers))
        for i, p in enumerate(paliers):
            with cols_p[i]:
                img_p, _ = executer_pca(img_norm, p)
                st.image(img_p, caption=f"n={p}", width='stretch')

    with tab4:
        st.subheader("🔢 Exploration de la Structure Matricielle")
        st.write("Comparaison des valeurs brutes des pixels (Extrait en haut à gauche).")

        taille_m = st.slider("Taille de l'extrait à afficher", 5, 20, 10)
        col_mat1, col_mat2 = st.columns(2)

        with col_mat1:
            st.markdown("**Matrice Image Originale**")
            st.dataframe(pd.DataFrame(img_gray[:taille_m, :taille_m]))

        with col_mat2:
            st.markdown(f"**Matrice Reconstruction (n={n_comp})**")
            st.dataframe(pd.DataFrame(img_final[:taille_m, :taille_m]))

        st.info(
            "💡 L'ACP réduit le bruit en lissant les valeurs numériques. Observez comment les chiffres de la reconstruction sont proches mais pas identiques à l'original.")

else:
    st.info("👈 Chargez une image pour activer le moteur d'analyse PCA.")
    st.image("https://images.unsplash.com/photo-1530210124550-912dc1381cb8?auto=format&fit=crop&q=80&w=1000",
             caption="Prêt pour l'analyse médicale", width='stretch')
# --- SECTION COURS / RÉSUMÉ (À placer tout en bas du fichier) ---
st.write("##")
st.divider()

with st.expander("📚 COMPRENDRE L'ACP APPLIQUÉE AUX IMAGES (MINI-COURS)"):
    st.markdown("### 🧬 Qu'est-ce que l'ACP fait à votre image ?")

    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.markdown("""
        L'**Analyse en Composantes Principales (ACP)** est une technique de réduction de dimension. 
        Appliquée à une image, elle fonctionne comme un **filtre intelligent** :

        1. **Décomposition** : L'image est vue comme une matrice de pixels. L'ACP cherche les axes (directions) où il y a le plus de variations de lumière.
        2. **Priorisation** : Elle classe ces axes par importance. Les premières composantes capturent les **formes globales** (le thorax, les poumons). Les dernières capturent les **détails fins** et le **bruit**.
        3. **Compression** : En ne gardant que les $n$ premières composantes, on élimine le superflu tout en gardant l'essentiel.
        """)

    with col_c2:
        st.info("""
        **🔍 L'analogie de l'ombre :**
        Imaginez que vous deviez résumer un objet 3D complexe par son ombre portée sur un mur. 
        L'ACP cherche l'angle de lumière qui donne l'ombre la plus détaillée possible de l'objet.
        """)

    st.markdown("---")

    st.markdown("### 📉 Interprétation Mathématique")
    st.latex(r'''
    I \approx \sum_{i=1}^{n} \sigma_i u_i v_i^T
    ''')
    st.caption("Formule de reconstruction : l'image est la somme des n premières composantes les plus importantes.")

    st.markdown("""
    * **Le Taux de Variance :** Si vous atteignez **95%**, cela signifie que mathématiquement, 95% des contrastes de l'image originale sont présents. 
    * **Le Résidu (Bruit) :** En imagerie médicale, l'ACP est souvent utilisée pour le **débruitage**. Ce qui est jeté (les 5% restants) est souvent considéré comme du bruit parasite du capteur.
    """)

    st.warning(
        "⚠️ **Attention :** En dessous de 80% de variance, des artefacts peuvent apparaître, ce qui pourrait masquer une pathologie fine.")

st.markdown(
    "<br><div style='text-align:center; opacity:0.5'>PCA Vision Pro v3.5 | Développé pour l'analyse d'images avancée</div>",
    unsafe_allow_html=True)
