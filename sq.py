import random

import pandas as pd
import sqlite3 as sqlite

conn = sqlite.connect("test.db")
cursor = conn.cursor()

df = pd.read_csv("dummyData.csv")

df.to_sql('COMPANIES1', conn, if_exists='replace', index=False)
df.iloc[:50].to_sql('COMPANIES2', conn, if_exists='replace', index=False)

cursor.execute("SELECT * FROM COMPANIES1")
print(len(cursor.fetchall()))

cursor.execute("SELECT * FROM COMPANIES2")
print(len(cursor.fetchall()))

conn.close()
