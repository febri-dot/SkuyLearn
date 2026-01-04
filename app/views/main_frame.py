import tkinter as tk
from app.views.login_ui import LoginFrame
from app.views.admin.dashboard_ui import DashboardFrame
from app.views.dosen.dashboard_ui import DashboardDosen
from app.views.mahasiswa.dashboard_ui import DashboardMahasiswa
from app.views.admin.student_data_ui import StudentDataFrame
from app.views.mahasiswa_mycourse_ui import MahasiswaMyCourseFrame
from app.views.sidebar import SidebarFrame
from app.views.profile_ui import ProfileFrame

class SkuylearnApp(tk.Tk):
   def __init__(self):
      super().__init__()
      self.current_user = None

      self.title("SKUYLEARN - Academic System")
      self.geometry("1100x700")
      self.current_user = None

      self.main_container = tk.Frame(self)
      self.main_container.pack(side="top", fill="both", expand=True)

      self.sidebar = SidebarFrame(parent=self.main_container, controller=self)
      self.sidebar.pack_propagate(False) 
      self.sidebar.pack(side="left", fill="both", expand=True)

      self.content_area = tk.Frame(self.main_container, bg="white")
      self.content_area.pack(side="right", fill="both", expand=True)

      self.frames = {}
      pages = [
         {"class": LoginFrame, "access": "any"},
         {"class": ProfileFrame, "access": "any"},
         {"class": DashboardFrame, "access": "admin"},
         {"class": StudentDataFrame, "access": "admin"},
         {"class": DashboardDosen, "access": "dosen"},
         {"class": DashboardMahasiswa, "access": "mahasiswa"},
         {"class": MahasiswaMyCourseFrame, "access": "any", "alias": "CoursesListFrame"}
      ]
         
      for page in pages:
         page_name = page["class"].__name__
         frame = page["class"](parent=self.content_area, controller=self)
         frame.access_level = page["access"] 
         self.frames[page_name] = frame
         frame.grid(row=0, column=0, sticky="nsew")

      self.content_area.grid_rowconfigure(0, weight=1)
      self.content_area.grid_columnconfigure(0, weight=1)

      self.show_frame("LoginFrame")

   def show_frame(self, page_name):
      frame = self.frames[page_name]
      
      if page_name == "LoginFrame":
         self.sidebar.pack_forget()
      else:
         self.sidebar.pack(side="left", fill="y")
         self.sidebar.refresh()

      if hasattr(frame, "refresh"):
         frame.refresh()
         
      frame.tkraise()
   def handle_logout(self):
      from tkinter import messagebox
      if messagebox.askyesno("Logout", "Are you sure?"):
         self.current_user = None
         self.show_frame("LoginFrame")