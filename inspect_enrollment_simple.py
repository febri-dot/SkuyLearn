
import sqlite3

try:
    conn = sqlite3.connect('skuylearn.db')
    cursor = conn.cursor()
    
    t_name = 'enrollment_class'
    cursor.execute(f"PRAGMA table_info({t_name})")
    columns = cursor.fetchall()
    print([col[1] for col in columns])
            
    conn.close()
except Exception as e:
    print(e)
