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
#map
import folium
import branca.colormap as cmp
from streamlit_folium import folium_static

########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/des.ico")

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
# Functions
########################################################

# BASE_URL="http://0.0.0.0:8008"
BASE_URL="http://34.71.10.158"

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

def graphs_improve(df, field, column):
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

    column.plotly_chart(fig, use_container_width=True)

def graphs_line(df, field):
    field_np = np.array(df[field])
    Ano = np.array(df['ANO'])
    Estado = np.array(df['ESTADO'])

    cross = pd.crosstab([Ano, field_np], Estado,  rownames=['Ano', str(field)], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]
    cross=pd.DataFrame(cross).reset_index()
    cross= cross[cross["Ano"]!=2022]
    cross.columns = ['Año', str(field),'% Deserción']

    title = "% de deserción por " + str(field) + " para cada año"
    fig = px.line(cross, x="Año", y='% Deserción',
                color=str(field), title=title)

    st.plotly_chart(fig, use_container_width=True)

def get_projections(QUERY_PARAMS = "?fields=ANO&fields=ESTADO"):
    API="/projections/"
    QUERY_PARAMS=str(QUERY_PARAMS)
    response = requests.get(BASE_URL+API+QUERY_PARAMS).json()
    if response:
        return response
    else:
        return "Error"

def rad_size(number):  #Probabilidad del 1 al 100, 6 posibles rangos
    if number < 16:  #funcion que usaremos mas adelante para poner los radios y colores de las ubicaciones
        return 1,'#D5C5FC'
    elif 500 <= number and number< 32:
        return 2,'#DC9248'
    elif 5000 <= number and number< 48:
        return 3,'#51C443'
    elif 15000 <= number and number< 64:
        return 4,'#436AC4'
    elif 30000 <= number and number< 80:
        return 5,'#CB6BE2'
    else:
        return 6,'#F80606'


# with st.sidebar.form('Form1'):
#     see_stratum_gender = st.checkbox("Stratum and gender")
#     # see_stats = st.checkbox("See stats")
#     st.warning("**Option(s)** will take more time.")
#     result = st.form_submit_button("Mostrar")

########################################################
# Map
########################################################

df = pd.read_csv(os.path.join(os.path.dirname(__file__), "../datasets/instituciones_2022.csv"))

year_to_filter = "2022"  

st.subheader('Map of % dropout by institution in ' + str(year_to_filter))

df['INSTITUCION_LATITUDE'] = df['INSTITUCION_LATITUDE'].astype(float)
df['INSTITUCION_LONGITUD'] = df['INSTITUCION_LONGITUD'].astype(float)

lat = list(df["INSTITUCION_LATITUDE"]) #latitud
lon = list(df["INSTITUCION_LONGITUD"]) #longitud
prob = list(df["% Deserción"]) #probabilidad
inst = list(df["INSTITUCION"]) #probabilidad


base_map = folium.Map(location=[5.7238722,-72.9546859], zoom_start=13)
linear = cmp.LinearColormap(
    ['#fef0d9','#66c2a4', '#fec44f', '#ffff33','#ff7f00','#de2d26'],
    index=[0,500, 5000, 15000, 30000,100000],
    vmin=1, vmax=100000,
    caption='% Dropout'  # Caption for Color scale or Legend
)
fg = folium.FeatureGroup(name="My Map") #nombre del mapa
for lt, ln, prob, inst in zip(lat, lon, prob, inst):
    fg.add_child(folium.CircleMarker(location=[lt, ln], radius=rad_size(prob)[0], popup="Institución: " + str(inst) + " \n Probability:"+str(prob),
                                        fill_color=rad_size(prob)[1], fill=True, fill_opacity=0.7, color='Black', opacity=0.4))

base_map.add_child(fg)

# call to render Folium map in Streamlit
linear.add_to(base_map)
folium_static(base_map)

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

########################################################
# Students graphs
########################################################


# if see_stratum_gender:
    # stratum_gender_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">📊 Stratum and Gender</h3>'
    # st.markdown(stratum_gender_title, unsafe_allow_html=True)
    ## Estrato
Estrato_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=ESTRATO"))
# graphs(Estrato_df, "ESTRATO")
graphs_improve(Estrato_df, "ESTRATO", col1)

## Genero

Gender_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=GENERO"))
# graphs(Gender_df, "GENERO")
graphs_improve(Gender_df, "GENERO", col2)


## Zona

Zona_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=INSTITUCION_ZONA"))
# graphs(Zona_df, "INSTITUCION_ZONA")
graphs_improve(Zona_df, "INSTITUCION_ZONA", col3)


## Caracter de la institucion

Caracter_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=INSTITUCION_CARACTER"))
# graphs(Caracter_df, "INSTITUCION_CARACTER")
graphs_improve(Caracter_df, "INSTITUCION_CARACTER", col4)


## Edad

Edad_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=CATEGORICAL_EDAD"))
graphs(Edad_df, "CATEGORICAL_EDAD")

## Intitucion

Institucion_df = pd.DataFrame.from_dict(get_projections(QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=INSTITUCION"))
graphs(Institucion_df, "INSTITUCION")