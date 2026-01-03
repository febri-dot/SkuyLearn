from app.models.user import User

class Dosen(User):
   def __init__(self, username, password, nidn, name):
      super().__init__(username, password, role="dosen")
      self.nidn = nidn
      self.name = name

   def get_dashboard_info(self):
      return f"Dashboard Dosen: {self.name} (NIDN: {self.nidn})"
   
   def get_course_frame(self):
      return "LecturerCourseFrame"