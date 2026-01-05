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

        self.title_label = tk.Label(
            header,
            text="COURSE ASSIGNMENTS",
            bg="white", fg="#2c3e50",
            font=("Helvetica", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        tk.Button(
            header, text="← Back to Courses",
            bg="#e74c3c", fg="white",
            relief="flat", cursor="hand2",
            font=("Arial", 9, "bold"), padx=15,
            command=lambda: controller.show_frame("MyCourseFrame")
        ).grid(row=0, column=1, sticky="e")

        # ================= CREATE FORM =================
        form = tk.Frame(
            self, bg="white", padx=25, pady=20,
            highlightbackground="#e1e8ed", highlightthickness=1
        )
        form.pack(fill="x", padx=40, pady=10)

        tk.Label(
            form, text="Create New Assignment",
            font=("Arial", 12, "bold"),
            bg="white", fg="#34495e"
        ).pack(anchor="w", pady=(0, 15))

        self.title_entry = self._input(form, "Assignment Title")
        self.desc_entry = self._input(form, "Description / Instructions")
        self.due_entry = self._input(form, "Due Date (YYYY-MM-DD HH:MM)")

        tk.Button(
            form, text="+ Publish Assignment",
            bg="#2ecc71", fg="white",
            relief="flat", cursor="hand2",
            font=("Arial", 10, "bold"),
            padx=20, pady=8,
            command=self.create_assignment
        ).pack(anchor="w", pady=(10, 0))

        # ================= LIST =================
        tk.Label(
            self, text="Existing Assignments",
            font=("Arial", 12, "bold"),
            bg="#f8f9fa", fg="#34495e"
        ).pack(anchor="w", padx=45, pady=(20, 5))

        self.content = tk.Frame(self, bg="#f8f9fa")
        self.content.pack(fill="both", expand=True, padx=40)

    # ================= INPUT =================
    def _input(self, parent, label):
        tk.Label(
            parent, text=label,
            bg="white", fg="#7f8c8d",
            font=("Arial", 9)
        ).pack(anchor="w")

        entry = tk.Entry(
            parent, font=("Arial", 11),
            bg="#f1f3f5", relief="flat"
        )
        entry.pack(fill="x", pady=(2, 10), ipady=5)
        return entry

    # ================= CREATE =================
    def create_assignment(self):
        course = self.controller.current_course
        if not course:
            messagebox.showerror("Error", "No course selected")
            return

        course_id = course[0]  # tuple index
        title = self.title_entry.get().strip()
        desc = self.desc_entry.get().strip()
        due = self.due_entry.get().strip()

        if not title or not due:
            messagebox.showwarning("Warning", "Title and due date are required")
            return

        success = AssignmentDosenController.create_assignment(
            course_id, title, desc, due
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

        # course[1] = nama course
        self.title_label.config(text=f"ASSIGNMENTS: {course[1]}")

        assignments = AssignmentDosenController.get_assignments_by_course(course[0])

        if not assignments:
            tk.Label(
                self.content,
                text="No assignments for this course yet.",
                bg="#f8f9fa",
                fg="#7f8c8d",
                font=("Arial", 10, "italic")
            ).pack(pady=40)
            return

        for ass in assignments:
            # ass = (id, title, desc, due_date)
            card = tk.Frame(
                self.content, bg="white",
                padx=15, pady=10,
                highlightbackground="#e1e8ed",
                highlightthickness=1
            )
            card.pack(fill="x", pady=6)

            tk.Label(
                card,
                text=ass["title"],
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#2d3436"
            ).pack(side="left")

            tk.Label(
                card,
                text=f"Due: {ass['due_date']}",
                font=("Arial", 9),
                bg="white",
                fg="#e74c3c"
            ).pack(side="right")

