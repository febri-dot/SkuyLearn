# app/views/dosen/edit_materi_popup.py
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from app.controllers.dosen.materi_controller import MateriController

class EditMateriPopup(tk.Toplevel):
   def __init__(self, parent, course_id, item_data, callback):
      super().__init__(parent)
      self.title("Edit Material")
      self.geometry("500x600")
      self.configure(bg="white")
      self.transient(parent)
      self.grab_set()

      self.course_id = course_id
      self.old_title = item_data[2]
      self.selected_file_path = item_data[5] 
      self.callback = callback

      tk.Label(self, text="EDIT MATERIAL", font=("Arial", 14, "bold"), bg="white").pack(pady=20)
      container = tk.Frame(self, bg="white", padx=30)
      container.pack(fill="both", expand=True)

      tk.Label(container, text="Title", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      self.title_entry = tk.Entry(container, font=("Arial", 11), bg="#f1f3f5", relief="flat")
      self.title_entry.insert(0, self.old_title)
      self.title_entry.pack(fill="x", pady=(5, 15), ipady=8)

      tk.Label(container, text="Content", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      self.content_text = tk.Text(container, font=("Arial", 10), bg="#f1f3f5", relief="flat", height=6, padx=10, pady=10)
      self.content_text.insert("1.0", item_data[3])
      self.content_text.pack(fill="x", pady=(5, 15))

      tk.Label(container, text="File", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      file_frame = tk.Frame(container, bg="white")
      file_frame.pack(fill="x", pady=(5, 20))
      
      display_name = os.path.basename(self.selected_file_path) if self.selected_file_path else "No file attached"
      self.file_label = tk.Label(file_frame, text=display_name, font=("Arial", 9, "italic"), bg="#f1f3f5", anchor="w", padx=10)
      self.file_label.pack(side="left", fill="x", expand=True, ipady=8)
      tk.Button(file_frame, text="Change", command=self.browse_file).pack(side="right")

      tk.Button(container, text="SAVE CHANGES", bg="#3498db", fg="white", font=("Arial", 10, "bold"), height=2, relief="flat", 
               command=self.handle_update).pack(fill="x", pady=20)

   def browse_file(self):
      path = filedialog.askopenfilename()
      if path:
         self.selected_file_path = path
         self.file_label.config(text=os.path.basename(path))

   def handle_update(self):
      new_title = self.title_entry.get().strip()
      new_content = self.content_text.get("1.0", "end-1c").strip()
      
      success, msg = MateriController.update_materi(self.course_id, self.old_title, new_title, new_content, self.selected_file_path)
      if success:
         messagebox.showinfo("Success", msg)
         self.callback()
         self.destroy()
      else:
         messagebox.showerror("Error", msg)