import os
import scipy
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
from PIL import Image

########################################################
# Loading images to the website
########################################################
icon = Image.open("asserts/sogamoso.ico")

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
# Update information
########################################################

df_students = pd.read_csv(os.path.join(os.path.dirname(__file__), "../to_delete/datasets/df_students.csv"))

# Variable EDAD: Agrupar/Categorizar dado los atípicos que tiene

def age_clasification(age):
    if 0 <= age <= 5:
        new_age = '1. 0-5'
    if 6 <= age <= 10:
        new_age = '2. 6-10'
    if 11 <= age <= 15:
        new_age = '3. 11-15'
    if 16 <= age <= 20:
        new_age = '4. 16-20'
    if 21 <= age <= 25:
        new_age = '5. 21-25'
    if 26 <= age:
        new_age = '6. 26+'
    return new_age


def group_vars(df_students):

    # Variable DISCAPACIDAD: pasar de categórica a dicotómica
    df_students.loc[df_students['DISCAPACIDAD'] != 'NO APLICA', 'DISCAPACIDAD'] = 1
    df_students.loc[df_students['DISCAPACIDAD'] == 'NO APLICA', 'DISCAPACIDAD'] = 0

    # Variable ESTRATO: Agrupar/Categorizar dado los atípicos que tiene
    df_students.loc[df_students['ESTRATO'] == 'ESTRATO 4', 'ESTRATO'] = 'ESTRATO ALTO'
    df_students.loc[df_students['ESTRATO'] == 'ESTRATO 5', 'ESTRATO'] = 'ESTRATO ALTO'
    df_students.loc[df_students['ESTRATO'] == 'ESTRATO 6', 'ESTRATO'] = 'ESTRATO ALTO'
    df_students['ESTRATO'].unique()
    df_students['ESTRATO'].value_counts()


    df_students['CATEGORICAL_EDAD'] = df_students['EDAD'].apply(age_clasification)

    return df_students

df_students = group_vars(df_students)


########################################################
# Students graphs - trend
########################################################


tabla_fin = pd.DataFrame(df_students.groupby(["ESTADO",'ANO'])['PER_ID_ANO'].count()).reset_index()
tabla_fin1 = pd.DataFrame(pd.pivot_table(data=tabla_fin,
                        index=['ANO'],
                        columns=['ESTADO'],
                        values='PER_ID_ANO')).reset_index()

tabla_fin1['calc_per'] = tabla_fin1[1]/(tabla_fin1[1]+tabla_fin1[0])*100
tabla_fin1= tabla_fin1[['ANO','calc_per']]#
tabla_fin1=pd.DataFrame(tabla_fin1)
tabla_fin1.set_index('ANO', inplace = True)
x = tabla_fin1.index
y = tabla_fin1['calc_per']

fig = px.line(tabla_fin1, x =  tabla_fin1.index,
              y = tabla_fin1['calc_per'],
              title = 'Students dropout historic trend')

st.plotly_chart(fig, use_container_width=True)


# Estrato

Estado = np.array(df_students['ESTADO'])
Ano = np.array(df_students["ANO"])
Estrato = np.array(df_students['ESTRATO'])
# form the cross tab
Estrato = pd.crosstab([Ano, Estrato], Estado,  rownames=['Ano', 'Estrato'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]
Estrato=pd.DataFrame(Estrato).reset_index()
Estrato= Estrato[Estrato["Ano"]!=2022]
Estrato.columns = ['Año','Estrato','% Deserción']

 
fig_estrato = px.bar(Estrato, x="Año", y='% Deserción',
             color="Estrato", barmode = 'group'
            ,title='% de deserción por estrato para cada año')

st.plotly_chart(fig_estrato, use_container_width=True)


# Genero

Genero = np.array(df_students['GENERO'])
# form the cross tab
gen = pd.crosstab([Ano, Genero], Estado,  rownames=['Ano', 'Género'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]

gen=pd.DataFrame(gen).reset_index()
gen= gen[gen["Ano"]!=2022]
gen.columns = ['Año', 'Género','% Deserción']

 
fig_genero = px.bar(gen, x="Año", y='% Deserción',
             color="Género", barmode = 'group'
            ,title='% de deserción por género para cada año')

st.plotly_chart(fig_genero, use_container_width=True)


# Zona

Zona = np.array(df_students['INSTITUCION_ZONA'])
# form the cross tab
Zona = pd.crosstab([Ano, Zona], Estado,  rownames=['Ano', 'INSTITUCION_ZONA'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]

Zona=pd.DataFrame(Zona).reset_index()
Zona= Zona[Zona["Ano"]!=2022]
Zona.columns = ['Año', 'Zona','% Deserción']

 
fig_zona = px.bar(Zona, x="Año", y='% Deserción',
             color="Zona", barmode = 'group'
            ,title='% de deserción por Zona para cada año')

st.plotly_chart(fig_zona, use_container_width=True)


# Caracter de la institucion

Caracter = np.array(df_students['INSTITUCION_CARACTER'])
# form the cross tab
Caracter = pd.crosstab([Ano, Caracter], Estado,  rownames=['Ano', 'INSTITUCION_CARACTER'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]

Caracter=pd.DataFrame(Caracter).reset_index()
Caracter= Caracter[Caracter["Ano"]!=2022]
Caracter.columns = ['Año', 'Carácter','% Deserción']

 
fig_caracter = px.bar(Caracter, x="Año", y='% Deserción',
             color="Carácter", barmode = 'group'
            ,title='% de deserción por Carácter para cada año')

st.plotly_chart(fig_caracter, use_container_width=True)


# Edad

Edad = np.array(df_students['CATEGORICAL_EDAD'])
# form the cross tab
Edad = pd.crosstab([Ano, Edad], Estado,  rownames=['Ano', 'CATEGORICAL_EDAD'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]

Edad=pd.DataFrame(Edad).reset_index()
Edad= Edad[Edad["Ano"]!=2022]
Edad.columns = ['Año', 'Edad','% Deserción']

 
fig_edad = px.bar(Edad, x="Año", y='% Deserción',
             color="Edad", barmode = 'group'
            ,title='% de deserción por grupo de edad para cada año')

st.plotly_chart(fig_edad, use_container_width=True)


# Intitucion

Ins = np.array(df_students['INSTITUCION'])
# form the cross tab
Ins = pd.crosstab([Ano, Ins], Estado,  rownames=['Ano', 'INSTITUCION'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
                                              axis=1)[1]

Ins=pd.DataFrame(Ins).reset_index()
Ins= Ins[Ins["Ano"]!=2022]
Ins.columns = ['Año', 'Institución','% Deserción']

fig_institucion = px.line(Ins, x='Año', y='% Deserción', color='Institución', markers=True)

st.plotly_chart(fig_institucion, use_container_width=True)
