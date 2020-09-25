import Chatty.fileSystem.filesystems as fss
import sqlite3 as sqlite
import pandas as pd


class Connection:
    def __init__(self) -> None:
        self.conn = sqlite.connect(fss.access_fs("database").root)

    def get_connection(self) -> sqlite.Connection:
        return self.conn

    def save_df(self, table_name: str, df: pd.DataFrame, if_exists="replace", index=False) -> None:
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=index)

    def to_df(self, table_name: str, index: str = None):
        return pd.read_sql_query(f"SELECT * from {table_name}", self.conn, index_col=index)

    def execute_query(self, query: str) -> list:
        cursor = self.conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def shutdown(self) -> None:
        self.conn.close()
