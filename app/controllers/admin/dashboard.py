from app.connection import Database

class DashboardController:
   @staticmethod
   def get_stats():
      """Fetch statistics data from the database."""
      db = Database()
      
      mhs_result = db.fetch_one("SELECT COUNT(*) FROM mahasiswa")
      dsn_result = db.fetch_one("SELECT COUNT(*) FROM dosen")
      crs_result = db.fetch_one("SELECT COUNT(*) FROM courses")

      return {
         "total_students": mhs_result[0] if mhs_result else 0,
         "total_lecturers": dsn_result[0] if dsn_result else 0,
         "total_courses": crs_result[0] if crs_result else 0
      }