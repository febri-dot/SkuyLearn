import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from app.controllers.dosen.coursedosen import CourseDosenController

class CourseDosenFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # --- HEADER ---
        header = tk.Frame(self, bg="white", padx=25, pady=20, highlightthickness=1, highlightbackground="#dee2e6")
        header.pack(fill="x", padx=20, pady=20)

        self.lbl_course_name = tk.Label(header, text="COURSE NAME", font=("Helvetica", 20, "bold"), bg="white", fg="#2c3e50")
        self.lbl_course_name.pack(side="left")

        btn_frame = tk.Frame(header, bg="white")
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="Add Assignment", bg="#3498db", fg="white", font=("Arial", 10, "bold"), 
                  relief="flat", padx=12, pady=5, command=lambda: controller.show_frame("AssignmentDosen")).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Add Material", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), 
                  relief="flat", padx=12, pady=5, command=self.open_add_material_popup).pack(side="left", padx=5)
                    
        # --- SCROLLABLE AREA ---
        content_wrapper = tk.Frame(self, bg="#f8f9fa")
        content_wrapper.pack(fill="both", expand=True, padx=30)

        self.canvas = tk.Canvas(content_wrapper, bg="#f8f9fa", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(content_wrapper, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f9fa")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # --- FOOTER (BACK BUTTON) ---
        footer = tk.Frame(self, bg="#f8f9fa", pady=15)
        footer.pack(fill="x", side="bottom")

        tk.Button(footer, text="BACK", bg="#34495e", fg="white", font=("Arial", 9, "bold"), 
                  relief="flat", padx=20, pady=6, cursor="hand2",
                  command=lambda: controller.show_frame("MyCourseFrame")).pack(anchor="center")

    def refresh(self):
        """Memuat ulang data materi & tugas"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        course = self.controller.current_course
        if not course: return

        c_id = course.get('id') if isinstance(course, dict) else course[0]
        c_name = course.get('course_name') if isinstance(course, dict) else course[1]
        self.lbl_course_name.config(text=c_name.upper())
        
        # Load Data
        materials = CourseDosenController.get_materials_by_course(c_id)
        assignments = CourseDosenController.get_assignments_by_course(c_id)

        # Bagian MATERIALS
        tk.Label(self.scrollable_frame, text="MATERIALS", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(10,5))
        if not materials:
            tk.Label(self.scrollable_frame, text="Belum ada materi.", font=("Arial", 10, "italic"), bg="#f8f9fa", fg="gray").pack(anchor="w", padx=20)
        else:
            for m in materials:
                self.create_card(m, is_material=True)

        # Bagian ASSIGNMENTS
        tk.Label(self.scrollable_frame, text="ASSIGNMENTS", font=("Arial", 12, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w", pady=(20,5))
        if not assignments:
            tk.Label(self.scrollable_frame, text="Belum ada tugas.", font=("Arial", 10, "italic"), bg="#f8f9fa", fg="gray").pack(anchor="w", padx=20)
        else:
            for a in assignments:
                self.create_card(a, is_material=False)

    def create_card(self, item, is_material=True):
        """Kartu visual dengan tombol Delete untuk materi maupun tugas"""
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid", padx=20, pady=15)
        card.pack(fill="x", pady=5)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x")
        
        icon = "📄 " if is_material else "📝 "
        tk.Label(top, text=f"{icon}{item['title']}", font=("Helvetica", 12, "bold"), bg="white", fg="#2d3436").pack(side="left")
        
        # Tombol Delete (Berfungsi untuk Materi maupun Tugas)
        delete_cmd = (lambda: self.on_delete_material(item['id'])) if is_material else (lambda: self.on_delete_assignment(item['id']))
        tk.Button(top, text="Delete", bg="#e74c3c", fg="white", font=("Arial", 8), 
                  relief="flat", padx=8, command=delete_cmd).pack(side="right")

        # Deskripsi
        tk.Label(card, text=item.get('description', ''), font=("Arial", 10), bg="white", fg="#636e72", 
                 wraplength=600, justify="left").pack(anchor="w", pady=5)

        # Info Tambahan
        if is_material:
            tk.Label(card, text=f"File: {item.get('file', '-')}", font=("Arial", 9, "bold"), bg="white", fg="#3498db").pack(anchor="w")
        else:
            tk.Label(card, text=f"Due: {item.get('due_date', '-')}", font=("Arial", 9, "italic"), bg="white", fg="#e67e22").pack(anchor="w")

    def on_delete_material(self, m_id):
        if messagebox.askyesno("Confirm", "Hapus materi ini?"):
            if CourseDosenController.delete_material(m_id):
                self.refresh()

    def on_delete_assignment(self, a_id):
        if messagebox.askyesno("Confirm", "Hapus tugas ini?"):
            if CourseDosenController.delete_assignment(a_id):
                self.refresh()

    def open_add_material_popup(self):
        pass # Navigasi ke form tambah materi