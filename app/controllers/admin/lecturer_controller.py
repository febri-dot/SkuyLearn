from app.connection import Database

class LecturerController:
   @staticmethod
   def get_all_lecturers():
      """Fetch all lecturer records joined with their password for the table."""
      db = Database()
      # Mengambil data profil + password dari tabel users
      query = """
         SELECT d.nidn, d.name, d.birthday, d.gender, d.address, d.phone_number, u.password
         FROM dosen d 
         JOIN users u ON d.nidn = u.username
      """
      return db.fetch_all(query)