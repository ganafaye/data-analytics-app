import streamlit as st


def apply_custom_style():
    """Épure l'interface et prépare la sidebar."""
    st.markdown("""
        <style>
            /* Supprime l'espace blanc inutile en haut */
            .block-container {
                padding-top: 1rem !important;
            }

            /* Masque la navigation par défaut pour utiliser tes boutons */
            [data-testid="stSidebarNav"] { display: none; }

            /* Style pour que le popover occupe bien la largeur de la sidebar */
            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button {
                width: 100% !important;
                border-radius: 10px !important;
                border: 1px solid #2563eb !important;
                color: #2563eb !important;
            }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    """Vérifie si l'utilisateur a passé la barrière de l'email."""
    return st.session_state.get("is_logged_in", False)


def login_sidebar():
    """Affiche l'interface de connexion stylisée dans la sidebar."""
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Titre de la section
    st.sidebar.markdown("""
        <div style='text-align: center; padding-bottom: 20px;'>
            <h2 style='color: #1e293b; font-size: 1.5rem;'>🔒 Auth Center</h2>
        </div>
    """, unsafe_allow_html=True)

    if not is_authorized():
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
        # LE BADGE VERT STYLISÉ (Remplace st.sidebar.success)
        st.sidebar.markdown(f"""
            <div style='background-color: #f0fdf4; padding: 15px; border-radius: 12px; border: 1px solid #bbf7d0; margin-bottom: 15px; display: flex; align-items: center; gap: 10px;'>
                <div style='background-color: #22c55e; width: 10px; height: 10px; border-radius: 50%;'></div>
                <div style='flex-grow: 1;'>
                    <p style='margin: 0; font-size: 0.7rem; color: #166534; text-transform: uppercase; font-weight: 700;'>Session Active</p>
                    <p style='margin: 0; font-size: 0.85rem; color: #14532d; font-weight: 600; word-break: break-all;'>{st.session_state['user_email']}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Bouton de déconnexion stylisé
        if st.sidebar.button("Se déconnecter", type="primary", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.rerun()