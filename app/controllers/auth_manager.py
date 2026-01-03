from app.connection import get_connection
from app.models.mahasiswa import Mahasiswa
from app.models.dosen import Dosen
from app.models.user import User 

class AuthManager:
   @staticmethod
   def authenticate(username, password):
      """Verify credentials and return the specific User object."""
      conn = get_connection()
      if not conn:
         return None
      
      try:
         cursor = conn.cursor()
         cursor.execute(
               "SELECT username, password, role FROM users WHERE username = ? AND password = ?", 
               (username, password)
         )
         result = cursor.fetchone()
         
         if result:
               un, pw, role = result
               if role == 'mahasiswa':
                  return Mahasiswa(un, pw, npm=un, name="Student User")
               elif role == 'dosen':
                  return Dosen(un, pw, nidn=un, name="Lecturer User")
               else:
                  return User(un, pw, role) 
         return None
      finally:
         conn.close()