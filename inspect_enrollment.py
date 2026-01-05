
import sqlite3

try:
    conn = sqlite3.connect('skuylearn.db')
    cursor = conn.cursor()
    
    t_name = 'enrollment_class'
    cursor.execute(f"PRAGMA table_info({t_name})")
    columns = cursor.fetchall()
    print(f"\nTable: {t_name}")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
            
    conn.close()
except Exception as e:
    print(e)
