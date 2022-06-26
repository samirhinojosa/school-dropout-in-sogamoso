import streamlit as st
from PIL import Image

########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/sogamoso.ico")

########################################################
# General settings
########################################################
st.set_page_config(
    page_title="Student Prediction - Sogamoso School dropout",
    page_icon=icon,
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
# Sidebar XXXXXXXXXXXXXXXXXXXXXXXXXXx
########################################################
client_selection_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🔎 Student selection</h3>'
st.sidebar.markdown(client_selection_title, unsafe_allow_html=True)

with st.sidebar.form('Form1'):
    see_local_interpretation = st.checkbox("See local interpretation")
    see_stats = st.checkbox("See stats")
    st.warning("**Option(s)** will take more time.")
    result = st.form_submit_button("Predict")

st.sidebar.info("Select a student to **get** information related to **probability** that he/she " \
                "**dropouts out** of school.\nIn addition, you can analyze some stats for this student.")

########################################################
# Page information
########################################################
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Student Prediction - Sogamoso School dropout</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:90%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)


########################################################
# XXXXXXXXXXXXXXXXXXXXXXXXXXx
########################################################
if see_local_interpretation:
    
    client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📋 Client information</h3>'
    st.markdown(client_information_title, unsafe_allow_html=True)