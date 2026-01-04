from app.models.user import User

class Mahasiswa(User):
   def __init__(self, username, password, npm, name):
      super().__init__(username, password, role="mahasiswa")
      self.npm = npm
      self.name = name

   def get_dashboard_info(self):
      return f"Dashboard Mahasiswa: {self.name} (NPM: {self.npm})"
   
   def get_course_frame(self):
      return "MyCourseFrame"