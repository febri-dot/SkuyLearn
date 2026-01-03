import tkinter as tk
from app.views.login_ui import LoginFrame
from app.views.dashboard_ui import DashboardFrame

class SkuylearnApp(tk.Tk):
   def __init__(self):
      super().__init__()
      self.title("SKUYLEARN - Academic System")
      self.geometry("1100x700")
      self.current_user = None

      self.main_container = tk.Frame(self)
      self.main_container.pack(side="top", fill="both", expand=True)

      self.sidebar = tk.Frame(self.main_container, bg="#2c3e50", width=200)
      self.sidebar.pack_propagate(False) 

      self.content_area = tk.Frame(self.main_container, bg="white")
      self.content_area.pack(side="right", fill="both", expand=True)

      self.frames = {}
      frames = [
         LoginFrame, 
         DashboardFrame
      ]
      for F in frames:
         page_name = F.__name__
         frame = F(parent=self.content_area, controller=self)
         self.frames[page_name] = frame
         frame.grid(row=0, column=0, sticky="nsew")

      self.content_area.grid_rowconfigure(0, weight=1)
      self.content_area.grid_columnconfigure(0, weight=1)

      self.show_frame("LoginFrame")

   def show_frame(self, page_name):
      if page_name == "LoginFrame":
         self.sidebar.pack_forget()
      else:
         self.sidebar.pack(side="left", fill="y")
         self.update_sidebar() 

      frame = self.frames[page_name]
      frame.tkraise()

   def update_sidebar(self):
      """Dynamically create sidebar buttons based on user role"""
      for widget in self.sidebar.winfo_children():
         widget.destroy()

      tk.Label(self.sidebar, text="SKUYLEARN", fg="white", bg="#2c3e50", 
               font=("Helvetica", 16, "bold")).pack(pady=20)

      btn_style = {
         "bg": "#34495e", 
         "fg": "white", 
         "relief": "flat", 
         "padx": 10, 
         "pady": 10,
         "font": ("Arial", 10, "bold"),
         "cursor": "hand2"
      }
      
      tk.Button(self.sidebar, text="Dashboard", **btn_style,
               command=lambda: self.show_frame("DashboardFrame")).pack(fill="x", pady=1)
      
      tk.Button(self.sidebar, text="Student Data", **btn_style).pack(fill="x", pady=1)
      tk.Button(self.sidebar, text="Course Materials", **btn_style).pack(fill="x", pady=1)

      # Logout at bottom
      tk.Button(self.sidebar, text="Logout", bg="#e74c3c", fg="white", relief="flat",
               command=lambda: self.show_frame("LoginFrame")).pack(side="bottom", fill="x", pady=20)