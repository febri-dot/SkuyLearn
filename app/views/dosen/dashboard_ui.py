# app/views/dosen/dashboard_dosen.py
import tkinter as tk
from tkinter import messagebox
from app.controllers.dosen.dashboard import DashboardDosenController
from app.views.course_ui import CourseWindow 

class DashboardDosen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(self, bg="white", padx=40, pady=20, highlightthickness=1, highlightbackground="#d1d1d1")
        header.pack(fill="x", padx=20, pady=20)

        title_container = tk.Frame(header, bg="white")
        title_container.pack(fill="x")

        tk.Label(title_container, text="LECTURER DASHBOARD", bg="white", fg="#2c3e50", font=("Helvetica", 22, "bold")).pack(side="left")
        
        tk.Button(title_container, text="+ Create New Course", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
                  padx=20, pady=8, relief="flat", cursor="hand2", command=lambda: CourseWindow(self)).pack(side="right")

        self.info_label = tk.Label(header, bg="white", fg="#7f8c8d", font=("Helvetica", 13))
        self.info_label.pack(anchor="w", pady=(10, 0))

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

    def course_card_wrapper(self, parent, course):
        # 1. Main Outer Card
        main_card = tk.Frame(parent, bg="white", padx=25, pady=20, highlightthickness=1, highlightbackground="#e1e8ed")
        main_card.pack(fill="x", pady=15, padx=20)

        # Header Card: Judul & Tombol Hapus
        header_card = tk.Frame(main_card, bg="white")
        header_card.pack(fill="x", pady=(0, 15))

        tk.Label(header_card, text=course["course_name"].upper(), bg="white", fg="#2c3e50", font=("Helvetica", 16, "bold")).pack(side="left")
        
        # Tombol Delete Course
        btn_del = tk.Label(header_card, text="🗑 Delete Course", bg="white", fg="#e74c3c", font=("Arial", 9, "bold"), cursor="hand2")
        btn_del.pack(side="right")
        btn_del.bind("<Button-1>", lambda e, c_id=course["course_id"], c_name=course["course_name"]: 
            self.confirm_delete(c_id, c_name))

        tk.Label(main_card, text=course["description"] or "No description provided", bg="white", fg="#7f8c8d", font=("Arial", 11), wraplength=800, justify="left").pack(anchor="w", pady=(0, 20))

        # 2. Inner Grid (Materi & Tugas)
        grid = tk.Frame(main_card, bg="white")
        grid.pack(fill="x")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        # Materi Column
        mat_frame = tk.Frame(grid, bg="#f1f9ff", padx=15, pady=15, highlightthickness=1, highlightbackground="#d6eaf8")
        mat_frame.grid(row=0, column=0, padx=(0, 10), sticky="nsew") # nsew membuat tinggi sama
        
        tk.Label(mat_frame, text="📘 Materials", bg="#f1f9ff", fg="#3498db", font=("Arial", 11, "bold")).pack(anchor="w")
        if course["materials"]:
            for m in course["materials"]:
                tk.Label(mat_frame, text=f"• {m['title']}", bg="#f1f9ff", fg="#2c3e50", font=("Arial", 10)).pack(anchor="w", pady=2)
        else:
            tk.Label(mat_frame, text="Empty", bg="#f1f9ff", fg="#bdc3c7", font=("Arial", 10, "italic")).pack(anchor="w")

        # Tugas Column
        task_frame = tk.Frame(grid, bg="#fff5eb", padx=15, pady=15, highlightthickness=1, highlightbackground="#fdebd0")
        task_frame.grid(row=0, column=1, padx=(10, 0), sticky="nsew") # nsew membuat tinggi sama
        
        tk.Label(task_frame, text="📝 Assignments", bg="#fff5eb", fg="#e67e22", font=("Arial", 11, "bold")).pack(anchor="w")
        if course["assignments"]:
            for a in course["assignments"]:
                tk.Label(task_frame, text=f"• {a['title']}", bg="#fff5eb", fg="#2c3e50", font=("Arial", 9)).pack(anchor="w")
                tk.Label(task_frame, text=f"  Due: {a['due_date']}", bg="#fff5eb", fg="#e74c3c", font=("Arial", 8)).pack(anchor="w", pady=(0, 4))
        else:
            tk.Label(task_frame, text="Empty", bg="#fff5eb", fg="#bdc3c7", font=("Arial", 10, "italic")).pack(anchor="w")

    def confirm_delete(self, c_id, c_name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{c_name}'?\n\nThis will permanently remove all materials, assignments, files, and student enrollments."):
            success, msg = DashboardDosenController.delete_course(c_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.refresh()
            else:
                messagebox.showerror("Error", msg)

    def refresh(self):
        user = self.controller.current_user
        if not user: return
        self.info_label.config(text=f"Welcome, {user.username} | NIDN: {getattr(user, 'nidn', '-')}")

        for w in self.content.winfo_children():
            w.destroy()

        courses = DashboardDosenController.get_course_detail(getattr(user, 'nidn', user.username))
        if not courses:
            tk.Label(self.content, text="No courses managed yet.", bg="#f8f9fa", fg="#7f8c8d", font=("Arial", 12, "italic")).pack(pady=100)
            return

        for course in courses:
            self.course_card_wrapper(self.content, course)