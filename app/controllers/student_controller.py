from app.connection import Database

class StudentController:
   @staticmethod
   def get_all_students():
      """Fetch all student records for the table."""
      db = Database()
      query = """
         SELECT m.*, u.password
         FROM mahasiswa m 
         JOIN users u ON m.npm = u.username
      """
      return db.fetch_all(query)

   @staticmethod
   def delete_student(npm):
      """Delete a student and their user account."""
      db = Database()
      return db.execute_query("DELETE FROM users WHERE username = ?", (npm,))