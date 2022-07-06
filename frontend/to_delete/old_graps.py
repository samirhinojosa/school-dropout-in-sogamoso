



# # Estrato

# Estado = np.array(df_students['ESTADO'])
# Ano = np.array(df_students["ANO"])
# Estrato = np.array(df_students['ESTRATO'])
# # form the cross tab
# Estrato = pd.crosstab([Ano, Estrato], Estado,  rownames=['Ano', 'Estrato'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]
# Estrato=pd.DataFrame(Estrato).reset_index()
# Estrato= Estrato[Estrato["Ano"]!=2022]
# Estrato.columns = ['Año','Estrato','% Deserción']

 
# fig_estrato = px.bar(Estrato, x="Año", y='% Deserción',
#              color="Estrato", barmode = 'group'
#             ,title='% de deserción por estrato para cada año')

# st.plotly_chart(fig_estrato, use_container_width=True)



# Genero = np.array(Gender_df['GENERO'])
# Ano = np.array(Gender_df['ANO'])
# Estado = np.array(Gender_df['ESTADO'])
# # form the cross tab
# gen = pd.crosstab([Ano, Genero], Estado,  rownames=['Ano', 'Género'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# gen=pd.DataFrame(gen).reset_index()
# gen= gen[gen["Ano"]!=2022]
# gen.columns = ['Año', 'Género','% Deserción']

 
# fig_genero = px.bar(gen, x="Año", y='% Deserción',
#              color="Género", barmode = 'group'
#             ,title='% de deserción por género para cada año')

# st.plotly_chart(fig_genero, use_container_width=True)



#####

# Genero = np.array(df_students['GENERO'])
# # form the cross tab
# gen = pd.crosstab([Ano, Genero], Estado,  rownames=['Ano', 'Género'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# gen=pd.DataFrame(gen).reset_index()
# gen= gen[gen["Ano"]!=2022]
# gen.columns = ['Año', 'Género','% Deserción']

 
# fig_genero = px.bar(gen, x="Año", y='% Deserción',
#              color="Género", barmode = 'group'
#             ,title='% de deserción por género para cada año')

# st.plotly_chart(fig_genero, use_container_width=True)


# # Zona

# Zona = np.array(df_students['INSTITUCION_ZONA'])
# # form the cross tab
# Zona = pd.crosstab([Ano, Zona], Estado,  rownames=['Ano', 'INSTITUCION_ZONA'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# Zona=pd.DataFrame(Zona).reset_index()
# Zona= Zona[Zona["Ano"]!=2022]
# Zona.columns = ['Año', 'Zona','% Deserción']

 
# fig_zona = px.bar(Zona, x="Año", y='% Deserción',
#              color="Zona", barmode = 'group'
#             ,title='% de deserción por Zona para cada año')

# st.plotly_chart(fig_zona, use_container_width=True)


# # Caracter de la institucion

# Caracter = np.array(df_students['INSTITUCION_CARACTER'])
# # form the cross tab
# Caracter = pd.crosstab([Ano, Caracter], Estado,  rownames=['Ano', 'INSTITUCION_CARACTER'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# Caracter=pd.DataFrame(Caracter).reset_index()
# Caracter= Caracter[Caracter["Ano"]!=2022]
# Caracter.columns = ['Año', 'Carácter','% Deserción']

 
# fig_caracter = px.bar(Caracter, x="Año", y='% Deserción',
#              color="Carácter", barmode = 'group'
#             ,title='% de deserción por Carácter para cada año')

# st.plotly_chart(fig_caracter, use_container_width=True)


# # Edad

# Edad = np.array(df_students['CATEGORICAL_EDAD'])
# # form the cross tab
# Edad = pd.crosstab([Ano, Edad], Estado,  rownames=['Ano', 'CATEGORICAL_EDAD'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# Edad=pd.DataFrame(Edad).reset_index()
# Edad= Edad[Edad["Ano"]!=2022]
# Edad.columns = ['Año', 'Edad','% Deserción']

 
# fig_edad = px.bar(Edad, x="Año", y='% Deserción',
#              color="Edad", barmode = 'group'
#             ,title='% de deserción por grupo de edad para cada año')

# st.plotly_chart(fig_edad, use_container_width=True)


# # Intitucion

# Ins = np.array(df_students['INSTITUCION'])
# # form the cross tab
# Ins = pd.crosstab([Ano, Ins], Estado,  rownames=['Ano', 'INSTITUCION'], colnames=['Estado']).apply(lambda r: r/r.sum() *100,
#                                               axis=1)[1]

# Ins=pd.DataFrame(Ins).reset_index()
# Ins= Ins[Ins["Ano"]!=2022]
# Ins.columns = ['Año', 'Institución','% Deserción']

# fig_institucion = px.line(Ins, x='Año', y='% Deserción', color='Institución', markers=True)

# st.plotly_chart(fig_institucion, use_container_width=True)

##




# Gender_df = pd.DataFrame.from_dict(get_genero())
# graphs(Gender_df, "GENERO")
# print("--------Doneee1-----")

# def get_genero():
#     API="/general_statistics/"
#     QUERY_PARAMS="?fields=ANO&fields=ESTADO&fields=GENERO"
#     response = requests.get(BASE_URL+API+QUERY_PARAMS).json()
#     if response:
#         return response
#     else:
#         return "Error"