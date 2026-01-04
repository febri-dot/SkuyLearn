import tkinter as tk
import sqlite3
import os

# Path database disesuaikan agar fleksibel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "../../skuylearn.db")

def fetch_courses():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT course_name, description FROM courses")
        data = cur.fetchall()
        conn.close()
        return data
    except sqlite3.Error as e:
        print(f"Error Database: {e}")
        return []

class MahasiswaMyCourseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f7f6")
        self.controller = controller

        # Header Section
        header_frame = tk.Frame(self, bg="#f4f7f6")
        header_frame.pack(fill="x", padx=40, pady=(30, 10))

        tk.Label(
            header_frame,
            text="My Courses",
            font=("Helvetica", 24, "bold"),
            bg="#f4f7f6",
            fg="#2c3e50"
        ).pack(anchor="w")

        # Container untuk Grid Card
        self.course_container = tk.Frame(self, bg="#f4f7f6")
        self.course_container.pack(fill="both", expand=True, padx=30, pady=10)

        self.load_courses()

    def load_courses(self):
        for widget in self.course_container.winfo_children():
            widget.destroy()

        courses = fetch_courses()
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

    def show_empty_state(self):
        tk.Label(self.course_container, text="Tidak ada kursus tersedia", bg="#f4f7f6", fg="#95a5a6").pack(pady=50)

    def create_card(self, title, description, r, c):
        # Frame Card Utama
        card = tk.Frame(
            self.course_container,
            bg="white",
            padx=20,
            pady=20,
            highlightbackground="#e1e8ed",
            highlightthickness=1,
            cursor="hand2" # Mengubah kursor menjadi tangan saat hover
        )
        card.grid(row=r, column=c, padx=12, pady=12, sticky="nsew")

        # Fungsi yang akan dipanggil saat card diklik
        def on_click(event=None):
            self.open_course(title)

        # Binding Klik ke Frame Card
        card.bind("<Button-1>", on_click)

        # Isi Card
        lbl_title = tk.Label(
            card, text=title, font=("Helvetica", 13, "bold"),
            bg="white", fg="#2d3436", wraplength=200, justify="left"
        )
        lbl_title.pack(anchor="w", fill="x")
        lbl_title.bind("<Button-1>", on_click) # Bind agar teks juga bisa diklik

        tk.Frame(card, bg="#3498db", height=3, width=40).pack(anchor="w", pady=10)

        lbl_desc = tk.Label(
            card, text=description, font=("Arial", 10),
            bg="white", fg="#636e72", wraplength=200, justify="left"
        )
        lbl_desc.pack(anchor="w", fill="x", pady=(5, 10))
        lbl_desc.bind("<Button-1>", on_click) # Bind teks deskripsi

        tk.Label(
            card, text="Buka Materi →", font=("Arial", 9, "bold"),
            bg="white", fg="#3498db"
        ).pack(anchor="w")

    def open_course(self, course_name):
        """Logika untuk membuka course"""
        print(f"Membuka materi untuk: {course_name}")
        
        # Contoh navigasi ke frame lain (Pastikan CourseDetailFrame sudah terdaftar di SkuylearnApp)
        # self.controller.current_course = course_name # Simpan kursus yang dipilih
        # self.controller.show_frame("CourseDetailFrame")
        
        # Sementara kita gunakan messagebox untuk tes
        from tkinter import messagebox
        messagebox.showinfo("Course Access", f"Anda sedang membuka materi: {course_name}")

    def refresh(self):
        self.load_courses()