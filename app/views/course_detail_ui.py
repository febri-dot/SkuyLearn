# app/views/course_detail_ui.py
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from app.controllers.course_detail_controller import CourseDetailController
from app.views.dosen.edit_materi_popup import EditMateriPopup
from app.views.dosen.edit_assignment_popup import EditAssignmentPopup


class CourseDetailFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller

      # ================= HEADER =================
      self.header = tk.Frame(self, bg="white", padx=30, pady=20, 
                              highlightthickness=1, highlightbackground="#d1d1d1")
      self.header.pack(fill="x", padx=20, pady=(20, 10))
      
      self.title_label = tk.Label(self.header, text="Course Name", 
                                 font=("Helvetica", 20, "bold"), bg="white", fg="#2c3e50")
      self.title_label.pack(side="left")

      tk.Button(self.header, text="← Back", bg="#e74c3c", fg="white", 
               font=("Arial", 10, "bold"), relief="flat", padx=20, pady=5, cursor="hand2",
               command=self.go_back).pack(side="right")

      # ================= ACTION BAR =================
      self.action_bar = tk.Frame(self, bg="#f8f9fa")
      self.action_bar.pack(fill="x", padx=40, pady=10)

      self.btn_add_materi = tk.Button(self.action_bar, text="+ Add Material", bg="#3498db", 
                                       fg="white", font=("Arial", 10, "bold"), padx=15, pady=8, 
                                       relief="flat", cursor="hand2", command=self.add_materi)
      
      self.btn_add_tugas = tk.Button(self.action_bar, text="+ Add Assignment", bg="#2ecc71", 
                                    fg="white", font=("Arial", 10, "bold"), padx=15, pady=8, 
                                    relief="flat", cursor="hand2", command=self.add_tugas)

      # ================= TIMELINE AREA =================
      self.container = tk.Frame(self, bg="#f8f9fa")
      self.container.pack(fill="both", expand=True, padx=40, pady=5)

      self.canvas = tk.Canvas(self.container, bg="#f8f9fa", highlightthickness=0)
      self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
      self.scroll_frame = tk.Frame(self.canvas, bg="#f8f9fa")

      self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
      self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
      
      self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
      self.canvas.configure(yscrollcommand=self.scrollbar.set)
      self.canvas.pack(side="left", fill="both", expand=True)
      self.scrollbar.pack(side="right", fill="y")

   def go_back(self):
      target = self.controller.current_user.get_course_frame()
      self.controller.show_frame(target)

   def add_materi(self): self.controller.show_frame("AddMateriFrame")
   def add_tugas(self): self.controller.show_frame("AssignmentDosen")

   def refresh(self):
      course = self.controller.current_course
      user = self.controller.current_user
      if not course or not user: return

      self.title_label.config(text=course[1].upper())

      if user.role.lower() == "dosen":
         self.btn_add_materi.pack(side="left", padx=(0, 10))
         self.btn_add_tugas.pack(side="left")
      else:
         self.btn_add_materi.pack_forget()
         self.btn_add_tugas.pack_forget()

      for widget in self.scroll_frame.winfo_children():
         widget.destroy()

      contents = CourseDetailController.get_course_contents(course[0])
      for item in contents:
         self.create_content_card(item)

   def create_content_card(self, item):
      # item: (type, id, title, desc, date, file_path)
      c_type, c_id, c_title, c_desc, c_date, c_file = item
      is_dosen = self.controller.current_user.role.lower() == "dosen"
      is_mahasiswa = self.controller.current_user.role.lower() == "mahasiswa" # Tambahkan ini
      color = "#2ecc71" if c_type == "tugas" else "#3498db"
      
      card = tk.Frame(self.scroll_frame, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#e1e8ed")
      card.pack(fill="x", pady=8, padx=5)

      tk.Frame(card, bg=color, width=6).pack(side="left", fill="y", padx=(0, 20))

      # Main Info
      info_frame = tk.Frame(card, bg="white")
      info_frame.pack(side="left", fill="both", expand=True)

      # Header Card (Title & Management Buttons)
      header_card = tk.Frame(info_frame, bg="white")
      header_card.pack(fill="x")

      tk.Label(header_card, text=f"{'📝' if c_type == 'tugas' else '📘'} {c_title}", 
               font=("Arial", 12, "bold"), bg="white", fg="#2d3436").pack(side="left")

      # Management Buttons (Edit & Delete) - Untuk Dosen
      if is_dosen:
         manage_frame = tk.Frame(card, bg="white")
         manage_frame.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")
         
         edit_btn = tk.Label(manage_frame, text="Edit ✏️", font=("Arial", 9), bg="white", fg="#f39c12", cursor="hand2")
         edit_btn.pack(side="left", padx=5)
         edit_btn.bind("<Button-1>", lambda e: self.edit_item(c_type, item))

         del_btn = tk.Label(manage_frame, text="✕", font=("Arial", 10, "bold"), bg="white", fg="#e74c3c", cursor="hand2")
         del_btn.pack(side="left", padx=5)
         del_btn.bind("<Button-1>", lambda e: self.handle_delete(c_type, c_id, c_title))

      # Description
      tk.Label(info_frame, text=c_desc if c_desc else "No description", 
               font=("Arial", 10), bg="white", fg="#636e72", wraplength=600, justify="left").pack(anchor="w", pady=(5, 10))

      # Download Button (File dari Dosen)
      if c_file and os.path.exists(c_file):
         btn_dl = tk.Button(info_frame, text=f"📥 Download {os.path.basename(c_file)}", 
                           font=("Arial", 9, "bold"), bg="#f1f3f5", fg="#2980b9", 
                           relief="flat", padx=10, cursor="hand2",
                           command=lambda p=c_file: self.open_file(p))
         btn_dl.pack(anchor="w", pady=(0, 10))

      # Footer (Date Info & Submit Button)
      footer = tk.Frame(info_frame, bg="white")
      footer.pack(fill="x")
      
      date_prefix = "Due Date:" if c_type == "tugas" else "Posted on:"
      tk.Label(footer, text=f"{date_prefix} {c_date}", font=("Arial", 8, "italic"), 
               bg="white", fg="#95a5a6").pack(side="left")

      # TOMBOL SUBMIT (Hanya untuk Mahasiswa di item tipe Tugas)
      if is_mahasiswa and c_type == "tugas":
         btn_submit = tk.Button(footer, text="📤 Submit Assignment", 
                              font=("Arial", 9, "bold"), bg="#2ecc71", fg="white", 
                              relief="flat", padx=15, pady=5, cursor="hand2",
                              command=lambda t_id=c_id, t_title=c_title: self.submit_assignment(t_id, t_title))
         btn_submit.pack(side="right")

   # Fungsi baru untuk mengarahkan ke halaman pengumpulan
   def submit_assignment(self, assignment_id, title):
      # Simpan assignment yang dipilih ke controller agar bisa diakses frame berikutnya
      self.controller.current_assignment = (assignment_id, title)
      # Arahkan ke frame pengumpulan (Buat frame ini jika belum ada)
      self.controller.show_frame("AssignmentMahasiswa")

   def open_file(self, path):
      try:
         if os.name == 'nt': # Windows
               os.startfile(path)
         else: # macOS/Linux
               subprocess.run(['open' if os.name == 'posix' else 'xdg-open', path])
      except Exception as e:
         messagebox.showerror("Error", f"Could not open file: {e}")

   def edit_item(self, c_type, item):
      if c_type == "materi":
         EditMateriPopup(self, self.controller.current_course[0], item, self.refresh)
      elif c_type == "tugas":
         EditAssignmentPopup(self, item, self.refresh)

   def handle_delete(self, content_type, item_id, title):
      if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {content_type}: {title}?"):
         if content_type == "materi":
               success = CourseDetailController.delete_materi(self.controller.current_course[0], title)
         else:
               success = CourseDetailController.delete_assignment(item_id)
         
         if success:
               messagebox.showinfo("Success", "Item deleted.")
               self.refresh()