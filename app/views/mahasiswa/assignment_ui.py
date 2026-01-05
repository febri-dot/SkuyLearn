# app/views/mahasiswa/assignment_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from app.controllers.mahasiswa.assignment import AssignmentMahasiswaController

class AssignmentMahasiswa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(self, bg="white", padx=40, pady=20, highlightthickness=1, highlightbackground="#d1d1d1")
        header.pack(fill="x", padx=20, pady=20)

        title_container = tk.Frame(header, bg="white")
        title_container.pack(fill="x")

        tk.Label(title_container, text="MY ASSIGNMENTS", bg="white", fg="#2c3e50", font=("Helvetica", 22, "bold")).pack(side="left")

        tk.Button(title_container, text="← Back to Course", bg="#e74c3c", fg="white", 
                font=("Arial", 10, "bold"), padx=15, pady=8, relief="flat", cursor="hand2", 
                command=self.go_back # Panggil fungsi go_back, jangan lambda show_frame langsung
        ).pack(side="right")

        # ================= CONTENT AREA (SCROLLABLE) =================
        self.container = tk.Frame(self, bg="#f8f9fa")
        self.container.pack(fill="both", expand=True, padx=20)
        
        self.canvas = tk.Canvas(self.container, bg="#f8f9fa", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.content = tk.Frame(self.canvas, bg="#f8f9fa")

        self.content.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def assignment_card(self, parent, assignment):
        # 1. Main Outer Card (Tema Putih Bersih)
        card = tk.Frame(parent, bg="white", padx=25, pady=20, highlightthickness=1, highlightbackground="#e1e8ed")
        card.pack(fill="x", pady=10, padx=20)

        # Aksen warna hijau di samping (khas Tugas/Assignment)
        tk.Frame(card, bg="#2ecc71", width=6).pack(side="left", fill="y", padx=(0, 20))

        # Content Container
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side="left", fill="both", expand=True)

        # Course Badge
        tk.Label(info_frame, text=assignment["course_name"].upper(), bg="#ebfbee", fg="#27ae60", 
                font=("Arial", 9, "bold"), padx=10).pack(anchor="w", pady=(0, 5))

        # Assignment Title
        tk.Label(info_frame, text=assignment["title"], bg="white", fg="#2c3e50", 
                font=("Helvetica", 16, "bold")).pack(anchor="w")

        # Description
        tk.Label(info_frame, text=assignment["description"] or "No instructions provided.", 
                bg="white", fg="#7f8c8d", font=("Arial", 10), wraplength=700, justify="left").pack(anchor="w", pady=10)

        # Details Row (Deadline & Status)
        details_row = tk.Frame(info_frame, bg="white")
        details_row.pack(fill="x", pady=(5, 0))

        tk.Label(details_row, text=f"📅 Deadline: {assignment['due_date']}", 
                bg="white", fg="#e74c3c", font=("Arial", 10, "bold")).pack(side="left")

        # Submission Status Badge
        status_bg = "#e8f5e9" if assignment["file"] else "#f8f9fa"
        status_fg = "#2e7d32" if assignment["file"] else "#95a5a6"
        status_text = f"✓ Submitted: {os.path.basename(assignment['file'])}" if assignment["file"] else "○ Not Submitted"
        
        tk.Label(details_row, text=status_text, bg=status_bg, fg=status_fg, 
                font=("Arial", 9, "italic"), padx=10).pack(side="left", padx=20)

        # 2. Action Button (Di pojok kanan bawah card)
        btn_text = "UPDATE SUBMISSION" if assignment["file"] else "SUBMIT ASSIGNMENT"
        btn_color = "#f39c12" if assignment["file"] else "#2ecc71"

        tk.Button(card, text=btn_text, bg=btn_color, fg="white", font=("Arial", 10, "bold"),
                padx=20, pady=10, relief="flat", cursor="hand2",
                command=lambda: self.upload_file(assignment)).pack(side="right", anchor="s")

    def upload_file(self, assignment):
        file_path = filedialog.askopenfilename(title="Select Assignment File")
        if not file_path: return

        npm = self.controller.current_user.npm
        success = AssignmentMahasiswaController.submit_assignment(assignment["id"], npm, file_path)

        if success:
            messagebox.showinfo("Success", "Your assignment has been uploaded!")
            self.refresh()
        else:
            messagebox.showerror("Error", "Failed to upload assignment.")

    def refresh(self):
        user = self.controller.current_user
        course = self.controller.current_course
        
        # Ambil tugas yang sedang dipilih dari controller
        selected_task = getattr(self.controller, 'current_assignment', None)

        if not user or not course: return

        for widget in self.content.winfo_children():
            widget.destroy()

        all_assignments = AssignmentMahasiswaController.get_assignments_by_student(user.npm)

        # ===== LOGIC FILTER YANG DIPERBAIKI =====
        if selected_task:
            # Tetap kunci tampilan hanya pada ID tugas ini
            assignments = [a for a in all_assignments if a["id"] == selected_task[0]]
            
            # Jangan di-set None di sini! 
            # Biarkan tetap ada supaya saat refresh() dipanggil lagi setelah upload, 
            # filternya masih nempel.
        else:
            # Jika masuk lewat menu MyCourse (bukan tombol submit spesifik)
            assignments = [a for a in all_assignments if a["course_name"] == course[1]]

        if not assignments:
            tk.Label(self.content, text="No assignments to show.", bg="#f8f9fa", 
                    fg="#7f8c8d", font=("Arial", 12, "italic")).pack(pady=100)
            return

        for assignment in assignments:
            self.assignment_card(self.content, assignment)

    # Update fungsi Back agar membersihkan filter
    def go_back(self):
        # Bersihkan filter tugas spesifik sebelum kembali
        if hasattr(self.controller, 'current_assignment'):
            self.controller.current_assignment = None
        self.controller.show_frame("CourseDetailFrame")