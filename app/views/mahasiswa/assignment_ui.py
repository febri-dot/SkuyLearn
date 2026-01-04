import tkinter as tk
from tkinter import filedialog, messagebox
from app.controllers.mahasiswa.assignment import AssignmentMahasiswaController


class AssignmentMahasiswa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(
            self, bg="white", padx=40, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        header.pack(fill="x", padx=20, pady=20)

        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        tk.Label(
            header,
            text="STUDENT ASSIGNMENTS",
            bg="white", fg="#2c3e50",
            font=("Helvetica", 22, "bold")
        ).grid(row=0, column=0, sticky="w")

        # ===== BACK BUTTON (TOP RIGHT) =====
        tk.Button(
            header,
            text="← Back",
            bg="#e74c3c",
            fg="black",
            relief="flat",
            cursor="hand2",
            command=lambda: controller.show_frame("MyCourseFrame")
        ).grid(row=0, column=1, sticky="e")

        # ================= CONTENT =================
        self.content = tk.Frame(self, bg="#f8f9fa")
        self.content.pack(fill="both", expand=True, padx=20)

    # ================= ASSIGNMENT CARD =================
    def assignment_card(self, parent, assignment):
        card = tk.Frame(
            parent, bg="white", padx=20, pady=15,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        card.pack(fill="x", pady=8)

        # Course name
        tk.Label(
            card,
            text=assignment["course_name"],
            bg="white", fg="#3498db",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        # Assignment title
        tk.Label(
            card,
            text=assignment["title"],
            bg="white", fg="#2c3e50",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(5, 0))

        # Description
        tk.Label(
            card,
            text=assignment["description"] or "-",
            bg="white", fg="#7f8c8d",
            font=("Arial", 10),
            wraplength=800,
            justify="left"
        ).pack(anchor="w", pady=3)

        # Deadline
        tk.Label(
            card,
            text=f"Deadline: {assignment['due_date']}",
            bg="white", fg="#e74c3c",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=2)

        # Submission status
        status_text = (
            f"Submitted file: {assignment['file']}"
            if assignment["file"]
            else "Not submitted yet"
        )

        tk.Label(
            card,
            text=status_text,
            bg="white",
            fg="#27ae60" if assignment["file"] else "#7f8c8d",
            font=("Arial", 10)
        ).pack(anchor="w", pady=3)

        # Submit / Update button
        btn_text = "Update Submission" if assignment["file"] else "Submit Assignment"

        tk.Button(
            card,
            text=btn_text,
            bg="#2ecc71",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.upload_file(assignment)
        ).pack(anchor="e", pady=5)

    # ================= UPLOAD FILE =================
    def upload_file(self, assignment):
        file_path = filedialog.askopenfilename(
            title="Select Assignment File",
            filetypes=[("All Files", "*.*")]
        )

        if not file_path:
            return

        npm = self.controller.current_user.npm

        success = AssignmentMahasiswaController.submit_assignment(
            assignment["id"], npm, file_path
        )

        if success:
            messagebox.showinfo("Success", "Assignment submitted successfully")
            self.refresh()
        else:
            messagebox.showerror("Error", "Failed to submit assignment")

    # ================= REFRESH =================
    def refresh(self):
        user = self.controller.current_user
        course = self.controller.current_course  # ⬅️ course aktif

        if not user or not course:
            return

        for widget in self.content.winfo_children():
            widget.destroy()

        assignments = AssignmentMahasiswaController.get_assignments_by_student(user.npm)

        # ===== FILTER BY COURSE =====
        assignments = [
            a for a in assignments
            if a["course_name"] == course["course_name"]
        ]

        if not assignments:
            tk.Label(
                self.content,
                text="No assignments available for this course",
                bg="#f8f9fa",
                fg="#7f8c8d",
                font=("Arial", 12)
            ).pack(pady=40)
            return

        for assignment in assignments:
            self.assignment_card(self.content, assignment)
