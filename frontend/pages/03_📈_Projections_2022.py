import os
import scipy
import requests
import numpy as np
import pandas as pd
from PIL import Image
import seaborn as sns
import streamlit as st
from operator import ge
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/sogamoso.ico")

########################################################
# General settings
########################################################
st.set_page_config(
    page_title="Projections 2022 - Sogamoso School dropout",
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
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">Sogamoso school dropout</h1>'
st_title_hr = '<hr style="background-color:#F0F2F6; width:60%; text-align:left; margin-left:0; margin-top:0">'
st.markdown(st_title, unsafe_allow_html=True)
st.markdown(st_title_hr, unsafe_allow_html=True)


########################################################
# Students graphs
########################################################

BASE_URL="http://0.0.0.0:8008"

def graphs(df, field):
    field_np = np.array(df[field])
    Ano = np.array(df['ANO'])
    Estado = np.array(df['ESTADO'])

    cross = pd.crosstab([Ano, field_np], Estado,  rownames=['Ano', str(field)], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]
    cross=pd.DataFrame(cross).reset_index()
    cross.columns = ['Año', str(field),'% Deserción']

    title = "Estimacion  del % de deserción por " + str(field) + " para 2022"
    fig = px.bar(cross, x="Año", y='% Deserción',
                color=str(field), barmode = 'group'
                ,title=title)

    st.plotly_chart(fig, use_container_width=True)

def get_projections(QUERY_PARAMS = "?fields=ANO&fields=ESTADO"):
    API="/projections/"
    QUERY_PARAMS=str(QUERY_PARAMS)
    response = requests.get(BASE_URL+API+QUERY_PARAMS).json()
    if response:
        return response
    else:
        return "Error"


## Estrato

Estrato_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=ESTRATO"))
graphs(Estrato_df, "ESTRATO")


## Genero

Gender_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=GENERO"))
graphs(Gender_df, "GENERO")


## Zona

Zona_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=INSTITUCION_ZONA"))
graphs(Zona_df, "INSTITUCION_ZONA")


## Caracter de la institucion

Caracter_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=INSTITUCION_CARACTER"))
graphs(Caracter_df, "INSTITUCION_CARACTER")


## Edad

Edad_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=CATEGORICAL_EDAD"))
graphs(Edad_df, "CATEGORICAL_EDAD")