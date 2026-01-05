# app/views/home_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.controllers.mycourse import MyCourseController
from tkinter import ttk, messagebox, simpledialog

class HomeFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller
      self.all_data = []

      # ================= HEADER & SEARCH =================
      header = tk.Frame(self, bg="white", padx=30, pady=20, highlightthickness=1, highlightbackground="#d1d1d1")
      header.pack(fill="x", padx=20, pady=20)

      tk.Label(header, text="EXPLORE COURSES", font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50").pack(side="left")

      search_frame = tk.Frame(header, bg="white")
      search_frame.pack(side="right")
      
      tk.Label(search_frame, text="Search:", bg="white", font=("Arial", 10)).pack(side="left", padx=5)
      self.search_entry = tk.Entry(search_frame, font=("Arial", 11), bg="#f1f3f5", relief="flat", width=25)
      self.search_entry.pack(side="left", padx=5, ipady=5)
      self.search_entry.bind("<KeyRelease>", self.on_search)

      # ================= TABLE AREA =================
      self.table_container = tk.Frame(self, bg="white", padx=20, pady=20, highlightthickness=1, highlightbackground="#e1e8ed")
      self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

      # Kita tidak membuat Treeview di __init__, tapi di refresh() agar kolomnya dinamis
      self.tree = None
      self.info_label = tk.Label(self, text="* Double-click on a row to Enroll Me", 
                                 font=("Arial", 9, "italic"), bg="#f8f9fa", fg="#7f8c8d")

   def is_mahasiswa(self):
      user = self.controller.current_user
      return user and user.role.lower() == "mahasiswa"

   def setup_table(self):
      """Membuat ulang struktur tabel berdasarkan role user"""
      if self.tree:
         self.tree.destroy()

      columns = ("id", "name", "lecturer", "desc")
      if self.is_mahasiswa():
         columns = ("id", "name", "lecturer", "desc", "action")

      self.tree = ttk.Treeview(self.table_container, columns=columns, show="headings", height=15)
      
      # Style
      self.tree.heading("id", text="ID")
      self.tree.heading("name", text="Course Name")
      self.tree.heading("lecturer", text="Lecturer")
      self.tree.heading("desc", text="Description")
      
      self.tree.column("id", width=50, anchor="center")
      self.tree.column("name", width=200)
      self.tree.column("lecturer", width=150)
      self.tree.column("desc", width=300)

      if self.is_mahasiswa():
         self.tree.heading("action", text="Action")
         self.tree.column("action", width=120, anchor="center")
         self.tree.bind("<Double-1>", self.on_item_double_click)
         self.info_label.pack(pady=5)
      else:
         self.info_label.pack_forget()

      self.tree.pack(fill="both", expand=True)
      
      # Re-attach scrollbar
      scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
      self.tree.configure(yscrollcommand=scrollbar.set)
      # Hapus scrollbar lama jika ada dan pasang yang baru
      for widget in self.table_container.winfo_children():
         if isinstance(widget, ttk.Scrollbar):
               widget.destroy()
      scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
      self.tree.configure(yscrollcommand=scrollbar.set)
      scrollbar.pack(side="right", fill="y")

   def on_search(self, event=None):
      if not self.tree: return
      query = self.search_entry.get().lower()
      for item in self.tree.get_children():
         self.tree.delete(item)
      
      for row in self.all_data:
         if query in row[1].lower() or query in row[2].lower():
               self.add_row_to_tree(row)

   def add_row_to_tree(self, row):
      if self.is_mahasiswa():
         # row[0]=id, row[1]=name, row[2]=lecturer, row[3]=desc
         self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], "➕ Enroll Me"))
      else:
         self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3]))

   def on_item_double_click(self, event):
      if not self.is_mahasiswa(): return
      
      selected = self.tree.selection()
      if not selected: return
      
      item_id = selected[0]
      item_values = self.tree.item(item_id, 'values')
      course_id = item_values[0]
      course_name = item_values[1]

      # 1. Tanya apakah yakin mau enroll
      if messagebox.askyesno("Enroll Course", f"Do you want to enroll in '{course_name}'?"):
         
         # 2. Minta Enrollment Key melalui dialog input
         enroll_key_input = simpledialog.askstring(
            "Enrollment Key Required", 
            f"Enter the key for {course_name}:",
            parent=self
         )

         # Jika user menekan 'Cancel'
         if enroll_key_input is None:
            return
         
         # 3. Kirim data ke controller untuk divalidasi dengan DB
         student_id = self.controller.current_user.username 
         
         # Controller akan mengecek apakah key input == key di DB
         success, msg = MyCourseController.enroll_student(course_id, student_id, enroll_key_input)
         
         if success:
            messagebox.showinfo("Success", "Enrollment successful! You can now access the course.")
            # Optional: arahkan langsung ke halaman MyCourse
            self.controller.show_frame("MyCourseFrame")
         else:
            # Jika key salah atau sudah terdaftar, munculkan pesan error dari controller
            messagebox.showerror("Enrollment Failed", msg)

   def refresh(self):
      # 1. Setup tabel ulang setiap kali refresh (agar kolom menyesuaikan login)
      self.setup_table()
      # 2. Ambil data
      self.all_data = MyCourseController.get_all_courses_with_owner()
      # 3. Tampilkan data
      self.on_search()