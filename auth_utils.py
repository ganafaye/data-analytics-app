import streamlit as st


def apply_custom_style():
    """Applique le CSS pour un design de login moderne et stylisé."""
    st.markdown("""
        <style>
            /* Import des polices */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

            /* Style général */
            .stApp {
                font-family: 'Inter', sans-serif;
            }

            /* Masquage de la navigation native */
            [data-testid="stSidebarNav"] { 
                display: none; 
            }

            /* ===== SIDEBAR STYLÉE ===== */
            section[data-testid="stSidebar"] {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border-right: 1px solid rgba(102, 126, 234, 0.1);
            }

            /* Conteneur de login */
            .login-container {
                background: white;
                border-radius: 20px;
                padding: 2rem 1.5rem;
                margin: 1rem 0 2rem 0;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
                border: 1px solid #e2e8f0;
                position: relative;
                overflow: hidden;
            }

            .login-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #4361ee, #7209b7, #f72585);
            }

            /* En-tête de login */
            .login-header {
                text-align: center;
                margin-bottom: 1.5rem;
            }

            .login-icon {
                width: 80px;
                height: 80px;
                margin: 0 auto 1rem auto;
                background: linear-gradient(135deg, #4361ee, #7209b7);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                color: white;
                box-shadow: 0 10px 20px rgba(67, 97, 238, 0.2);
                animation: float 3s ease-in-out infinite;
            }

            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-5px); }
                100% { transform: translateY(0px); }
            }

            .login-title {
                font-size: 1.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, #4361ee, #7209b7);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.3rem;
            }

            .login-subtitle {
                color: #64748b;
                font-size: 0.85rem;
            }

            /* Champ d'email stylisé */
            .email-input {
                margin: 1.5rem 0;
            }

            .stTextInput > div > div > input {
                border: 2px solid #e2e8f0 !important;
                border-radius: 12px !important;
                padding: 0.8rem 1rem !important;
                font-size: 0.95rem !important;
                transition: all 0.3s ease !important;
            }

            .stTextInput > div > div > input:focus {
                border-color: #4361ee !important;
                box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1) !important;
            }

            .stTextInput > div > div > input::placeholder {
                color: #94a3b8 !important;
                font-size: 0.9rem !important;
            }

            /* Bouton de connexion stylisé */
            .stButton > button {
                background: linear-gradient(135deg, #4361ee, #7209b7) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 0.8rem !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                transition: all 0.3s ease !important;
                box-shadow: 0 8px 20px rgba(67, 97, 238, 0.2) !important;
                position: relative;
                overflow: hidden;
            }

            .stButton > button::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }

            .stButton > button:hover::before {
                width: 300px;
                height: 300px;
            }

            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 30px rgba(67, 97, 238, 0.3) !important;
            }

            /* Messages de statut */
            .stAlert {
                border-radius: 12px !important;
                border: none !important;
                padding: 1rem !important;
                font-size: 0.9rem !important;
            }

            .stSuccess {
                background: linear-gradient(135deg, #e8f5e9, #c8e6c9) !important;
                color: #1b5e20 !important;
                border-left: 4px solid #2e7d32 !important;
            }

            .stError {
                background: linear-gradient(135deg, #ffebee, #ffcdd2) !important;
                color: #b71c1c !important;
                border-left: 4px solid #c62828 !important;
            }

            /* Badge d'email autorisé */
            .allowed-emails {
                background: #f8fafc;
                border-radius: 12px;
                padding: 1rem;
                margin: 1.5rem 0 1rem 0;
                border: 1px solid #e2e8f0;
            }

            .allowed-emails-title {
                font-size: 0.8rem;
                font-weight: 600;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 0.8rem;
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }

            .email-badge {
                display: inline-block;
                background: white;
                padding: 0.3rem 0.8rem;
                border-radius: 30px;
                font-size: 0.75rem;
                color: #4361ee;
                border: 1px solid #4361ee;
                margin: 0.2rem;
                transition: all 0.3s ease;
            }

            .email-badge:hover {
                background: #4361ee;
                color: white;
                transform: translateY(-2px);
            }

            /* Section d'information */
            .login-info {
                margin-top: 1.5rem;
                padding-top: 1rem;
                border-top: 1px dashed #e2e8f0;
                text-align: center;
                font-size: 0.75rem;
                color: #94a3b8;
            }

            .login-info strong {
                color: #4361ee;
                font-weight: 600;
            }

            /* Animation de chargement */
            @keyframes pulse {
                0% { opacity: 0.6; }
                50% { opacity: 1; }
                100% { opacity: 0.6; }
            }

            .loading {
                animation: pulse 1.5s ease-in-out infinite;
            }

            /* Titres de sections dans la sidebar */
            .sidebar-section-title {
                font-weight: 700; 
                color: #1e293b; 
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                border-left: 4px solid #4361ee; 
                padding-left: 0.8rem;
                font-size: 0.85rem; 
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            /* Style des boutons de navigation */
            .stButton > button.nav-button {
                background: white !important;
                color: #334155 !important;
                border: 1px solid #e2e8f0 !important;
                box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
            }

            .stButton > button.nav-button:hover {
                border-color: #4361ee !important;
                color: #4361ee !important;
            }
        </style>
    """, unsafe_allow_html=True)


def login_sidebar():
    """Affiche le formulaire de connexion stylisé dans la sidebar."""

    # Conteneur principal de login
    with st.sidebar:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        # En-tête avec icône animée
        st.markdown("""
            <div class="login-header">
                <div class="login-icon">🔐</div>
                <div class="login-title">Accès sécurisé</div>
                <div class="login-subtitle">Connectez-vous pour accéder aux outils</div>
            </div>
        """, unsafe_allow_html=True)

        # Champ d'email
        st.markdown('<div class="email-input">', unsafe_allow_html=True)
        email = st.text_input(
            "",
            placeholder="votre.email@exemple.com",
            label_visibility="collapsed",
            key="email_auth"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Bouton de connexion
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            login_clicked = st.button("Se connecter", key="login_btn")

        # Traitement de la connexion
        if login_clicked:
            if email:
                # Vérification dans la whitelist
                allowed_emails = st.secrets["auth"]["allowed_emails"]
                if email in allowed_emails:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email
                    st.success("✅ Connexion réussie !")
                    st.rerun()
                else:
                    st.error("❌ Email non autorisé")
            else:
                st.warning("⚠️ Veuillez entrer votre email")

        # Liste des emails autorisés (optionnel, pour information)
        if st.secrets["auth"].get("show_whitelist", True):
            allowed_emails = st.secrets["auth"]["allowed_emails"]
            st.markdown("""
                <div class="allowed-emails">
                    <div class="allowed-emails-title">
                        <span>👥</span> Accès autorisés
                    </div>
            """, unsafe_allow_html=True)

            # Afficher les emails sous forme de badges
            email_html = ""
            for email in allowed_emails[:5]:  # Limiter à 5 pour l'affichage
                email_html += f'<span class="email-badge">{email}</span>'
            st.markdown(email_html, unsafe_allow_html=True)

            if len(allowed_emails) > 5:
                st.caption(f"... et {len(allowed_emails) - 5} autres")

            st.markdown('</div>', unsafe_allow_html=True)

        # Information supplémentaire
        st.markdown("""
            <div class="login-info">
                🔒 Connexion sécurisée<br>
                <strong>Gana's HomeLab</strong> · Accès réservé
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


def user_info_sidebar():
    """Affiche les informations de l'utilisateur connecté."""
    with st.sidebar:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        # Avatar et infos utilisateur
        st.markdown(f"""
            <div class="login-header">
                <div class="login-icon">👤</div>
                <div class="login-title">{st.session_state.user_email.split('@')[0]}</div>
                <div class="login-subtitle">{st.session_state.user_email}</div>
            </div>
        """, unsafe_allow_html=True)

        # Badge de statut
        st.markdown("""
            <div style="text-align: center; margin: 1rem 0;">
                <span style="background: #e8f5e9; color: #2e7d32; padding: 0.3rem 1rem; border-radius: 30px; font-size: 0.8rem; font-weight: 600;">
                    ✅ Connecté
                </span>
            </div>
        """, unsafe_allow_html=True)

        # Bouton de déconnexion
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚪 Déconnexion", key="logout_btn"):
                st.session_state["is_logged_in"] = False
                if "user_email" in st.session_state:
                    del st.session_state["user_email"]
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# --- EXEMPLE D'UTILISATION DANS VOTRE APPLICATION ---
def main():
    # Appliquer le style
    apply_custom_style()

    # Vérifier si l'utilisateur est connecté
    if not st.session_state.get("is_logged_in", False):
        # Afficher le formulaire de connexion
        login_sidebar()

        # Contenu principal (page d'accueil publique)
        st.title("🚀 Gana's AI & Data HomeLab")
        st.markdown("Bienvenue sur ma plateforme d'expérimentation en IA et Data Science.")
        st.info("👈 Connectez-vous avec votre email autorisé pour accéder aux applications.")

    else:
        # Afficher les infos utilisateur dans la sidebar
        user_info_sidebar()

        # Contenu principal (page d'accueil pour utilisateurs connectés)
        st.title(f"👋 Bonjour {st.session_state.user_email.split('@')[0]} !")
        st.markdown("### 🎯 Applications disponibles")

        # Afficher les applications
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏙️ Dakar Immo AI")
            st.markdown("Prédiction des loyers à Dakar")
            if st.button("Lancer"):
                st.switch_page("pages/app_prediction_prix_loyer.py")

        with col2:
            st.markdown("#### 📊 Data Quality Analyzer")
            st.markdown("Analyse de qualité des données")
            if st.button("Lancer"):
                st.switch_page("pages/analyse_data_traitement.py")


if __name__ == "__main__":
    main()