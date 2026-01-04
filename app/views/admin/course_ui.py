import tkinter as tk
from tkinter import messagebox
from app.controllers.mycourse import MyCourseController 
from app.views.course_ui import CourseWindow

class CourseDataFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller 
      self.user = self.controller.current_user 
      
      self.col_widths = {"id": 10, "name": 30, "lecturer": 20, "actions": 15}

      # --- Header Section ---
      self.header = tk.Frame(self, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#d1d1d1")
      self.header.pack(fill="x", padx=20, pady=(20, 10))
      
      self.title_label = tk.Label(self.header, font=("Helvetica", 16, "bold"), bg="white", fg="#2c3e50")
      self.title_label.pack(side="left")
      
      self.btn_add = tk.Button(self.header, text="+ Add Course", bg="#2ecc71", fg="white", 
                              font=("Arial", 9, "bold"), padx=15, pady=5, 
                              cursor="hand2", command=self.add_course)

      # --- Table Header ---
      self.table_header = tk.Frame(self, bg="#34495e")
      self.table_header.pack(fill="x", padx=20)
      
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
      self.user = self.controller.current_user 
      if not self.user: return

      role = self.user.role.lower()
      self.title_label.config(text="ALL COURSES" if role == "admin" else "MY COURSES")
      
      # MODIFIKASI: Dosen juga diberikan izin untuk melihat tombol Add
      if role in ["admin", "dosen"]:
         self.btn_add.pack(side="right")
      else:
         self.btn_add.pack_forget()

      # Update Header Kolom
      for widget in self.table_header.winfo_children():
         widget.destroy()
         
      headers = [("ID", "id"), ("COURSE NAME", "name"), ("LECTURER", "lecturer")]
      # Tampilkan kolom ACTIONS jika Admin (untuk manajemen semua) 
      # atau Dosen (untuk manajemen kursus miliknya sendiri)
      if role in ["admin", "dosen"]: 
         headers.append(("ACTIONS", "actions"))

      for text, key in headers:
         anchor = "w" if key == "name" else "center"
         tk.Label(self.table_header, text=text, width=self.col_widths[key], bg="#34495e", fg="white", 
                  font=("Arial", 9, "bold"), pady=12, anchor=anchor, padx=10 if key=="name" else 0).pack(side="left")

      # Isi Data
      for widget in self.scroll_frame.winfo_children():
         widget.destroy()
      
      courses = MyCourseController.get_courses_for_user(self.user)

      if not courses:
         tk.Label(self.scroll_frame, text="No courses found.", bg="#f8f9fa", font=("Arial", 10, "italic"), pady=20).pack()
         return

      for c in courses:
         row = tk.Frame(self.scroll_frame, bg="white", highlightthickness=1, highlightbackground="#f1f1f1")
         row.pack(fill="x", pady=1)

         # Mapping Nama Dosen: Mahasiswa (indeks 4), Admin/Dosen (indeks 5)
         lecturer_name = c[4] if role == "mahasiswa" else c[5]

         tk.Label(row, text=c[0], width=self.col_widths["id"], bg="white").pack(side="left", pady=10)
         tk.Label(row, text=c[1], width=self.col_widths["name"], bg="white", anchor="w", padx=10).pack(side="left", pady=10)
         tk.Label(row, text=lecturer_name if lecturer_name else "Unknown", width=self.col_widths["lecturer"], bg="white").pack(side="left", pady=10)

         # Tombol Edit/Del hanya untuk Admin atau Dosen (pada kursus miliknya)
         if role in ["admin", "dosen"]:
               action_area = tk.Frame(row, bg="white", width=120)
               action_area.pack(side="left", fill="y")
               
               tk.Button(action_area, text="Edit", bg="#f1c40f", fg="white", font=("Arial", 8, "bold"),
                        command=lambda d=c: self.edit_course(d)).pack(side="left", padx=5, pady=8)
               tk.Button(action_area, text="Del", bg="#e74c3c", fg="white", font=("Arial", 8, "bold"),
                        command=lambda cid=c[0]: self.delete_course(cid)).pack(side="left", padx=2, pady=8)

   def add_course(self):
      CourseWindow(self)

   def edit_course(self, data):
      CourseWindow(self, course_data=data)

   def delete_course(self, course_id):
      if messagebox.askyesno("Confirm Delete", f"Delete course {course_id}?"):
         success, msg = MyCourseController.delete_course(course_id)
         if success:
               messagebox.showinfo("Success", msg)
               self.refresh()
         else:
               messagebox.showerror("Error", msg)