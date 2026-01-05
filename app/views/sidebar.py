import tkinter as tk

class SidebarFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#2c3e50", width=200)
      self.controller = controller
      self.pack_propagate(False) 
      
   def refresh(self):
      """Hapus dan gambar ulang tombol sesuai style yang diinginkan"""
      for widget in self.winfo_children():
         widget.destroy()

      tk.Label(self, text="SKUYLEARN", fg="white", bg="#2c3e50", 
               font=("Helvetica", 16, "bold")).pack(pady=20)

      btn_style = {
         "bg": "#34495e", 
         "fg": "white", 
         "relief": "flat", 
         "padx": 10, 
         "pady": 10,
         "font": ("Arial", 10, "bold"),
         "cursor": "hand2",
         "activebackground": "#2c3e50",
         "activeforeground": "white"
      }

      # 1. Tombol Home (Semua Role)
      tk.Button(self, text="Home", **btn_style,
               command=lambda: self.controller.show_frame("HomeFrame")).pack(fill="x", pady=1)
      
      user = self.controller.current_user
      if user:
         role = user.role.lower() # Ambil role user
         dashboard_frame = user.get_dashboard_frame()
         target_frame = user.get_course_frame()
         
         # 2. Tombol Dashboard (Semua Role)
         tk.Button(self, text="Dashboard", **btn_style,
                  command=lambda f=dashboard_frame: self.controller.show_frame(f)).pack(fill="x", pady=1)
         
         # 3. Tombol My Course (HANYA jika BUKAN admin)
         if role != "admin":
            tk.Button(self, text="My Course", **btn_style,
                     command=lambda: self.controller.show_frame(target_frame)).pack(fill="x", pady=1)

      # 4. Tombol Profile (Semua Role)
      tk.Button(self, text="Profile", **btn_style,
               command=lambda: self.controller.show_frame("ProfileFrame")).pack(fill="x", pady=1)
      
      # 5. Tombol Logout
      tk.Button(self, text="Logout", bg="#e74c3c", fg="white", relief="flat",
               font=("Arial", 10, "bold"), cursor="hand2",
               command=self.controller.handle_logout).pack(side="bottom", fill="x", pady=20)