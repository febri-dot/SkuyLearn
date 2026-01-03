import tkinter as tk

class DashboardFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent)
      self.controller = controller
      
      tk.Label(self, text="MAIN DASHBOARD", font=("Arial", 18)).pack(pady=20)
      
      tk.Button(self, text="Master Mahasiswa").pack(fill="x", padx=50, pady=2)
      tk.Button(self, text="Master Dosen").pack(fill="x", padx=50, pady=2)
      
      tk.Button(self, text="Logout", bg="red", fg="white", 
               command=lambda: controller.show_frame("LoginFrame")).pack(pady=20)