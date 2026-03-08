import streamlit as st


def apply_custom_style():
    """Applique le CSS pour masquer la navigation native et styliser l'interface de login."""
    st.markdown("""
        <style>
            /* Masquage de la navigation native */
            [data-testid="stSidebarNav"] { display: none; }

            /* Conteneur de l'icône de profil */
            .login-icon-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 20px;
                padding: 10px;
            }

            .login-avatar {
                background-color: #f1f5f9;
                border-radius: 50%;
                width: 80px;
                height: 80px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 40px;
                border: 2px solid #e2e8f0;
                margin-bottom: 10px;
            }

            /* Titres de sections */
            .sidebar-section-title {
                font-weight: 700; color: #1e293b; margin-top: 1.2rem;
                border-left: 4px solid #2563eb; padding-left: 0.5rem;
                font-size: 0.85rem; text-transform: uppercase;
            }

            /* Style des boutons (Navigation et Connexion) */
            .stButton > button { 
                width: 100%; 
                border-radius: 10px; 
                text-align: left;
                font-weight: 500;
                transition: 0.3s;
            }

            /* Style spécifique pour le bouton de connexion (on peut utiliser une couleur différente) */
            div[data-testid="stSidebar"] .stButton > button {
                border-color: #2563eb;
            }
        </style>
    """, unsafe_allow_html=True)


def login_sidebar():
    """Affiche le formulaire de connexion stylisé dans la sidebar."""
    # Affichage de l'icône de profil en HTML
    st.sidebar.markdown("""
        <div class="login-icon-container">
            <div class="login-avatar">👤</div>
            <div style="font-weight: 600; color: #1e293b;">Connexion</div>
        </div>
    """, unsafe_allow_html=True)

    email = st.sidebar.text_input("Email", placeholder="nom@exemple.com", label_visibility="collapsed",
                                  key="email_auth")

    if st.sidebar.button("Se connecter 🔓", key="login_btn"):
        if email in st.secrets["auth"]["allowed_emails"]:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.sidebar.success("Accès accordé")
            st.rerun()
        else:
            st.sidebar.error("Email non autorisé")