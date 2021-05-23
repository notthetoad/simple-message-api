import sqlite3

def create_connection():
  conn = None
  try:
    conn = sqlite3.connect('../main.db')
  except Error as e:
    print(e)
  finally:
    if conn:
      conn.close()