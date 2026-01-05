# app/controllers/course_detail_controller.py
from app.connection import Database

class CourseDetailController:
   @staticmethod
   def get_course_contents(course_id):
      db = Database()
      # Fetching materials and assignments as a single timeline
      query = """
         SELECT 'materi' as type, course_id as id, title, content as description, 
                  uploaded_at as created_at, content_path as file_path
         FROM course_materials WHERE course_id = ?
         UNION ALL
         SELECT 'tugas' as type, id, title, description, 
                  due_date as created_at, assignment_path as file_path
         FROM assignments WHERE course_id = ?
         ORDER BY created_at DESC
      """
      return db.fetch_all(query, (course_id, course_id))

   @staticmethod
   def delete_materi(course_id, title):
      db = Database()
      try:
         db.execute_query("DELETE FROM course_materials WHERE course_id = ? AND title = ?", (course_id, title))
         return True
      except Exception as e:
         print(f"Error deleting material: {e}")
         return False

   @staticmethod
   def delete_assignment(assignment_id):
      db = Database()
      try:
         db.execute_query("DELETE FROM assignments WHERE id = ?", (assignment_id,))
         return True
      except Exception as e:
         print(f"Error deleting assignment: {e}")
         return False