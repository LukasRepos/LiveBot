import pandas as pd
import sqlite3 as sqlite

conn = sqlite.connect("/home/luiscarlos/PycharmProjects/LiveBot/sandbox/configuration/memory.db")

cursor = conn.cursor()
cursor.execute("SELECT * FROM RESERVED_RAW_INTENTS")
original_intent_list = cursor.fetchall()

original_intents = {}
for c, p in original_intent_list:
    if c in original_intents:
        original_intents[c].append(p)
    else:
        original_intents[c] = [p]

modified_df = pd.read_sql_query(f"SELECT * from RESERVED_TFIDF", conn)[["__documents", "__class"]]
modified_intents = {}
for c, p in zip(modified_df["__class"], modified_df["__documents"]):
    if c in modified_intents:
        modified_intents[c].append(p)
    else:
        modified_intents[c] = [p]

diff = {}
for km, vm in modified_intents.items():
    if km not in original_intents:
        diff[km] = vm
    elif vm != original_intents[km]:
        diff[km] = list(set(vm) - set(original_intents[km]))

cursor.execute("SELECT * FROM RESERVED_RAW_RESPONSES")
raw_response_list = cursor.fetchall()
raw_responses = {k: v for k, v in raw_response_list}

print(diff.keys())
print(raw_responses.keys())

print(raw_responses)

cursor.close()
conn.close()
