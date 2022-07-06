import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image
import plotly.graph_objects as go

########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/des.ico")

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
# Page information
########################################################
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Student Prediction - Sogamoso School dropout</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:90%; text-align:left; margin-left:0; margin-top:0">'
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
# Functions to call the EndPoints
########################################################
@st.cache
def students():
    # Getting students Id
    response = requests.get("http://backend:8008/api/students").json()
    if response:
        return response["StudentsId"]
    else:
        return "Error"

def student_details(id):
    # Getting students's details
    response = fetch(session, f"http://backend:8008/api/students/{id}")
    if response:
        return response
    else:
        return "Error"

def student_prediction(id):
    # Getting students's prediction
    response = fetch(session, f"http://backend:8008/api/predictions/students/{id}")
    if response:
        return response
    else:
        return "Error"


########################################################
# Sidebar section
########################################################
client_selection_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🔎 Student selection</h3>'
st.sidebar.markdown(client_selection_title, unsafe_allow_html=True)

with st.sidebar.form('Form1'):
    student_id = st.selectbox(
        "Student Id list", students()
    )
    see_local_interpretation = st.checkbox("See local interpretation")
    see_stats = st.checkbox("See stats")
    st.warning("**Option(s)** will take more time.")
    result = st.form_submit_button("Predict")

st.sidebar.info("Select a student to **get** information related to **probability** that he/she " \
                "**dropouts out** of school.\nIn addition, you can analyze some stats for this student.")


########################################################
# Page body
########################################################
# if see_local_interpretation:
    
#     client_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📋 Client information</h3>'
#     st.markdown(client_information_title, unsafe_allow_html=True)

if result:

    student_information_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📋 Student information</h3>'
    st.markdown(student_information_title, unsafe_allow_html=True)

    data = student_details(student_id)

    prediction = student_prediction(student_id)
    drop_out = prediction["dropOut"]
    threshold = float(prediction["threshold"] * 100)
    probability_value_0 = prediction["probability"][0] * 100
    probability_value_1 = float(prediction["probability"][1] * 100)

    if drop_out == "Yes":
        success_msg = "Based on the **threshold " + str(threshold) + \
            "**, and the given information, the student **will NOT DROPOUT**"
        st.success(success_msg)
    else:
        error_msg = "Based on the **threshold " + str(threshold) + \
            "**, and the given information, the student **will DROPOUT**"
        st.error(error_msg)

    con_student_detail = st.container()

    col1_csd, col2_csd, col3_csd, col4_csd = con_student_detail.columns([2, 1, 1, 1])

    with col1_csd:
        
        st.caption("&nbsp;")

        figP = go.Figure(
                go.Indicator(
                    mode = "gauge+number",
                    value = probability_value_1,
                    domain = {"x": [0, 1], "y": [0, 1]},
                    gauge = {
                        "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "darkblue", "tick0": 0, "dtick": 20},
                        "bar": {"color": "darkblue"},# LawnGreen
                        "bgcolor": "white",
                        "steps": [
                            {"range": [0, threshold], "color": "#27AE60"},#Green
                            {"range": [threshold, 100], "color": "#E74C3C"}#red
                        ],
                    }
                )   
            )

        figP.update_layout(
            paper_bgcolor="white",
            font={
                "color": "darkblue",
                "family": "sans serif"
            },
            autosize=False,
            width=500,
            height=300,
            margin=dict(
                l=50, r=50, b=0, t=0, pad=0
            ),
            annotations=[
                go.layout.Annotation(
                    text=f"<b>Probability that the student will not drop out</b>",
                    x=0.5, xanchor="center", xref="paper",
                    y=0, yanchor="bottom", yref="paper",
                    showarrow=False,
                )
            ]
        )
        
        col1_csd.plotly_chart(figP, config=config, use_container_width=True)

    with col2_csd:
        st.caption("&nbsp;")
        st.markdown("**Estudiante id:**")
        st.caption(data["studentId"])
        st.markdown("**Discapacidad:**")
        st.caption(data["disability"])
        st.markdown("**Institución:**")
        st.caption(data["institution"])

    with col3_csd:
        st.caption("&nbsp;")
        st.markdown("**Género:**")
        st.caption(data["gender"])
        st.markdown("**País de origen:**")
        st.caption(data["countryOrigin"])
        st.markdown("**Grado:**")
        st.caption(data["schoolGrade"])

    with col4_csd:
        st.caption("&nbsp;")
        st.markdown("**Edad:**")
        st.caption(data["age"])
        st.markdown("**Estrato:**")
        st.caption(data["stratum"])
        st.markdown("**Jornada:**")
        st.caption(data["schoolDay"])
        
