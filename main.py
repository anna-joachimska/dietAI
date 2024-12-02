import streamlit as st

st.set_page_config(
    page_title="DietAI",
    page_icon="🥦",
    layout="wide"
)
# add logo
# st.sidebar.image("images/logo.png")
st.html("""
  <style>
    [alt=Logo] {
      height: 80px;
    }
  </style>
        """)
st.logo("images/logo.png", size="large")

with st.sidebar:

    pages = [
        st.Page("pages/01_chat.py", title="🤖 Chat "),
        st.Page("pages/02_meal_planer.py", title="🍴 Meal Planner"),
        st.Page("pages/03_diet_vision.py", title="📷 Diet Vision")
    ]

pg = st.navigation(pages)
pg.run()
