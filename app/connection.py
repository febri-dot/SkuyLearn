import sqlite3
import os

def get_connection():
   """Establish a connection to the SQLite database."""
   try:
      conn = sqlite3.connect('skuylearn.db')
      conn.execute("PRAGMA foreign_keys = ON;")
      return conn
   except sqlite3.Error as e:
      print(f"Database Connection Error: {e}")
      return None

def init_db():
   """Execute queries to create all tables if they do not exist."""
   query = """
   -- 1. Table: users
   CREATE TABLE IF NOT EXISTS users (
      username VARCHAR PRIMARY KEY,
      password VARCHAR NOT NULL,
      role VARCHAR NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- 2. Table: mahasiswa
   CREATE TABLE IF NOT EXISTS mahasiswa (
      npm INTEGER PRIMARY KEY,
      name VARCHAR NOT NULL,
      birthday DATE,
      gender VARCHAR,
      address VARCHAR,
      phone_number VARCHAR,
      FOREIGN KEY (npm) REFERENCES users (username) ON DELETE CASCADE
   );

   -- 3. Table: dosen
   CREATE TABLE IF NOT EXISTS dosen (
      nidn INTEGER PRIMARY KEY,
      name VARCHAR NOT NULL,
      birthday DATE,
      gender VARCHAR,
      address VARCHAR,
      phone_number VARCHAR,
      FOREIGN KEY (nidn) REFERENCES users (username) ON DELETE CASCADE
   );

   -- 4. Table: courses
   CREATE TABLE IF NOT EXISTS courses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      course_name VARCHAR NOT NULL,
      description TEXT,
      enrollment_key VARCHAR,
      owner INTEGER,
      FOREIGN KEY (owner) REFERENCES dosen (nidn) ON DELETE SET NULL
   );

   -- 5. Table: enrollment_class
   CREATE TABLE IF NOT EXISTS enrollment_class (
      course_id INTEGER,
      npm INTEGER,
      joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (course_id, npm),
      FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
      FOREIGN KEY (npm) REFERENCES mahasiswa (npm) ON DELETE CASCADE
   );

   -- 6. Table: course_materials
   CREATE TABLE IF NOT EXISTS course_materials (
      course_id INTEGER,
      uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      title VARCHAR NOT NULL,
      content VARCHAR,
      content_path VARCHAR,
      PRIMARY KEY (course_id, uploaded_at),
      FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
   );

   -- 7. Table: assignments
   CREATE TABLE IF NOT EXISTS assignments (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      course_id INTEGER,
      title VARCHAR NOT NULL,
      description TEXT,
      assignment_path VARCHAR,
      due_date DATETIME,
      FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE
   );

   -- 8. Table: submissions
   CREATE TABLE IF NOT EXISTS submissions (
      assignment_id INTEGER,
      npm INTEGER,
      assignment_path VARCHAR,
      grade INTEGER DEFAULT NULL,
      submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (assignment_id, npm),
      FOREIGN KEY (assignment_id) REFERENCES assignments (id) ON DELETE CASCADE,
      FOREIGN KEY (npm) REFERENCES mahasiswa (npm) ON DELETE CASCADE
   );
   """
   
   conn = get_connection()
   if conn:
      try:
         conn.executescript(query)
         conn.commit()
         print("Database & Tables initialized successfully.")
      except sqlite3.Error as e:
         print(f"Failed to create tables: {e}")
      finally:
         conn.close()

def initlize_dummy():
   """Initialize dummy data ONLY if the users table is empty."""
   conn = get_connection()
   if not conn:
      return

   try:
      cursor = conn.cursor()
      
      cursor.execute("SELECT COUNT(*) FROM users")
      count = cursor.fetchone()[0]

      if count == 0:
         print("Database is empty. Inserting dummy data...")

         users_dummy = [
               ('admin01', '123', 'admin'),
               ('2021001', '123', 'mahasiswa'),
               ('990011', '123', 'dosen')
         ]
         cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users_dummy)

         cursor.execute("""
               INSERT INTO mahasiswa (npm, name, birthday, gender, address, phone_number)
               VALUES (2021001, 'Andi Wijaya', '2003-05-15', 'Male', 'Jakarta St. No. 5', '08123456789')
         """)

         cursor.execute("""
               INSERT INTO dosen (nidn, name, birthday, gender, address, phone_number)
               VALUES (990011, 'Dr. Budi Santoso, M.Kom', '1985-10-20', 'Male', 'Bandung No. 10', '08987654321')
         """)

         conn.commit()
         print("Dummy data successfully initialized.")
      else:
         print("Database already has data. Skipping dummy initialization.")

   except sqlite3.Error as e:
      print(f"Error during dummy initialization: {e}")
   finally:
      conn.close()