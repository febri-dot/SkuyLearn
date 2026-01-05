class User:
   def __init__(self, username, password, role):
      self.__username = username  
      self.__password = password
      self.role = role

   @property
   def username(self):
      return self.__username
   
   @username.setter
   def username(self, value):
      self._username = value

   def get_dashboard_info(self):
      return f"Selamat datang, {self.__username}!"
   
   def get_dashboard_frame(self):
        if self.role == "mahasiswa":
            return "DashboardMahasiswa"
        elif self.role == "dosen":
            return "DashboardDosen"
        elif self.role == "admin":
            return "DashboardFrame"
        else:
            return "HomeFrame"

   def get_course_frame(self):
      return "MahasiswaMyCourseFrame"
   
   def get_course_detail_frame(self):
      return "CourseDetailFrame"