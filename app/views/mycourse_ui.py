import tkinter as tk
from app.controllers.mycourse import MyCourseController


class MyCourseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f7f6")
        self.controller = controller

        # ================= HEADER =================
        header_frame = tk.Frame(self, bg="#f4f7f6")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))

        tk.Label(
            header_frame,
            text="My Courses",
            font=("Helvetica", 24, "bold"),
            bg="#f4f7f6",
            fg="#2c3e50"
        ).pack(anchor="w")

        # ================= COURSE GRID =================
        self.course_container = tk.Frame(self, bg="#f4f7f6")
        self.course_container.pack(fill="both", expand=True, padx=30, pady=10)

    # ================= LOAD =================
    def load_courses(self):
        # Bersihkan card lama
        for widget in self.course_container.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        if not user:
            return

        # Ambil course sesuai role user
        courses = MyCourseController.get_courses_for_user(user)

        if not courses:
            self.show_empty_state()
            return

        NUM_COLUMNS = 3
        for i in range(NUM_COLUMNS):
            self.course_container.grid_columnconfigure(i, weight=1, uniform="card")

        for index, (name, desc) in enumerate(courses):
            row = index // NUM_COLUMNS
            col = index % NUM_COLUMNS
            self.create_card(name, desc, row, col)

    # ================= EMPTY =================
    def show_empty_state(self):
        tk.Label(
            self.course_container,
            text="Tidak ada course",
            bg="#f4f7f6",
            fg="#95a5a6",
            font=("Arial", 12)
        ).pack(pady=50)

    # ================= CARD =================
    def create_card(self, title, description, r, c):
        card = tk.Frame(
            self.course_container,
            bg="white",
            padx=20,
            pady=20,
            highlightbackground="#e1e8ed",
            highlightthickness=1,
            cursor="hand2"
        )
        card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")

        # klik card
        def on_click(event=None):
            self.open_course(title)

        card.bind("<Button-1>", on_click)

        lbl_title = tk.Label(
            card,
            text=title,
            font=("Helvetica", 13, "bold"),
            bg="white",
            fg="#2d3436",
            wraplength=200,
            justify="left"
        )
        lbl_title.pack(anchor="w", fill="x")
        lbl_title.bind("<Button-1>", on_click)

        tk.Frame(card, bg="#3498db", height=3, width=40).pack(anchor="w", pady=10)

        lbl_desc = tk.Label(
            card,
            text=description or "-",
            font=("Arial", 10),
            bg="white",
            fg="#636e72",
            wraplength=200,
            justify="left"
        )
        lbl_desc.pack(anchor="w", fill="x", pady=(5, 10))
        lbl_desc.bind("<Button-1>", on_click)

        # Tombol teks
        btn = tk.Label(
            card,
            text="Buka Materi →",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#3498db",
            cursor="hand2"
        )
        btn.pack(anchor="w")
        btn.bind("<Button-1>", lambda e: self.open_course(title))

    # ================= NAVIGASI =================
    def open_course(self, course_name):
        # Simpan course aktif
        self.controller.current_course = course_name

        # Pindah ke halaman assignment mahasiswa
        self.controller.show_frame("AssignmentMahasiswaFrame")

    # ================= REFRESH =================
    def refresh(self):
        self.load_courses()
