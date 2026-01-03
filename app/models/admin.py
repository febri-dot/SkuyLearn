from app.models.user import User

class Admin(User):
   def __init__(self, username, password):
      super().__init__(username, password, role="admin")

   def get_dashboard_info(self):
      return f"System Administrator: {self.username} (All Access Granted)"
   
   def get_course_frame(self):
      return "AdminCourseFrame"