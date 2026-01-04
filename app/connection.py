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
      if not conn:
         return

      try:
         cursor = conn.cursor()

         # Cek apakah sudah ada data
         cursor.execute("SELECT COUNT(*) FROM users")
         if cursor.fetchone()[0] > 0:
               print("Dummy data already exists.")
               return

         print("Inserting dummy data...")

         # ================= USERS =================
         users = [
               ("180001", "123", "mahasiswa"),
               ("180002", "123", "mahasiswa"),
               ("9001", "123", "dosen"),
               ("9002", "123", "dosen"),
               ("admin", "admin", "admin")
         ]

         cursor.executemany(
               "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
               users
         )

         # ================= MAHASISWA =================
         mahasiswa = [
               (180001, "Andi Pratama", "2003-01-10", "L", "Jakarta", "081234567890"),
               (180002, "Siti Aisyah", "2003-05-21", "P", "Bandung", "082345678901")
         ]

         cursor.executemany(
               """INSERT INTO mahasiswa 
                  (npm, name, birthday, gender, address, phone_number)
                  VALUES (?, ?, ?, ?, ?, ?)""",
               mahasiswa
         )

         # ================= DOSEN =================
         dosen = [
               (9001, "Dr. Budi Santoso", "1980-02-14", "L", "Depok", "0811111111"),
               (9002, "Dr. Rina Lestari", "1985-07-09", "P", "Bogor", "0822222222")
         ]

         cursor.executemany(
               """INSERT INTO dosen
                  (nidn, name, birthday, gender, address, phone_number)
                  VALUES (?, ?, ?, ?, ?, ?)""",
               dosen
         )

         # ================= COURSES =================
         courses = [
               ("Pemrograman Python", "Belajar Python Dasar", "PY123", 9001),
               ("Basis Data", "Konsep Database Relasional", "DB123", 9002)
         ]

         cursor.executemany(
               """INSERT INTO courses 
                  (course_name, description, enrollment_key, owner)
                  VALUES (?, ?, ?, ?)""",
               courses
         )

         # ================= ENROLLMENT =================
         enrollment = [
               (1, 180001),
               (1, 180002),
               (2, 180001)
         ]

         cursor.executemany(
               """INSERT INTO enrollment_class (course_id, npm)
                  VALUES (?, ?)""",
               enrollment
         )

         # ================= COURSE MATERIALS =================
         materials = [
               (1, "Pengenalan Python", "Materi dasar Python", None),
               (2, "Normalisasi Database", "Materi normalisasi", None)
         ]

         cursor.executemany(
               """INSERT INTO course_materials
                  (course_id, title, content, content_path)
                  VALUES (?, ?, ?, ?)""",
               materials
         )

         # ================= ASSIGNMENTS =================
         assignments = [
               (1, "Tugas 1 Python", "Buat program kalkulator", None, "2026-02-01"),
               (2, "Tugas 1 Basis Data", "ERD Sistem Akademik", None, "2026-02-05")
         ]

         cursor.executemany(
               """INSERT INTO assignments
                  (course_id, title, description, assignment_path, due_date)
                  VALUES (?, ?, ?, ?, ?)""",
               assignments
         )

         conn.commit()
         print("Dummy data inserted successfully.")

      except sqlite3.Error as e:
         print("Error inserting dummy data:", e)
         conn.rollback()
      finally:
         conn.close()
