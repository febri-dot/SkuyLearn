import tkinter as tk
from tkinter import messagebox
from app.controllers.auth_manager import AuthManager

class RegisterWindow(tk.Toplevel):
   def __init__(self, parent, role="MAHASISWA"):
      super().__init__(parent)
      self.role = role.upper()
      self.title(f"Add New {self.role.capitalize()}")
      self.geometry("450x670")
      self.configure(bg="#f8f9fa")
      self.resizable(False, False)
      self.grab_set() # Focus on this window

      # --- 1. DEFINISI main_frame (PENTING: Harus sebelum looping fields) ---
      self.main_frame = tk.Frame(self, bg="white", padx=30, pady=25, 
                                 highlightbackground="#d1d1d1", highlightthickness=1)
      self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

      # 2. Generate ID automatically from AuthManager
      # Pastikan di AuthManager sudah ada fungsi generate_next_id
      next_id = AuthManager.generate_next_id(self.role)

      # Header Title
      tk.Label(self.main_frame, text=f"REGISTRATION: {self.role}", 
               font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

      # --- 3. Fields Area ---
      self.entries = {}
      id_label = "Generated NPM" if self.role == "MAHASISWA" else "Generated NIDN"
      
      fields = [
         (id_label, "id_num", next_id), 
         ("Full Name", "name", ""),
         ("Birthday (YYYY-MM-DD)", "birthday", ""),
         ("Gender (M/F)", "gender", ""),
         ("Address", "address", ""),
         ("Phone Number", "phone", "")
      ]

      for label_text, key, default_val in fields:
         tk.Label(self.main_frame, text=label_text, bg="white", 
                  font=("Arial", 9, "bold"), fg="#34495e").pack(anchor="w")
         
         entry = tk.Entry(self.main_frame, font=("Arial", 11), bg="#f1f3f5", 
                           relief="flat", highlightthickness=1, highlightbackground="#dee2e6")
         entry.insert(0, default_val)
         
         # Lock ID field so it cannot be edited
         if key == "id_num":
               entry.config(state="readonly", readonlybackground="#e9ecef")
               
         entry.pack(fill="x", pady=(5, 12), ipady=7)
         self.entries[key] = entry

      # Submit Button
      self.btn_save = tk.Button(self.main_frame, text="SAVE & CREATE ACCOUNT", 
                                 bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), 
                                 height=2, relief="flat", cursor="hand2", 
                                 command=self.handle_save)
      self.btn_save.pack(fill="x", pady=(15, 0))

   def handle_save(self):
      # Get data from entries
      # Special handling for readonly field to get its content
      self.entries['id_num'].config(state='normal')
      data = {key: entry.get().strip() for key, entry in self.entries.items()}
      self.entries['id_num'].config(state='readonly')
      
      # Validation
      if any(not val for val in data.values()):
         messagebox.showwarning("Input Error", "All profile fields are required!")
         return

      # Call AuthManager to save profile and account
      # Pastikan fungsi register_new_user di AuthManager juga menggunakan pesan Inggris
      success, message = AuthManager.register_new_user(data, self.role)

      if success:
         messagebox.showinfo("Success", message)
         if hasattr(self.master, 'refresh'):
               self.master.refresh() # Auto-refresh the table in the background
         self.destroy()
      else:
         messagebox.showerror("Error", message)