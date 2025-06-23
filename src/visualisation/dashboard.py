import streamlit as st
from src.visualisation.pages import (
    contributing_factor_analysis,
    geographic_analysis,
    time_based_analysis,
)

st.set_page_config(page_title="MVC Dashboard", layout="wide")

st.sidebar.title("NYC Crash Dashboard")

# Use session state to persist exit confirmation
if "exit_confirmed" not in st.session_state:
    st.session_state.exit_confirmed = False

if st.session_state.exit_confirmed:
    st.title("👋 Thank you for using the NYC Crash Dashboard")
    st.markdown("You have exited the dashboard. To start again, refresh the page or restart the app.")
else:
    # Add Exit to menu options
    page = st.sidebar.selectbox(
        "Choose Analysis", ["Time-Based", "Factors", "Geographic", "Exit App"]
    )

    if page == "Time-Based":
        time_based_analysis.show()
    elif page == "Factors":
        contributing_factor_analysis.show()
    elif page == "Geographic":
        geographic_analysis.show()
    elif page == "Exit App":
        st.warning("You are about to exit the dashboard.")
        if st.button("Confirm Exit"):
            st.session_state.exit_confirmed = True
            st.rerun()
