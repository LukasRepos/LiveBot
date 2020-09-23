import sqlite3 as sqlite

import pandas as pd

conn = sqlite.connect("test.db")
cursor = conn.cursor()

df = pd.read_csv("dummyData.csv", index_col="Serial Number")

df.to_sql('COMPANIES1', conn, if_exists='replace', index=False)
df.iloc[:50].to_sql('COMPANIES2', conn, if_exists='replace', index=True)

cursor.execute("SELECT * FROM COMPANIES1")
print(cursor.fetchall())

cursor.execute("SELECT * FROM COMPANIES2")
print(cursor.fetchall())

table = pd.read_sql_query("SELECT * from COMPANIES2", conn, index_col=None)
print(table.head())

conn.close()
