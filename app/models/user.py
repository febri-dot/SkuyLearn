class User:
   def __init__(self, username, password, role):
      self.__username = username  
      self.__password = password
      self.role = role

   @property
   def username(self):
      return self.__username

   def get_dashboard_info(self):
      return f"Selamat datang, {self.__username}!"