
import sqlite3

try:
    conn = sqlite3.connect('skuylearn.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    for table in tables:
        t_name = table[0]
        cursor.execute(f"PRAGMA table_info({t_name})")
        columns = cursor.fetchall()
        print(f"\nTable: {t_name}")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
            
    conn.close()
except Exception as e:
    print(e)
