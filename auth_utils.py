import streamlit as st


def apply_custom_style():
    """Fixe le header en haut et permet le défilement du contenu uniquement."""
    st.markdown("""
        <style>
            /* 1. FIXER LE HEADER EN HAUT */
            [data-testid="stHeader"] {
                position: fixed;
                top: 0;
                z-index: 1000;
                background-color: white;
            }

            /* 2. RÉDUIRE L'ESPACE ET GÉRER LE SCROLL DU CORPS */
            .block-container {
                padding-top: 4rem !important; /* Espace pour ne pas être caché par le header fixe */
                padding-bottom: 0rem !important;
            }

            /* Masquer la navigation native sidebar */
            [data-testid="stSidebarNav"] { display: none; }

            /* Style du bouton popover discret */
            div[data-testid="stPopover"] > button {
                border-radius: 20px !important;
                border: 1px solid #e2e8f0 !important;
                height: 35px !important;
            }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    return st.session_state.get("is_logged_in", False)


def login_header():
    """Header compact qui restera visible au scroll."""
    # Conteneur pour le header
    header_container = st.container()

    with header_container:
        col1, col2 = st.columns([0.85, 0.15])

        with col1:
            st.markdown("### 🚀 Gana's Datalab")

        with col2:
            if not is_authorized():
                with st.popover("🔑 Login"):
                    email = st.text_input("Email", placeholder="nom@exemple.com", key="email_auth")
                    if st.button("Valider", use_container_width=True):
                        if email in st.secrets["auth"]["allowed_emails"]:
                            st.session_state["is_logged_in"] = True
                            st.session_state["user_email"] = email
                            st.rerun()
                        else:
                            st.error("Email refusé")
            else:
                with st.popover("👤"):
                    st.write(f"Connecté: {st.session_state['user_email']}")
                    if st.button("Déconnexion", type="primary", use_container_width=True):
                        st.session_state["is_logged_in"] = False
                        st.rerun()
        st.markdown("---")