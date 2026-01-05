# app/views/dosen/add_materi_ui.py
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from app.controllers.dosen.materi_controller import MateriController

class AddMateriFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller
      self.selected_file_path = ""

      # Header
      header = tk.Frame(self, bg="white", padx=30, pady=20, highlightthickness=1, highlightbackground="#d1d1d1")
      header.pack(fill="x", padx=20, pady=20)
      self.header_label = tk.Label(header, text="ADD MATERIAL", font=("Helvetica", 18, "bold"), bg="white")
      self.header_label.pack(side="left")
      tk.Button(header, text="← Cancel", bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=15, 
               command=lambda: self.controller.show_frame("CourseDetailFrame")).pack(side="right")

      # Form
      form = tk.Frame(self, bg="white", padx=40, pady=30, highlightthickness=1, highlightbackground="#e1e8ed")
      form.pack(pady=10, padx=50, fill="both", expand=True)

      tk.Label(form, text="Title", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
      self.title_entry = tk.Entry(form, font=("Arial", 12), bg="#f1f3f5", relief="flat")
      self.title_entry.pack(fill="x", pady=(5, 15), ipady=8)

      tk.Label(form, text="Content / Description", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
      self.content_text = tk.Text(form, font=("Arial", 11), bg="#f1f3f5", relief="flat", height=6, padx=10, pady=10)
      self.content_text.pack(fill="x", pady=(5, 15))

      # File Picker
      tk.Label(form, text="Attach File", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
      file_frame = tk.Frame(form, bg="white")
      file_frame.pack(fill="x", pady=(5, 20))
      self.file_label = tk.Label(file_frame, text="No file selected", font=("Arial", 9, "italic"), bg="#f1f3f5", anchor="w", padx=10)
      self.file_label.pack(side="left", fill="x", expand=True, ipady=8)
      tk.Button(file_frame, text="Browse", bg="#34495e", fg="white", relief="flat", command=self.browse_file).pack(side="right", padx=5)

      tk.Button(form, text="PUBLISH MATERIAL", bg="#3498db", fg="white", font=("Arial", 11, "bold"), height=2, relief="flat", 
               command=self.handle_save).pack(fill="x")

   def browse_file(self):
      path = filedialog.askopenfilename()
      if path:
         self.selected_file_path = path
         self.file_label.config(text=os.path.basename(path), font=("Arial", 9, "normal"))

   def refresh(self):
      course = self.controller.current_course
      if course: self.header_label.config(text=f"ADD MATERIAL: {course[1]}")
      self.title_entry.delete(0, tk.END)
      self.content_text.delete("1.0", tk.END)
      self.selected_file_path = ""
      self.file_label.config(text="No file selected")

   def handle_save(self):
      title = self.title_entry.get().strip()
      content = self.content_text.get("1.0", "end-1c").strip()
      if not title or not content:
         messagebox.showwarning("Warning", "Title and Content are required!")
         return

      success, msg = MateriController.save_materi(self.controller.current_course[0], title, content, self.selected_file_path)
      if success:
         messagebox.showinfo("Success", msg)
         self.controller.show_frame("CourseDetailFrame")
      else:
         messagebox.showerror("Error", msg)