import pandas as pd
import sqlite3

try:
    df = pd.read_csv('player_data.csv')
    with sqlite3.connect('data.db') as conn:
        print(f'opened sqlite db {sqlite3.sqlite_version}')
        df.to_sql()
except sqlite3.OperationalError as e:
    print("failed to open db", e)
