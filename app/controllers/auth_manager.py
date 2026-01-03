from app.connection import Database
from app.models.mahasiswa import Mahasiswa
from app.models.dosen import Dosen
from app.models.user import User 

class AuthManager:
   @staticmethod
   def authenticate(username, password):
      """Verify credentials and return the specific User object."""
      db = Database()
      result = db.fetch_one(
         "SELECT username, password, role FROM users WHERE username = ? AND password = ?", 
         (username, password)
      )
      
      if result:
         un, pw, role = result
         name_data = AuthManager.get_display_name(un, role)
         
         if role == 'mahasiswa':
               return Mahasiswa(un, pw, npm=un, name=name_data)
         elif role == 'dosen':
               return Dosen(un, pw, nidn=un, name=name_data)
         else:
               return User(un, pw, role) 
      return None

   @staticmethod
   def get_display_name(username, role):
      """Helper to fetch the real name from academic tables."""
      db = Database()
      if role == "mahasiswa":
         res = db.fetch_one("SELECT name FROM mahasiswa WHERE npm = ?", (username,))
      elif role == "dosen":
         res = db.fetch_one("SELECT name FROM dosen WHERE nidn = ?", (username,))
      else:
         return "Administrator"
      return res[0] if res else "User"

   @staticmethod
   def check_academic_identity(username, role):
      """Verify if the ID exists in academic records before allowing registration."""
      db = Database()
      query = ""
      if role == "mahasiswa":
         query = "SELECT name FROM mahasiswa WHERE npm = ?"
      elif role == "dosen":
         query = "SELECT name FROM dosen WHERE nidn = ?"
      
      if not query:
         return {"status": False, "message": "Invalid role selected."}

      result = db.fetch_one(query, (username,))
      
      if result:
         return {
               "status": True, 
               "message": f"Hello {result[0]}! Identity verified. You may proceed with registration."
         }
      return {
         "status": False, 
         "message": "Academic record not found. Please ensure your ID is correct."
      }

   @staticmethod
   def register_user(username, password, role):
      """Create a new user account."""
      db = Database()
      
      # 1. Check if the username is already taken
      check = db.fetch_one("SELECT username FROM users WHERE username = ?", (username,))
      if check:
         return {"status": False, "message": "This ID/Username is already registered."}

      # 2. Insert into the database
      success = db.execute_query(
         "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
         (username, password, role)
      )
      
      if success:
         return {"status": True, "message": "Registration successful! Please login."}
      
      return {"status": False, "message": "Database error: Failed to save user data."}