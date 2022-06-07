import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

st.title('School droput in Sogamoso / Team 112 DS4A')

df_students_2022 = pd.read_csv("alumnos_s_oficial2022.csv", encoding="cp1252", sep=";")

# Add histogram data
# x1 = np.random.randn(200) - 2
x2 = np.random.randint(11, size=(20))
x3 = np.random.randint(11, size=(20))

# Group data together
hist_data = [x2, x3]

group_labels = ['Students grade dist 2021', 'Students grade dist 2022']

# Create distplot with custom bin_size
# fig = ff.create_distplot(
#          hist_data, group_labels, bin_size=[.1, .25, .5])
fig = ff.create_distplot(
         hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)

fig_1, ax1 = plt.subplots(figsize=(10, 7))
plot = sns.barplot(x=df_students_2022.groupby("MODELO")["INSTITUCION"].nunique().sort_values().index, 
                   y=df_students_2022.groupby("MODELO")["INSTITUCION"].nunique().sort_values())
for p in plot.patches:
    plot.annotate(format(p.get_height(), ".1f"), (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha="center", va="center", xytext=(0, 9), textcoords="offset points")
plot.set_xticklabels(labels=df_students_2022["MODELO"].value_counts(ascending=True).index,
                     rotation=70, size=12, horizontalalignment="right")
plt.title("Número de Instituciones por Modelo", size=16)
plt.xlabel("Modelo", size=14)
plt.ylabel("Número de instituciones", size=14)
# plt.show()

st.pyplot(fig_1, use_container_width=True)