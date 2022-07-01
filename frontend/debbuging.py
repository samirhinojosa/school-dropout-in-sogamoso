import os
import scipy
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df_students = pd.read_csv(os.path.join(os.path.dirname(__file__), "datasets/df_students.csv"))
# pd.set_option('display.max_columns', None)
# print(df_students.head())
# da=pd.crosstab(index=df_students['AÑO'],
#             columns=df_students['DISCAPACIDAD'])#, normalize='index')
# axes = da.plot.bar()
# axes.set_xlabel('Año')
# axes.set_ylabel('Número de estudiantes')
# axes.set_title('Discapacidad de los estudiantes por año')
# plt.figure(figsize = (30, 10))
# plt.show()


# Data for plotting
# t = np.arange(0.0, 2.0, 0.01)
# s = 1 + np.sin(2 * np.pi * t)

# fig, ax = plt.subplots()
# ax.plot(t, s)

# ax.set(xlabel='time (s)', ylabel='voltage (mV)',
#        title='About as simple as it gets, folks')
# ax.grid()

# fig.savefig("test.png")
# plt.show()

# Arreglo de variables:

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
df_students['CATEGORICAL_EDAD']

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
            columns=df_students['ESTRATO'])#, normalize='index')
axes = da.plot.bar()
axes.set_xlabel('Año')
axes.set_ylabel('Número de estudiantes')
axes.set_title('Estrato de los estudiantes por año')
plt.figure(figsize = (30, 10))

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
plt.show()