import tkinter as tk
from tkinter import messagebox
from app.controllers.dosen.assignment import AssignmentDosenController


class AssignmentDosen(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(
            self, bg="white", padx=30, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        header.pack(fill="x", padx=20, pady=20)

        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="COURSE ASSIGNMENTS",
            bg="white",
            fg="#2c3e50",
            font=("Helvetica", 22, "bold")
        ).grid(row=0, column=0, sticky="w")

        tk.Button(
            header,
            text="← Back",
            bg="#e74c3c",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: controller.show_frame("MyCourseFrame")
        ).grid(row=0, column=1, sticky="e")

        # ================= CREATE ASSIGNMENT =================
        form = tk.Frame(self, bg="#f8f9fa")
        form.pack(fill="x", padx=40, pady=10)

        tk.Label(form, text="Create New Assignment",
                 font=("Arial", 14, "bold"),
                 bg="#f8f9fa").pack(anchor="w", pady=(0, 10))

        self.title_entry = self._input(form, "Title")
        self.desc_entry = self._input(form, "Description")
        self.due_entry = self._input(form, "Due Date (YYYY-MM-DD)")

        tk.Button(
            form,
            text="Create Assignment",
            bg="#2ecc71",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.create_assignment
        ).pack(anchor="w", pady=10)

        # ================= ASSIGNMENT LIST =================
        self.content = tk.Frame(self, bg="#f8f9fa")
        self.content.pack(fill="both", expand=True, padx=20)

    def _input(self, parent, label):
        tk.Label(parent, text=label, bg="#f8f9fa").pack(anchor="w")
        entry = tk.Entry(parent, width=50)
        entry.pack(anchor="w", pady=5)
        return entry

    # ================= CREATE =================
    def create_assignment(self):
        course = self.controller.current_course
        if not course:
            messagebox.showerror("Error", "No course selected")
            return

        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due = self.due_entry.get()

        if not title or not due:
            messagebox.showwarning("Warning", "Title and due date are required")
            return

        success = AssignmentDosenController.create_assignment(
            course["id"], title, desc, due
        )

        if success:
            messagebox.showinfo("Success", "Assignment created successfully")
            self.title_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.due_entry.delete(0, tk.END)

            self.refresh()
        else:
            messagebox.showerror("Error", "Failed to create assignment")

    # ================= REFRESH =================
    def refresh(self):
        for w in self.content.winfo_children():
            w.destroy()

        course = self.controller.current_course
        if not course:
            return

        assignments = AssignmentDosenController.get_assignments_by_course(course["id"])

        if not assignments:
            tk.Label(
                self.content,
                text="No assignments for this course",
                bg="#f8f9fa",
                fg="#7f8c8d"
            ).pack(pady=40)
            return