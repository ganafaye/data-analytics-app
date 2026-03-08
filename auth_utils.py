import streamlit as st


def apply_custom_style():
    """Injecte un CSS moderne pour une expérience utilisateur haut de gamme."""
    st.markdown("""
        <style>
            /* 1. Fond de la Sidebar et suppression des menus par défaut */
            [data-testid="stSidebar"] {
                background-color: #f8fafc;
            }
            [data-testid="stSidebarNav"] { display: none; }

            /* 2. Stylisation du bouton Popover (Le bouton de Login) */
            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button {
                background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
                color: white !important;
                border: none !important;
                padding: 0.6rem 1rem !important;
                border-radius: 12px !important;
                font-weight: 600 !important;
                box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1) !important;
                transition: all 0.3s ease !important;
                width: 100% !important;
            }

            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
                opacity: 0.9 !important;
            }

            /* 3. Style pour le formulaire à l'intérieur du popover */
            div[data-testid="stPopoverContent"] {
                border-radius: 15px !important;
                border: 1px solid #e2e8f0 !important;
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1) !important;
            }

            /* 4. Personnalisation des boutons de navigation sur la page Home */
            .stButton > button {
                border-radius: 12px !important;
                border: 1px solid #e2e8f0 !important;
                transition: all 0.2s;
            }
        </style>
    """, unsafe_allow_html=True)


def login_sidebar():
    """Affiche une interface de connexion stylisée dans la sidebar."""
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Titre stylisé
    st.sidebar.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h2 style='color: #1e293b; font-size: 1.5rem;'>🔒 Auth Center</h2>
            <p style='color: #64748b; font-size: 0.8rem;'>Gestion des accès Datalab</p>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("is_logged_in", False):
        with st.sidebar.popover("👤 Se connecter"):
            st.markdown("### Identification")
            email = st.text_input("Email", placeholder="nom@exemple.com", key="email_auth")
            if st.button("Débloquer l'accès", use_container_width=True):
                if email in st.secrets["auth"]["allowed_emails"]:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Email non répertorié")
    else:
        # Affichage du profil utilisateur connecté
        st.sidebar.markdown(f"""
            <div style='background-color: white; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; margin-bottom: 10px;'>
                <p style='margin: 0; font-size: 0.7rem; color: #64748b; text-transform: uppercase;'>Session Active</p>
                <p style='margin: 0; font-weight: 600; color: #0f172a; word-break: break-all;'>{st.session_state['user_email']}</p>
            </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("Déconnexion", type="primary", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.rerun()