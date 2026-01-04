import tkinter as tk
from tkinter import messagebox
from app.controllers.admin.student_controller import StudentController
from app.views.admin.register_ui import RegisterWindow
from app.views.admin.edit_user_ui import EditUserWindow
from app.controllers.auth_manager import AuthManager


class StudentDataFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller

      # --- Definisi Lebar Kolom (Gunakan unit karakter) ---
      self.col_widths = {
         "column": 15,
         "long_column": 25,
         "actions": 20
      }

      # --- Header Section ---
      self.header = tk.Frame(self, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#d1d1d1")
      self.header.pack(fill="x", padx=20, pady=(20, 10))
      
      tk.Label(self.header, text="STUDENT LIST", font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50").pack(side="left")
      tk.Button(self.header, text="+ Add Student", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2", command=self.add_student).pack(side="right")

      # --- Table Header (Tetap di luar Canvas agar tidak ikut ter-scroll) ---
      self.table_header_bg = tk.Frame(self, bg="#34495e")
      self.table_header_bg.pack(fill="x", padx=20)
      
      # Tambahkan inner frame agar paddingnya sama dengan baris data di canvas
      self.header_inner = tk.Frame(self.table_header_bg, bg="#34495e")
      self.header_inner.pack(anchor="nw")

      tk.Label(self.header_inner, text="Username", width=self.col_widths["column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Full Name", width=self.col_widths["long_column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10, anchor="w", padx=10).pack(side="left")
      tk.Label(self.header_inner, text="Phone Number", width=self.col_widths["column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Address", width=self.col_widths["long_column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Actions", width=self.col_widths["actions"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")

      # --- Scrollable Area ---
      self.container = tk.Frame(self, bg="#f8f9fa")
      self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

      # Tambahkan scrollbar horizontal di sini
      self.h_scrollbar = tk.Scrollbar(self.container, orient="horizontal")
      self.h_scrollbar.pack(side="bottom", fill="x")

      self.canvas = tk.Canvas(self.container, bg="#f8f9fa", highlightthickness=0,
                              xscrollcommand=self.h_scrollbar.set) # Hubungkan horizontal
      self.v_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
      
      self.scroll_frame = tk.Frame(self.canvas, bg="#f8f9fa")

      # Update scrollregion untuk Vertikal DAN Horizontal
      self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
      
      self.canvas_frame = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
      
      # HUBUNGKAN KEMBALI SCROLLBAR
      self.v_scrollbar.config(command=self.canvas.yview)
      self.h_scrollbar.config(command=self.canvas.xview)
      self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

      self.canvas.pack(side="left", fill="both", expand=True)
      self.v_scrollbar.pack(side="right", fill="y")

   def _on_canvas_configure(self, event):
      """Memaksa lebar scroll_frame mengikuti lebar canvas"""
      self.canvas.itemconfig(self.canvas_frame, width=event.width)

   def refresh(self):
      """Clear and reload data from Controller"""
      for widget in self.scroll_frame.winfo_children():
         widget.destroy()

      try:
         students = StudentController.get_all_students()
         if not students:
               tk.Label(self.scroll_frame, text="No students found.", bg="#f8f9fa", pady=20).pack()
               return

         for s in students:
               row = tk.Frame(self.scroll_frame, bg="white", highlightthickness=1, highlightbackground="#f1f1f1")
               row.pack(fill="x", pady=1)

               # Samakan lebar dengan Header
               tk.Label(row, text=s[0], width=self.col_widths["column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)
               tk.Label(row, text=s[1], width=self.col_widths["long_column"], bg="white", font=("Arial", 10), anchor="w", padx=10).pack(side="left", pady=10)
               tk.Label(row, text=s[5], width=self.col_widths["column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)
               tk.Label(row, text=s[4], width=self.col_widths["long_column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)

               # Action Area
               action_area = tk.Frame(row, bg="white", width=180) 
               action_area.pack(side="left", fill="y")
               action_area.pack_propagate(False) 

               btn_edit = tk.Button(action_area, text="Edit", bg="#f1c40f", fg="white", relief="flat",
                                 font=("Arial", 8, "bold"), padx=10, cursor="hand2", command=lambda d=s: self.edit_student(d))
               btn_edit.pack(side="left", padx=5, pady=8)

               btn_delete = tk.Button(action_area, text="Delete", bg="#e74c3c", fg="white", relief="flat",
                                    font=("Arial", 8, "bold"), padx=10, cursor="hand2", command=lambda n=s[0]: self.delete_student(n))
               btn_delete.pack(side="left", padx=2, pady=8)
      except Exception as e:
         print(f"Error loading students: {e}")

   # --- Actions ---
   def delete_student(self, npm):
      if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ID {npm}?\nThis will also delete the login account and this action cannot be undone."):
         success, message = AuthManager.delete_user(npm, "MAHASISWA")
         if success:
               messagebox.showinfo("Success", "Student and account have been deleted successfully.")
               self.refresh() 
         else:
               messagebox.showerror("Error", message)

   def edit_student(self, data):
      EditUserWindow(self, user_data=data, role="MAHASISWA")

   def add_student(self):
      RegisterWindow(self, role="MAHASISWA")