import os
import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:postgres@ds4a-112-db.c9ft450u5oen.us-east-2.rds.amazonaws.com/dropout')
df_students_2022_predicted = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_students_2022_predicted.csv"))

df_students_2022_predicted['ANO'] = df_students_2022_predicted['AÑO']
df_students_2022_predicted['PER_ID_ANO'] = df_students_2022_predicted['PER_ID_AÑO']
df_students_2022_predicted['CATEGORICAL_EDAD'] = df_students_2022_predicted['EDAD_CLASIFICACION']

df_students_2022_predicted.to_sql('prediction_2022_students_table', engine, if_exists='replace')


### Validate information
# df_students_nl = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_students_nl.csv"))
# print("-------df_students_nl--------")
# # print(df_students_nl.columns)
# print(df_students_nl['ANO'])
# df_students_sm = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_students_sm.csv"))
# print("-------df_students_sm--------")
# print(df_students_sm.columns)
# print(df_students_sm['AÑO'])

df_students = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_students.csv"))

# Arreglo de variables:

#Variable DISCAPACIDAD: pasar de categórica a dicotómica
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

df_students['CATEGORICAL_EDAD'] = df_students['EDAD'].apply(age_clasification)
# print(df_students['CATEGORICAL_EDAD'].unique())
# print(df_students['CATEGORICAL_EDAD'].value_counts())
# df_students['CATEGORICAL_EDAD']
# print(df_students.dtypes)

df_students['AÑO'] = df_students['ANO']
df_students['PER_ID_AÑO'] = df_students['PER_ID_ANO']

## Add data to the db


# df_students.to_sql('students_table', engine, if_exists='replace')
# result = engine.execute('SELECT * FROM students_table limit 5;')
# print(result)
# for row in result:
#     print(row)
