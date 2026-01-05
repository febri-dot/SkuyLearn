# app/views/dosen/assignment_ui.py
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from app.controllers.dosen.assignment import AssignmentDosenController

class AssignmentDosen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller
        self.selected_file_path = "" # Variable to store the picked file path

        # ================= HEADER =================
        header = tk.Frame(self, bg="white", padx=30, pady=20, 
                          highlightthickness=1, highlightbackground="#d1d1d1")
        header.pack(fill="x", padx=20, pady=20)
        
        self.header_label = tk.Label(header, text="ASSIGNMENTS", 
                                     font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50")
        self.header_label.pack(side="left")

        tk.Button(header, text="← Back", bg="#e74c3c", fg="white", 
                  font=("Arial", 10, "bold"), relief="flat", padx=15, cursor="hand2",
                  command=lambda: self.controller.show_frame("CourseDetailFrame")).pack(side="right")

        # ================= FORM CONTAINER =================
        form_container = tk.Frame(self, bg="white", padx=40, pady=30, 
                                  highlightthickness=1, highlightbackground="#e1e8ed")
        form_container.pack(pady=10, padx=50, fill="both", expand=True)

        # Assignment Title
        tk.Label(form_container, text="Assignment Title", font=("Arial", 10, "bold"), 
                 bg="white", fg="#34495e").pack(anchor="w")
        self.title_entry = tk.Entry(form_container, font=("Arial", 12), bg="#f1f3f5", relief="flat")
        self.title_entry.pack(fill="x", pady=(5, 15), ipady=8)

        # Description
        tk.Label(form_container, text="Instructions / Description", font=("Arial", 10, "bold"), 
                 bg="white", fg="#34495e").pack(anchor="w")
        self.desc_text = tk.Text(form_container, font=("Arial", 11), bg="#f1f3f5", 
                                 relief="flat", height=5, padx=10, pady=10)
        self.desc_text.pack(fill="x", pady=(5, 15))

        # Due Date
        tk.Label(form_container, text="Due Date (YYYY-MM-DD HH:MM)", font=("Arial", 10, "bold"), 
                 bg="white", fg="#34495e").pack(anchor="w")
        self.due_entry = tk.Entry(form_container, font=("Arial", 11), bg="#f1f3f5", relief="flat")
        self.due_entry.pack(fill="x", pady=(5, 15), ipady=8)

        # ================= UPLOAD FILE SECTION =================
        tk.Label(form_container, text="Assignment Template/File (Optional)", font=("Arial", 10, "bold"), 
                 bg="white", fg="#34495e").pack(anchor="w")
        
        file_frame = tk.Frame(form_container, bg="white")
        file_frame.pack(fill="x", pady=(5, 20))

        self.file_label = tk.Label(file_frame, text="No file selected", font=("Arial", 9, "italic"), 
                                   bg="#f1f3f5", fg="#7f8c8d", anchor="w", padx=10)
        self.file_label.pack(side="left", fill="x", expand=True, ipady=8)

        tk.Button(file_frame, text="Browse", bg="#34495e", fg="white", font=("Arial", 9, "bold"), 
                  padx=15, relief="flat", cursor="hand2", command=self.browse_file).pack(side="right", padx=(5, 0))

        # Submit Button
        tk.Button(form_container, text="PUBLISH ASSIGNMENT", bg="#2ecc71", fg="white", 
                  font=("Arial", 11, "bold"), height=2, relief="flat", cursor="hand2", 
                  command=self.create_assignment).pack(fill="x")

    def browse_file(self):
        path = filedialog.askopenfilename(title="Select Assignment File")
        if path:
            self.selected_file_path = path
            self.file_label.config(text=os.path.basename(path), fg="#2c3e50", font=("Arial", 9, "normal"))

    def refresh(self):
        course = self.controller.current_course
        if course:
            self.header_label.config(text=f"ASSIGNMENTS: {course[1]}")
        
        # Reset form fields
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.due_entry.delete(0, tk.END)
        self.selected_file_path = ""
        self.file_label.config(text="No file selected", fg="#7f8c8d", font=("Arial", 9, "italic"))

    def create_assignment(self):
        course = self.controller.current_course
        if not course: return

        title = self.title_entry.get().strip()
        desc = self.desc_text.get("1.0", "end-1c").strip()
        due = self.due_entry.get().strip()

        if not title or not due:
            messagebox.showwarning("Warning", "Title and Due Date are required!")
            return

        # Send to controller (course[0] is ID)
        success, msg = AssignmentDosenController.create_assignment(
            course[0], title, desc, due, self.selected_file_path
        )

        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame("CourseDetailFrame")
        else:
            messagebox.showerror("Error", msg)