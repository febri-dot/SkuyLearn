import tkinter as tk
from tkinter import messagebox
from app.controllers.auth_manager import AuthManager

class RegisterFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f0f2f5") 
      self.controller = controller

      self.card = tk.Frame(self, bg="white", padx=40, pady=40, 
                           highlightbackground="#d1d1d1", highlightthickness=1)
      self.card.place(relx=0.5, rely=0.5, anchor="center") 

      tk.Label(self.card, text="SKUYLEARN", bg="white", fg="#2c3e50", 
               font=("Helvetica", 24, "bold")).pack(pady=(0, 10))
      
      tk.Label(self.card, text="Create New Account", bg="white", fg="#7f8c8d", 
               font=("Arial", 10)).pack(pady=(0, 30))

      tk.Label(self.card, text="Username", bg="white", fg="#2c3e50", 
               font=("Arial", 10, "bold")).pack(anchor="w")
      self.username_entry = tk.Entry(self.card, font=("Arial", 12), width=30, 
                                    relief="flat", bg="#f8f9fa")
      self.username_entry.pack(pady=(5, 20), ipady=8)
      tk.Frame(self.card, height=1, bg="#bdc3c7").pack(fill="x", pady=(0, 20)) 

      tk.Label(self.card, text="Password", bg="white", fg="#2c3e50", 
               font=("Arial", 10, "bold")).pack(anchor="w")
      self.password_entry = tk.Entry(self.card, font=("Arial", 12), width=30, 
                                    relief="flat", bg="#f8f9fa", show="•")
      self.password_entry.pack(pady=(5, 5), ipady=8)
      tk.Frame(self.card, height=1, bg="#bdc3c7").pack(fill="x", pady=(0, 30)) 

      tk.Label(self.card, text="Role", bg="white", fg="#2c3e50", 
               font=("Arial", 10, "bold")).pack(anchor="w")

      self.role_var = tk.StringVar(self.card)
      self.role_var.set("MAHASISWA") 

      self.role_menu = tk.OptionMenu(self.card, self.role_var, "ADMIN", "DOSEN", "MAHASISWA")
      self.role_menu.config(font=("Arial", 11), bg="#f8f9fa", relief="flat", width=27)
      self.role_menu.pack(pady=(5, 20), ipady=5)
      
      tk.Frame(self.card, height=1, bg="#bdc3c7").pack(fill="x", pady=(0, 20))

      self.login_btn = tk.Button(self.card, text="CREATE NEW ACCOUNT", bg="#3498db", fg="white", 
                                 font=("Arial", 12, "bold"), width=25, height=2,
                                 relief="flat", cursor="hand2", command=self.handle_register)
      self.login_btn.pack(pady=10)

      tk.Label(self.card, text="E-Learning Project v1.0", bg="white", fg="#bdc3c7", 
               font=("Arial", 8)).pack(pady=(20, 0))

   def handle_register(self):
      username = self.username_entry.get()
      password = self.password_entry.get()
      role = self.role_var.get()

      if not username or not password:
         messagebox.showwarning("Input Error", "Please fill in all fields")
         return

      academic_account = AuthManager.check_academic_identity(username, role)

      if academic_account.status:
         user = AuthManager.is_username_taken(username)

         if user.status:
            pass
 
         else:
            messagebox.showerror("Registration failed", academic_account.message)
         
         
         self.username_entry.delete(0, tk.END)
         self.password_entry.delete(0, tk.END)
      else:
         messagebox.showerror("Authentication Failed", academic_account.message)