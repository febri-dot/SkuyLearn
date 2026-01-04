import tkinter as tk
from tkinter import messagebox
from app.controllers.auth_manager import AuthManager

class RegisterWindow(tk.Toplevel): 
   def __init__(self, parent, target_role="MAHASISWA"):
      super().__init__(parent)
      self.target_role = target_role.upper()
      self.title(f"Add New {self.target_role.capitalize()}")
      
      # Setup Window agar di tengah screen
      self.geometry("400x550")
      self.configure(bg="#f0f2f5")
      self.resizable(False, False)

      # UI Card
      self.card = tk.Frame(self, bg="white", padx=30, pady=30, 
                           highlightbackground="#d1d1d1", highlightthickness=1)
      self.card.pack(expand=True, padx=20, pady=20)

      # Header dinamis berdasarkan Role
      tk.Label(self.card, text=f"ADD {self.target_role}", bg="white", fg="#2c3e50", 
               font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

      # --- Input Fields ---
      # Username/ID (NPM/NIDN)
      tk.Label(self.card, text="Username", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
      self.username_entry = tk.Entry(self.card, font=("Arial", 11), width=30, bg="#f8f9fa", relief="flat")
      self.username_entry.pack(pady=(5, 15), ipady=8)

      # Password
      tk.Label(self.card, text="Password", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
      self.password_entry = tk.Entry(self.card, font=("Arial", 11), width=30, bg="#f8f9fa", relief="flat", show="•")
      self.password_entry.pack(pady=(5, 15), ipady=8)

      # Role (Hidden/Locked)
      tk.Label(self.card, text="Role", bg="white", font=("Arial", 9, "bold")).pack(anchor="w")
      self.role_label = tk.Label(self.card, text=self.target_role, bg="#e9ecef", fg="#495057", 
                                 font=("Arial", 10, "bold"), width=28, pady=10)
      self.role_label.pack(pady=(5, 25))

      # Submit Button
      self.btn_save = tk.Button(self.card, text="SAVE DATA", bg="#3498db", fg="white", 
                                 font=("Arial", 11, "bold"), width=25, height=2,
                                 relief="flat", cursor="hand2", command=self.handle_save)
      self.btn_save.pack()

   def handle_save(self):
      username = self.username_entry.get()
      password = self.password_entry.get()
      role = self.target_role.lower()

      if not username or not password:
         messagebox.showwarning("Warning", "Please fill all fields!")
         return

      # Logika Validasi & Simpan (Reuse AuthManager)
      academic_check = AuthManager.check_academic_identity(username, role)
      
      if academic_check["status"]:
         # 2. Eksekusi Register
         result = AuthManager.register_user(username, password, role)
         if result["status"]:
               messagebox.showinfo("Success", f"{self.target_role} registered successfully!")
               self.master.refresh()
               self.destroy() # Tutup pop-up
         else:
               messagebox.showerror("Error", result["message"])
      else:
         messagebox.showerror("Failed", academic_check["message"])