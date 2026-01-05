# app/views/dosen/edit_assignment_popup.py
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from app.controllers.dosen.assignment import AssignmentDosenController

class EditAssignmentPopup(tk.Toplevel):
   def __init__(self, parent, item_data, callback):
      super().__init__(parent)
      self.title("Edit Assignment")
      self.geometry("500x650")
      self.configure(bg="white")
      self.transient(parent)
      self.grab_set()

      # item_data: (type, id, title, description, due_date, file_path)
      self.assignment_id = item_data[1]
      self.current_file_path = item_data[5]
      self.selected_file_path = item_data[5]
      self.callback = callback

      tk.Label(self, text="EDIT ASSIGNMENT", font=("Arial", 14, "bold"), 
               bg="white", fg="#2c3e50").pack(pady=20)

      container = tk.Frame(self, bg="white", padx=30)
      container.pack(fill="both", expand=True)

      # Title
      tk.Label(container, text="Assignment Title", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      self.title_entry = tk.Entry(container, font=("Arial", 11), bg="#f1f3f5", relief="flat")
      self.title_entry.insert(0, item_data[2])
      self.title_entry.pack(fill="x", pady=(5, 15), ipady=8)

      # Description
      tk.Label(container, text="Description / Instructions", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      self.desc_text = tk.Text(container, font=("Arial", 10), bg="#f1f3f5", relief="flat", height=6, padx=10, pady=10)
      self.desc_text.insert("1.0", item_data[3])
      self.desc_text.pack(fill="x", pady=(5, 15))

      # Due Date
      tk.Label(container, text="Due Date (YYYY-MM-DD HH:MM)", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      self.due_entry = tk.Entry(container, font=("Arial", 11), bg="#f1f3f5", relief="flat")
      self.due_entry.insert(0, item_data[4])
      self.due_entry.pack(fill="x", pady=(5, 15), ipady=8)

      # File Section
      tk.Label(container, text="Assignment File", font=("Arial", 9, "bold"), bg="white").pack(anchor="w")
      file_frame = tk.Frame(container, bg="white")
      file_frame.pack(fill="x", pady=(5, 20))

      display_name = os.path.basename(self.selected_file_path) if self.selected_file_path else "No file attached"
      self.file_label = tk.Label(file_frame, text=display_name, font=("Arial", 9, "italic"), 
                                 bg="#f1f3f5", fg="#2c3e50", anchor="w", padx=10)
      self.file_label.pack(side="left", fill="x", expand=True, ipady=8)

      tk.Button(file_frame, text="Change", bg="#34495e", fg="white", relief="flat", 
               command=self.browse_file).pack(side="right", padx=(5, 0))

      # Action Buttons
      btn_frame = tk.Frame(container, bg="white")
      btn_frame.pack(fill="x", pady=20)

      tk.Button(btn_frame, text="UPDATE ASSIGNMENT", bg="#2ecc71", fg="white", 
               font=("Arial", 10, "bold"), height=2, relief="flat", 
               command=self.handle_update).pack(fill="x")

   def browse_file(self):
      path = filedialog.askopenfilename()
      if path:
         self.selected_file_path = path
         self.file_label.config(text=os.path.basename(path))

   def handle_update(self):
      title = self.title_entry.get().strip()
      desc = self.desc_text.get("1.0", "end-1c").strip()
      due = self.due_entry.get().strip()

      if not title or not due:
         messagebox.showwarning("Warning", "Title and Due Date are required!")
         return

      success, msg = AssignmentDosenController.update_assignment(
         self.assignment_id, title, desc, due, self.selected_file_path, self.current_file_path
      )

      if success:
         messagebox.showinfo("Success", msg)
         self.callback() # Refresh CourseDetailFrame
         self.destroy()
      else:
         messagebox.showerror("Error", msg)