import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import joblib
import shap


########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/des.ico")

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
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Student Prediction</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:90%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)

st.info("Select a student to **get** information related to **probability** that he/she " \
                "**dropouts** of school.\nIn addition, you can analyze some stats for this student.")


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
    response = requests.get("http://0.0.0.0:8008/api/students").json()
    if response:
        return response["StudentsId"]
    else:
        return "Error"

def student_details(id):
    # Getting students's details
    response = fetch(session, f"http://0.0.0.0:8008/api/students/{id}")
    if response:
        return response
    else:
        return "Error"

def student_prediction(id):
    # Getting students's prediction
    response = fetch(session, f"http://0.0.0.0:8008/api/predictions/students/{id}")
    if response:
        return response
    else:
        return "Error"

def student_shap_prediction(id):
    # Getting students's prediction
    response = fetch(session, f"http://0.0.0.0:8008/api/predictions/shap/students/{id}")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_ages():
    # Getting General statistics about ages
    response = fetch(session, f"http://0.0.0.0:8008/api/statistics/ages")
    if response:
        return response
    else:
        return "Error"

@st.cache
def statistical_stratums():
    # Getting General statistics about stratums
    response = fetch(session, f"http://0.0.0.0:8008/api/statistics/stratums")
    if response:
        return response
    else:
        return "Error"


########################################################
# To show the SHAP image
########################################################
def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


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


########################################################
# Page body
########################################################
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

    con_student_detail, con_local_interpretation, con_stats = (st.container() for i in range(3))

    col1_csd, col2_csd, col3_csd, col4_csd = con_student_detail.columns([2, 1, 1, 1])

    with col1_csd:
        
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
                    text=f"<b>Probability that the student will dropout</b>",
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

    if see_local_interpretation:

        with con_local_interpretation:
    
            local_interpretation_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📉 Local interpretation</h3>'
            st.markdown(local_interpretation_title, unsafe_allow_html=True)

            data_shap = student_shap_prediction(student_id)
            data_shap = pd.read_json(data_shap)
            
            if "shap_values" not in st.session_state:
                st.session_state["shap_values"] = joblib.load("models/shap_values_20220705.pkl")

            st_shap(shap.plots.force(st.session_state["shap_values"][data["shapPosition"]]))
    
    if see_stats:

        # Defining variables to use in graphs
        group_labels = ["Dropout", "Not dropout"]
        colors=["Red", "Green"]

        with con_stats:

            student_statistics_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📊 Student statistics</h3>'
            st.markdown(student_statistics_title, unsafe_allow_html=True)

            col1_gs_1, col2_gs_1 = con_stats.columns(2)

            with col1_gs_1:

                if "ages" not in st.session_state:
                    st.session_state["ages"] = statistical_ages()

                ages_dropout = st.session_state["ages"]["ages_dropout"]
                ages_not_dropout = st.session_state["ages"]["ages_not_dropout"]
                ages_dropout_list = [int(key) for key, val in ages_dropout.items() for _ in range(val)]
                ages_not_dropout_list = [int(key) for key, val in ages_not_dropout.items() for _ in range(val)]

                fig_ages = ff.create_distplot([ages_dropout_list, ages_not_dropout_list],
                                                group_labels, show_hist=False, show_rug=False, 
                                                colors=colors)

                fig_ages.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Student's age vs other students",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="Ages",
                        yaxis_title="density",
                        legend={
                            "traceorder" : "normal"
                        }
                    )

                fig_ages.add_vline(x=data["age"], line_width=3,
                                line_dash="dash", line_color="blue", annotation_text="Student's age")

                col1_gs_1.plotly_chart(fig_ages, config=config, use_container_width=True)
            
            with col2_gs_1:

                if "stratums" not in st.session_state:
                    st.session_state["stratums"] = statistical_stratums()

                stratums_dropout = st.session_state["stratums"]["stratum_dropout"]
                stratums_not_dropout = st.session_state["stratums"]["stratum_not_dropout"]

                stratums_dropout_list = [int(key) for key, val in stratums_dropout.items() for _ in range(val)]
                stratums_not_dropout_list = [int(key) for key, val in stratums_not_dropout.items() for _ in range(val)]
                
                fig_stratums = ff.create_distplot([stratums_dropout_list, stratums_not_dropout_list],
                                                group_labels, show_hist=False, show_rug=False, 
                                                colors=colors)

                fig_stratums.update_layout(
                        paper_bgcolor="white",
                        font={
                            "family": "sans serif"
                        },
                        autosize=False,
                        width=500,
                        height=360,
                        margin=dict(
                            l=50, r=50, b=0, t=20, pad=0
                        ),
                        title={
                            "text" : "Student's stratum vs other students",
                            "y" : 1,
                            "x" : 0.45,
                            "xanchor" : "center",
                            "yanchor" : "top"
                        },
                        xaxis_title="Stratums",
                        yaxis_title="density",
                        legend={
                            "traceorder" : "normal"
                        }
                    )

                fig_stratums.add_vline(x=int(data["stratum"].replace("ESTRATO ", "")), line_width=3,
                                line_dash="dash", line_color="blue", annotation_text="Student's stratum")

                col2_gs_1.plotly_chart(fig_stratums, config=config, use_container_width=True)