import streamlit as st
from PIL import Image


########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/des.ico")
des = Image.open("asserts/des.png")
DS4A_Sogamoso = Image.open("asserts/DS4A-Sogamoso.png")

########################################################
# General settings
########################################################
st.set_page_config(
    page_title="Sogamoso School dropout",
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
# Page information
########################################################

st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">School dropout in Sogamoso</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:60%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)

col1, col2  = st.columns([1, 3])

col1.image(des)

col2.markdown("This project is part of [Data Science 4 All - DS4A](https://www.correlation-one.com/data-science-for-all-colombia)"\
            " training, and has two main objectives:")

objectives_list = '<ul style="list-style-type:disc;">'\
                    '<li>Building a classification model that will give a prediction about the probability of a student dropouts the school.<br>'\
                    'The model will be treated as a <strong>binary classification problem</strong>. So, 0 will be the class who does not dropout '\
                    'the school and 1 will be the class who dropouts the school.</li>'\
                    '<li>Build an interactive <strong>dashboard</strong> for <a href="https://www.sogamoso-boyaca.gov.co/" target="blank">Sogamoso municipality</a> '\
                    'to interpret the predictions made by the model,<br>'\
                    'and improve the  knowledge to allows the making-decision.</li>'\
                '</ul>'
col2.markdown(objectives_list, unsafe_allow_html=True)

col3, col4, col5  = st.columns([2, 1, 1])

col3.subheader("How to use it ?")
how_to_use_text = '<ul style="list-style-type:disc;">'\
                    '<li>You can navigate through the <strong>Home page</strong> where you will find information related with the project.</li>'\
                    '<li>Also, there are statistics available into the links <strong>General Statistics</strong> and <strong>Projections 2022</strong></li>'\
                    '<li>Finally, you can go to the <strong>Students prediction</strong> to know whether a specific client will pay the loan based on his information.</li>'\
                '</ul>'
col3.markdown(how_to_use_text, unsafe_allow_html=True)

col4.caption("&nbsp;")
col4.image(DS4A_Sogamoso)

col5.caption("&nbsp;")

st.subheader("Other information")
other_text = '<ul style="list-style-type:disc;">'\
                '<li><h4>Repository</h4>'\
                'You can find more information about the project\'s code in its <a href="https://github.com/samirhinojosa/school-dropout-in-sogamoso" target="_blank">Github\' repository</a></li>'\
            '</ul>'
st.markdown(other_text, unsafe_allow_html=True)