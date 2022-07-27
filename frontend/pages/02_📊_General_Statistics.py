import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import requests
from PIL import Image
import numpy as np
import pandas as pd
import folium
import branca.colormap as cmp
from streamlit_folium import st_folium



########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/des.ico")


########################################################
# General settings
########################################################
st.set_page_config(
    page_title="General Statistics - Sogamoso School dropout",
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
    .stSlider{{
        width: 450px !important;
        
    }}
    .element-container.css-fg6p3w.e1tzin5v3.stAlert{{
        width: 750px !important;
        
    }}
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
st_title = '<h1 style="color:#262730; margin-bottom:0; padding: 1.25rem 0px 0rem;">General Statistics</h1>'
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
# Functions to call the EndPoints
########################################################
if "statistics_general" not in st.session_state:

    @st.cache
    def statistics_general(QUERY_PARAMS="?fields=anyo&fields=estado"):
        # General statistics based on year and state
        response = requests.get("http://backend:8008/api/statistics/general/").json()

        st.session_state["statistics_general"] = response
                    
        if response:
            return response
        else:
            return "Error"


########################################################
# Sidebar section
########################################################
client_selection_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🔎 Options to see</h3>'
st.sidebar.markdown(client_selection_title, unsafe_allow_html=True)

with st.sidebar.form('Form1'):
    see_dropout_map = st.checkbox("Dropout map")
    see_historical_dropout = st.checkbox("Historical dropout")
    st.warning("**Option(s)** will take more time.")
    result = st.form_submit_button("Show")


########################################################
# Page body
########################################################


########################################################
# -----------> Dropout map
########################################################
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


if see_dropout_map:

    dropout_map_title = '<h3 style="margin-bottom:0; padding: 0.5rem 0px 1rem;">🗺️ Dropout map</h3>'
    st.markdown(dropout_map_title, unsafe_allow_html=True)

    con_dropout_map = st.container()

    col1_cdm, col2_cdm = con_dropout_map.columns([2, 1])

    with col1_cdm:

        st.info("Select a year to get the statistics by school")

        if "df_drop_map" not in st.session_state:
            st.session_state["df_drop_map"] = pd.read_csv("datasets/instituciones.csv")

        year_to_filter = st.slider("", 2013, 2021, 2013)  #slider, año inicial, año final, año por defecto en pantalla

        # Average title
        df_year_map = st.session_state["df_drop_map"][st.session_state["df_drop_map"]['Año'] == year_to_filter] #si se escoge un año particular

        st.markdown("Dropout map by institucion in " + str(year_to_filter) +\
                    " with average of " + str(round(df_year_map['% Deserción'].mean(), 2)))


        st.session_state["df_drop_map"]['INSTITUCION_LATITUDE'] = st.session_state["df_drop_map"]['INSTITUCION_LATITUDE'].astype(float)
        st.session_state["df_drop_map"]['INSTITUCION_LONGITUD'] = st.session_state["df_drop_map"]['INSTITUCION_LONGITUD'].astype(float)

        lat = list(st.session_state["df_drop_map"]["INSTITUCION_LATITUDE"]) #latitud
        lon = list(st.session_state["df_drop_map"]["INSTITUCION_LONGITUD"]) #longitud
        prob = list(st.session_state["df_drop_map"]["% Deserción"]) #probabilidad
        inst = list(st.session_state["df_drop_map"]["INSTITUCION"])

        base_map = folium.Map(location=[5.7238722,-72.9546859], zoom_start=12)

        linear = cmp.LinearColormap(
            ['#fef0d9','#66c2a4', '#fec44f', '#ffff33','#ff7f00','#de2d26'],
            index=[0,500, 5000, 15000, 30000,100000],
            vmin=1, vmax=100000,
            caption='% Dropout'  # Caption for Color scale or Legend
        )

        fg = folium.FeatureGroup(name="My Map") #nombre del mapa

        for lt, ln, prob, inst in zip(lat, lon, prob, inst):
            fg.add_child(folium.CircleMarker(location=[lt, ln], radius=rad_size(prob)[0], 
                                                popup="Institución: " + str(inst) +  " \n % de deserción"+str(prob),
                                                fill_color=rad_size(prob)[1], fill=True, fill_opacity=0.7, color='Black', 
                                                opacity=0.4))

        base_map.add_child(fg)

        # call to render Folium map in Streamlit
        linear.add_to(base_map)
        st_folium(base_map, width=725)


    with col2_cdm:
        st.caption("&nbsp;")
        st.caption("&nbsp;")
        st.caption("&nbsp;")
        st.caption("&nbsp;")
        st.caption("&nbsp;")



########################################################
# -----------> Graphs
########################################################

def graphs(df, field):
    field_np = np.array(df[field])
    Ano = np.array(df['anyo'])
    Estado = np.array(df['estado'])

    cross = pd.crosstab([Ano, field_np], Estado,  rownames=['anyo', str(field)], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]
    cross=pd.DataFrame(cross).reset_index()
    cross= cross[cross["anyo"]!=2022]
    cross.columns = ['Año', str(field),'% Deserción']

    title = "% de deserción por " + str(field) + " para cada año"
    fig = px.bar(cross, x="Año", y='% Deserción',
                color=str(field), barmode = 'group'
                ,title=title)

    st.plotly_chart(fig, use_container_width=True)

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


## Trend

Peridano_df = pd.DataFrame.from_dict(statistics_general(QUERY_PARAMS="?fields=anyo&fields=estado&fields=per_id_anyo"))


tabla_fin = pd.DataFrame(Peridano_df.groupby(["estado", "anyo"])["per_id_anyo"].count()).reset_index()

tabla_fin1 = pd.DataFrame(pd.pivot_table(data=tabla_fin,
                        index=["anyo"],
                        columns=["estado"],
                        values="per_id_anyo")).reset_index()
tabla_fin1['% Deserción'] = tabla_fin1[1]/(tabla_fin1[1]+tabla_fin1[0])*100
tabla_fin1= tabla_fin1[["anyo",'% Deserción']]
tabla_fin1=pd.DataFrame(tabla_fin1)
tabla_fin1.columns = ["anyo", '% Deserción']
tabla_fin1.set_index("anyo", inplace = True)

fig = px.line(tabla_fin1, x=tabla_fin1.index, y="% Deserción", title='Histórico % de deserción por años', markers=True)
st.plotly_chart(fig, use_container_width=True)

