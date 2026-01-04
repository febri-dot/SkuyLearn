import tkinter as tk
from tkinter import messagebox
from app.controllers.admin.student_controller import StudentController

class StudentDataFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller

      # --- Definisi Lebar Kolom (Gunakan angka yang sama untuk Header & Row) ---
      self.col_widths = {
         "npm": 15,
         "name": 40,
         "gender": 15,
         "actions": 20
      }

      # --- Header ---
      self.header = tk.Frame(self, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#d1d1d1")
      self.header.pack(fill="x", padx=20, pady=(20, 10))
      
      tk.Label(self.header, text="STUDENT LIST", font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50").pack(side="left")
      tk.Button(self.header, text="+ Add Student", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2", command=self.add_student).pack(side="right")

      # --- Table Header (Baris Judul Kolom) ---
      self.table_header_bg = tk.Frame(self, bg="#34495e")
      self.table_header_bg.pack(fill="x", padx=20)
      
      # Samakan urutan dan lebarnya
      tk.Label(self.table_header_bg, text="NPM", width=self.col_widths["npm"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.table_header_bg, text="Full Name", width=self.col_widths["name"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10, anchor="w").pack(side="left")
      tk.Label(self.table_header_bg, text="Gender", width=self.col_widths["gender"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.table_header_bg, text="Actions", width=self.col_widths["actions"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")

      # --- Scrollable Area ---
      self.canvas = tk.Canvas(self, bg="#f8f9fa", highlightthickness=0)
      self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
      self.scroll_frame = tk.Frame(self.canvas, bg="#f8f9fa")

      self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
      self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
      self.canvas.configure(yscrollcommand=self.scrollbar.set)

      self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
      self.scrollbar.pack(side="right", fill="y", padx=(0, 20))

   def refresh(self):
      for widget in self.scroll_frame.winfo_children():
         widget.destroy()

      try:
         students = StudentController.get_all_students()
         for s in students:
               # Setiap baris data
               row = tk.Frame(self.scroll_frame, bg="white", highlightthickness=1, highlightbackground="#f1f1f1")
               row.pack(fill="x", pady=1)

               # Samakan 'width' label di row dengan 'width' label di header
               tk.Label(row, text=s[0], width=self.col_widths["npm"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)
               tk.Label(row, text=s[1], width=self.col_widths["name"], bg="white", font=("Arial", 10), anchor="w").pack(side="left", pady=10)
               tk.Label(row, text=s[2], width=self.col_widths["gender"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)

               # Action Area (Container Tombol)
               action_area = tk.Frame(row, bg="white", width=self.col_widths["actions"])
               action_area.pack(side="left", fill="y")
               action_area.pack_propagate(False) # Mengunci ukuran frame agar tidak menciut

               # Tombol Edit
               btn_edit = tk.Button(action_area, text="Edit", bg="#f1c40f", fg="white", relief="flat",
                                    font=("Arial", 8, "bold"), padx=8, command=lambda d=s: self.edit_student(d))
               btn_edit.pack(side="left", padx=5, pady=8)

               # Tombol Delete
               btn_delete = tk.Button(action_area, text="Delete", bg="#e74c3c", fg="white", relief="flat",
                                    font=("Arial", 8, "bold"), padx=8, command=lambda n=s[0]: self.delete_student(n))
               btn_delete.pack(side="left", padx=2, pady=8)
      except Exception as e:
         print(f"Error loading students: {e}")

   def delete_student(self, npm):
      if messagebox.askyesno("Confirm", f"Delete student with NPM {npm}?"):
         if StudentController.delete_student(npm):
               messagebox.showinfo("Success", "Student deleted.")
               self.refresh()

   def edit_student(self, data):
      messagebox.showinfo("Edit", f"Editing {data[1]}")

   def add_student(self):
      messagebox.showinfo("Add", "Open Add Form")