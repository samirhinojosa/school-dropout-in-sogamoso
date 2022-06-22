import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image


########################################################
# Loading images to the website
########################################################
#icon = Image.open("images/favicon.ico")
logo = Image.open("asserts/logo-min.png")


########################################################
# General settings
########################################################
st.set_page_config(
    page_title="Sogamoso School dropout",
    #page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug" : None,
        "Get help" : "https://github.com/samirhinojosa/school-dropout-in-sogamoso",
        "About" : 
        '''
        Made with ❤️ by Team 112 - cohort 6 in Data Science for All - DS4A,
        [Correlation-One](https://www.correlation-one.com/) Training.

        For more information visit the following 
        [link](https://github.com/samirhinojosa/school-dropout-in-sogamoso).
        '''
    }
)


########################################################
# General styles
########################################################
padding = 0
st.markdown(f""" <style>
    .block-container.css-18e3th9.egzxvld2{{
            padding: 20px 60px;
    }}
    .css-v3ay09.edgvbvh1,
    .css-v3ay09.edgvbvh5 {{
        margin-right: 0;
        margin-left: auto;
        display: block;
    }}
    .css-4yfn50.e1fqkh3o1{{
            padding: 4rem 1rem;
    }}
    #data, #repository{{
        padding: 0px;
    }}
    .css-1kyxreq.etr89bj0{{
        justify-content: center;
    }}
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True
)

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

config = {
    "displayModeBar": False,
    "displaylogo": False
}


########################################################
# Page information
########################################################
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Sogamoso school dropout</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:60%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)


########################################################
# Session for the API
########################################################
def fetch(session, url):

    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

session = requests.Session()


########################################################
# Sidebar section
########################################################
sb = st.sidebar # defining the sidebar
#sb.image(sogamoso)

sb.markdown("🛰️ **Navigation**")
page_names = ["🏠 Home", "📊 General statistics", "🎯 2022 projections", "⚙️ Student prediction"]
page = sb.radio("", page_names, index=0)
sb.write('<style>.css-1p2iens { margin-bottom: 0px !important; min-height: 0 !important;}</style>', unsafe_allow_html=True)

msg_sb = sb.info("**How to use it ?** Select the **Home page** to see information related with the project. " \
                "Select **Client prediction** to know whether a specific client will pay the loan based on his information.")

if page == "🏠 Home":

    st.subheader("Home")

elif page == "📊 General statistics":

    st.subheader("📊 General statistics")

elif page == "🎯 2022 projections":

    st.subheader("🎯 2022 projections")

else:
    st.subheader("⚙️ Student prediction")

