import streamlit as st

def apply_custom_style():
    """Applique le CSS pour masquer la navigation native et styliser la sidebar."""
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] { display: none; }
            .sidebar-section-title {
                font-weight: 700; color: #1e293b; margin-top: 1.2rem;
                border-left: 4px solid #2563eb; padding-left: 0.5rem;
                font-size: 0.85rem; text-transform: uppercase;
            }
            .stButton > button { width: 100%; border-radius: 10px; text-align: left; }
        </style>
    """, unsafe_allow_html=True)

def is_authorized():
    """Vérifie si l'utilisateur est connecté et présent dans la whitelist."""
    return st.session_state.get("is_logged_in", False)

def login_sidebar():
    """Affiche le formulaire de connexion dans la sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔐 Accès Restreint")
    email = st.sidebar.text_input("Email autorisé", key="email_auth")
    if st.sidebar.button("Vérifier l'accès"):
        # Vérification par rapport aux secrets Streamlit
        if email in st.secrets["auth"]["allowed_emails"]:
            st.session_state["is_logged_in"] = True
            st.session_state["user_email"] = email
            st.sidebar.success("Accès accordé")
            st.rerun()
        else:
            st.sidebar.error("Email non autorisé")