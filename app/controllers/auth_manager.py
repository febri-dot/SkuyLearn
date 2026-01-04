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
   def register_new_user(data, role):
      db = Database()
      
      role_lower = role.lower()
      target_table = "mahasiswa" if role_lower == "mahasiswa" else "dosen"
      id_col = "npm" if role_lower == "mahasiswa" else "nidn"

      # --- STEP 1: Insert into USERS table FIRST ---
      # This satisfies the Foreign Key requirement
      query_user = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)"
      params_user = (data['id_num'], data['id_num'], role_lower)

      # --- STEP 2: Insert into PROFILE table SECOND ---
      query_profile = f"""
         INSERT INTO {target_table} ({id_col}, name, birthday, gender, address, phone_number)
         VALUES (?, ?, ?, ?, ?, ?)
      """
      params_profile = (
         data['id_num'], 
         data['name'], 
         data['birthday'], 
         data['gender'], 
         data['address'], 
         data['phone']
      )

      try:
         # Execute User first
         db.execute_query(query_user, params_user)
         # Then execute Profile
         db.execute_query(query_profile, params_profile)
         
         return True, f"Registration successful! Account created with ID: {data['id_num']}"
      
      except Exception as e:
         print(f"Registration Error: {e}")
         return False, f"Database Error: {str(e)}"
   
   def generate_next_id(role):
      db = Database()
      table = "mahasiswa" if role == "MAHASISWA" else "dosen"
      column = "npm" if role == "MAHASISWA" else "nidn"
      
      query = f"SELECT {column} FROM {table} ORDER BY {column} DESC LIMIT 1"
      result = db.fetch_one(query)
      
      if result and result[0]:
         last_id = int(result[0])
         return str(last_id + 1)
      else:
         return "220001" if role == "MAHASISWA" else "110001"
      
   @staticmethod
   def update_user_data(data, role):
      db = Database()
      
      role_lower = role.lower()
      target_table = "mahasiswa" if role_lower == "mahasiswa" else "dosen"
      id_col = "npm" if role_lower == "mahasiswa" else "nidn"

      # 1. Update Profile
      query_profile = f"""
         UPDATE {target_table} 
         SET name=?, birthday=?, gender=?, address=?, phone_number=?
         WHERE {id_col}=?
      """
      params_profile = (data['name'], data['birthday'], data['gender'], 
                        data['address'], data['phone'], data['id_num'])

      # 2. Update Password di tabel users
      query_user = "UPDATE users SET password=? WHERE username=?"
      params_user = (data['password'], data['id_num'])

      try:
         db.execute_query(query_profile, params_profile)
         db.execute_query(query_user, params_user)
         return True, "User data and password updated successfully!"
      except Exception as e:
         return False, f"Update Failed: {str(e)}"
   
   @staticmethod
   def delete_user(user_id, role):
      db = Database()
      
      role_lower = role.lower()
      target_table = "mahasiswa" if role_lower == "mahasiswa" else "dosen"
      id_col = "npm" if role_lower == "mahasiswa" else "nidn"

      # SQL Queries
      query_profile = f"DELETE FROM {target_table} WHERE {id_col} = ?"
      query_user = "DELETE FROM users WHERE username = ?"

      try:
         db.execute_query(query_profile, (user_id,))
         db.execute_query(query_user, (user_id,))
         
         return True, "User deleted successfully."
      except Exception as e:
         return False, f"Delete Failed: {str(e)}"