import os
import pandas as pd
from sqlalchemy import create_engine

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
# print(df_students.dtypes)

df_students['AÑO'] = df_students['ANO']
df_students['PER_ID_AÑO'] = df_students['PER_ID_ANO']

## Add data to the db

engine = create_engine('postgresql://postgres:postgres@ds4a-112-db.c9ft450u5oen.us-east-2.rds.amazonaws.com/dropout')
df_students.to_sql('students_table', engine, if_exists='replace')
# result = engine.execute('SELECT * FROM students_table limit 5;')
# print(result)
# for row in result:
#     print(row)