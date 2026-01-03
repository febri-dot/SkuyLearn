import sqlite3
import os
from tkinter import messagebox

class Database:
   def __init__(self, db_name='skuylearn.db'):
      self.db_name = db_name

   def get_connection(self):
      """Membuka koneksi ke database."""
      try:
         conn = sqlite3.connect(self.db_name)
         conn.execute("PRAGMA foreign_keys = ON;")
         return conn
      except sqlite3.Error as e:
         print(f"Database Connection Error: {e}")
         return None

   # --- FUNGSI HELPER UNTUK CONTROLLER ---
   def fetch_one(self, query, params=()):
      conn = self.get_connection()
      if conn:
         try:
               cursor = conn.cursor()
               cursor.execute(query, params)
               return cursor.fetchone()
         finally:
               conn.close()
      return None

   def fetch_all(self, query, params=()):
      """Fetch all rows (Perfect for tables and lists)."""
      conn = self.get_connection()
      if conn:
         try:
               cursor = conn.cursor()
               cursor.execute(query, params)
               return cursor.fetchall() 
         except sqlite3.Error as e:
               print(f"Fetch All Error: {e}")
               return []
         finally:
               conn.close()
      return []

   def execute_query(self, query, params=()):
      conn = self.get_connection()
      if conn:
         try:
               cursor = conn.cursor()
               cursor.execute(query, params)
               conn.commit()
               return True
         finally:
               conn.close()
      return False

   # --- LOGIKA INISIALISASI ---
   def init_db(self):
      """Membuat semua tabel jika belum ada."""
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
      conn = self.get_connection()
      if conn:
         try:
               conn.executescript(query)
               conn.commit()
               print("Database & Tables initialized.")
               self.initialize_dummy()
         finally:
               conn.close()

   def initialize_dummy(self):
      """Isi data dummy jika tabel users kosong."""
      conn = self.get_connection()
      if not conn: return
      try:
         cursor = conn.cursor()
         cursor.execute("SELECT COUNT(*) FROM users")
         if cursor.fetchone()[0] == 0:
               print("Inserting dummy data...")
               conn.commit()
      finally:
         conn.close()