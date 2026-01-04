import tkinter as tk
from tkinter import messagebox
from app.controllers.auth_manager import AuthManager

class EditUserWindow(tk.Toplevel):
   def __init__(self, parent, user_data, role="MAHASISWA"):
      super().__init__(parent)
      self.role = role.upper()
      self.user_data = user_data 
      self.title(f"Edit {self.role.capitalize()}")
      self.geometry("450x750")
      self.configure(bg="#f8f9fa")
      self.grab_set()

      self.main_frame = tk.Frame(self, bg="white", padx=30, pady=25, 
                                 highlightbackground="#d1d1d1", highlightthickness=1)
      self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

      tk.Label(self.main_frame, text=f"EDIT {self.role} DATA", 
               font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

      self.entries = {}
      
      # Mapping data dari tabel ke field (Sesuaikan index s[0], s[1] dsb dari refresh tabelmu)
      # Misal: s[0]=NPM, s[1]=Name, s[2]=Birthday, s[3]=Gender, s[4]=Address, s[5]=Phone
      initial_values = {
         "id_num": user_data[0],
         "name": user_data[1],
         "birthday": user_data[2],
         "gender": user_data[3],
         "address": user_data[4],
         "phone": user_data[5],
         "password": user_data[6]
      }

      fields = [
         ("NPM" if self.role == "MAHASISWA" else "NIDN", "id_num"),
         ("Full Name", "name"),
         ("Birthday (YYYY-MM-DD)", "birthday"),
         ("Gender", "gender"),
         ("Address", "address"),
         ("Phone Number", "phone"),
         ("New Password (Leave same if no change)", "password") 
      ]

      for label_text, key in fields:
         tk.Label(self.main_frame, text=label_text, bg="white", 
                  font=("Arial", 9, "bold"), fg="#34495e").pack(anchor="w")
         
         entry = tk.Entry(self.main_frame, font=("Arial", 11), bg="#f1f3f5", relief="flat")
         
         # Isi data awal jika bukan field password
         entry.insert(0, initial_values[key])

         # ID tidak boleh diubah karena itu Primary Key/Username
         if key == "id_num":
            entry.config(state="readonly", readonlybackground="#e9ecef")
               
         entry.pack(fill="x", pady=(5, 12), ipady=7)
         self.entries[key] = entry

      tk.Button(self.main_frame, text="UPDATE DATA", bg="#f1c40f", fg="white", 
               font=("Arial", 11, "bold"), height=2, relief="flat", 
               command=self.handle_update).pack(fill="x", pady=15)

   def handle_update(self):
      self.entries['id_num'].config(state='normal')
      data = {key: entry.get().strip() for key, entry in self.entries.items()}
      self.entries['id_num'].config(state='readonly')

      if any(not val for val in data.values()):
         messagebox.showwarning("Input Error", "All fields must be filled!")
         return

      success, message = AuthManager.update_user_data(data, self.role)

      if success:
         messagebox.showinfo("Success", message)
         if hasattr(self.master, 'refresh'):
               self.master.refresh()
         self.destroy()
      else:
         messagebox.showerror("Error", message)