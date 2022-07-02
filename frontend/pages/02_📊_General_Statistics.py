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
# Students graphs
########################################################

df_students = pd.read_csv(os.path.join(os.path.dirname(__file__), "../to_delete/datasets/df_students.csv"))

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



# da=pd.crosstab(index=df_students['ANO'],
#             columns=df_students['DISCAPACIDAD'])#, normalize='index')
# axes = da.plot.bar()
# axes.set_xlabel('Año')
# axes.set_ylabel('Número de estudiantes')
# axes.set_title('Discapacidad de los estudiantes por año')
# # plt.figure(figsize = (30, 10))
# st.pyplot(fig)

# Variable DISCAPACIDAD: pasar de categórica a dicotómica
df_students.loc[df_students['DISCAPACIDAD'] != 'NO APLICA', 'DISCAPACIDAD'] = 1
df_students.loc[df_students['DISCAPACIDAD'] == 'NO APLICA', 'DISCAPACIDAD'] = 0

# Variable ESTRATO: Agrupar/Categorizar dado los atípicos que tiene
df_students.loc[df_students['ESTRATO'] == 'ESTRATO 4', 'ESTRATO'] = 'ESTRATO ALTO'
df_students.loc[df_students['ESTRATO'] == 'ESTRATO 5', 'ESTRATO'] = 'ESTRATO ALTO'
df_students.loc[df_students['ESTRATO'] == 'ESTRATO 6', 'ESTRATO'] = 'ESTRATO ALTO'
df_students['ESTRATO'].unique()
df_students['ESTRATO'].value_counts()

# Variable EDAD: Agrupar/Categorizar dado los atípicos que tiene
def age_clasification(age):
    if 0 <= age <= 5:
        new_age = '0-5'
    if 6 <= age <= 8:
        new_age = '6-8'
    if 9 <= age <= 10:
        new_age = '9-10'
    if 11 <= age <= 20:
        new_age = str(age)
    if 21 <= age <= 22:
        new_age = '21-22'
    if 23 <= age <= 25:
        new_age = '23-25'
    if 26 <= age:
        new_age = '26+'
    return new_age

df_students['CATEGORICAL_EDAD'] = df_students['EDAD'].apply(age_clasification)
# print(df_students['CATEGORICAL_EDAD'].unique())
# print(df_students['CATEGORICAL_EDAD'].value_counts())
# df_students['CATEGORICAL_EDAD']

da=pd.crosstab(index=df_students['ANO'],
            columns=df_students['DISCAPACIDAD'])#, normalize='index')
axes = da.plot.bar()
axes.set_xlabel('Año')
axes.set_ylabel('Número de estudiantes')
axes.set_title('Discapacidad de los estudiantes por año')
plt.figure(figsize = (30, 10))

# df2=df_students[df_students["DISCAPACIDAD"]== 1]

# axes = df2.plot.bar()
# axes.set_xlabel('Año')
# axes.set_ylabel('Número de estudiantes')
# axes.set_title('Discapacidad de los estudiantes por año')
# plt.figure(figsize = (30, 10))


da=pd.crosstab(index=df_students['ANO'],
            columns=df_students['CATEGORICAL_EDAD'])#, normalize='index')
axes = da.plot.bar()
axes.set_xlabel('Año')
axes.set_ylabel('Número de estudiantes')
axes.set_title('Edad de los estudiantes por año')
plt.figure(figsize = (30, 10))

plt.figure(figsize = (20, 10))
plt.xticks(da.index,
                     rotation=70, size=12, horizontalalignment="right")
plt.title("Promedio anual de estudiantes por Institución", size=16)
plt.xlabel("Institución", size=14)
plt.ylabel("Número de estudiantes", size=14)
sns.barplot(data=da)

fig, ax1 = plt.subplots(figsize=(10, 7))
plot = sns.barplot(x=df_students["ESTRATO"].value_counts(ascending=True).index,
                   y=df_students["ESTRATO"].value_counts(ascending=True))
for p in plot.patches:
    plot.annotate(format(p.get_height(), ".0f"), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="center", xytext=(0, 9), textcoords="offset points")
plot.set_xticklabels(labels=df_students["ESTRATO"].value_counts(ascending=True).index,
                     size=12, horizontalalignment="center")
plt.title("Número de estudiantes por Estrato", size=16)
plt.xlabel("Estrato", size=14)
plt.ylabel("Número de estudiantes", size=14)
st.pyplot(fig)



########################################################
# Graphic test
########################################################

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
         hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)