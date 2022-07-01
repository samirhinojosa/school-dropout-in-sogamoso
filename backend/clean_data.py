import os
import pandas as pd

# df_students = pd.read_csv(os.path.join(os.path.dirname(__file__), "df_students.csv"))
# print(df_students.dtypes)

from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@ds4a-112-db.c9ft450u5oen.us-east-2.rds.amazonaws.com/dropout')
# df_students.to_sql('students_table', engine, if_exists='replace')
result = engine.execute('SELECT * FROM students_table limit 5;')
# print(result)
for row in result:
    print(row)