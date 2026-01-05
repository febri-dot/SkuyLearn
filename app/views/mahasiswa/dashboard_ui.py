# app/views/mahasiswa/dashboard_ui.py
import tkinter as tk
from app.controllers.mahasiswa.dashboard import DashboardMahasiswaController

class DashboardMahasiswa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        self.header_card = tk.Frame(
            self, bg="white", padx=40, pady=25,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        self.header_card.pack(fill="x", padx=20, pady=20)

        tk.Label(
            self.header_card, text="STUDENT DASHBOARD",
            bg="white", fg="#2c3e50", font=("Helvetica", 24, "bold")
        ).pack(anchor="w")

        self.info_label = tk.Label(
            self.header_card, text="",
            bg="white", fg="#7f8c8d", font=("Helvetica", 13)
        )
        self.info_label.pack(anchor="w", pady=(5, 0))

        # ================= SCROLLABLE CONTENT =================
        self.main_container = tk.Frame(self, bg="#f8f9fa")
        self.main_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_container, bg="#f8f9fa", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f9fa")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # ================= STAT CARDS =================
        self.stat_container = tk.Frame(self.scrollable_frame, bg="#f8f9fa")
        self.stat_container.pack(fill="x", padx=20, pady=10)

        self.material_card = self.create_stat_card(
            self.stat_container, "📘 TOTAL MATERIALS", "#3498db"
        )
        self.material_card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        self.assignment_card = self.create_stat_card(
            self.stat_container, "📝 TOTAL ASSIGNMENTS", "#e67e22"
        )
        self.assignment_card.grid(row=0, column=1, padx=10, sticky="nsew")
        
        # Placeholder kolom 3 agar seimbang
        tk.Frame(self.stat_container, bg="#f8f9fa").grid(row=0, column=2, padx=10, sticky="nsew")
        
        self.stat_container.columnconfigure((0, 1, 2), weight=1)

        # ================= SECTIONS =================
        self.material_container = self.create_section("Recent Materials")
        self.assignment_container = self.create_section("Upcoming Assignments")

    # ================= HELPER UI =================
    def create_stat_card(self, parent, title, color):
        card = tk.Frame(
            parent, bg="white", padx=25, pady=30, # Tambah pady agar lebih tinggi
            highlightbackground="#e1e8ed", highlightthickness=1
        )

        # Title di tengah
        tk.Label(
            card, text=title, bg="white", fg="#7f8c8d",
            font=("Arial", 9, "bold")
        ).pack(expand=True) # expand=True membantu pemusatan vertikal/horizontal

        # Angka di tengah
        label = tk.Label(
            card, text="0", bg="white", fg=color,
            font=("Helvetica", 42, "bold") # Ukuran sedikit diperbesar agar mantap
        )
        label.pack(expand=True)

        card.count_label = label
        return card

    def create_section(self, title):
        wrapper = tk.Frame(self.scrollable_frame, bg="#f8f9fa", padx=20, pady=15)
        wrapper.pack(fill="x")

        # Garis aksen judul
        title_frame = tk.Frame(wrapper, bg="#f8f9fa")
        title_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(
            title_frame, text=title.upper(), bg="#f8f9fa", fg="#2c3e50",
            font=("Helvetica", 13, "bold")
        ).pack(side="left")
        
        tk.Frame(title_frame, bg="#d1d1d1", height=2).pack(side="left", fill="x", expand=True, padx=15)

        container = tk.Frame(wrapper, bg="#f8f9fa")
        container.pack(fill="x")
        return container

    def create_list_card(self, parent, title, subtitle, info, type_color):
        card = tk.Frame(
            parent, bg="white", padx=15, pady=20,
            highlightbackground="#e1e8ed", highlightthickness=1
        )
        
        # Aksen warna sekarang di ATAS, bukan di samping (agar simetri tengah)
        tk.Frame(card, bg=type_color, height=4).pack(side="top", fill="x", pady=(0, 15))
        
        text_container = tk.Frame(card, bg="white")
        text_container.pack(fill="both", expand=True)

        # Judul rata tengah
        tk.Label(
            text_container, text=title, bg="white", fg="#2c3e50",
            font=("Arial", 11, "bold"), wraplength=200, justify="center"
        ).pack(anchor="center")

        # Nama Course rata tengah
        tk.Label(
            text_container, text=subtitle, bg="white", fg="#3498db",
            font=("Arial", 9, "bold"), justify="center"
        ).pack(anchor="center", pady=(5, 0))

        # Info (Date/Deadline) rata tengah
        tk.Label(
            text_container, text=info, bg="white", fg="#95a5a6",
            font=("Arial", 9, "italic"), justify="center"
        ).pack(anchor="center", pady=(12, 0))

        return card

    def render_cards_grid(self, container, data_list, type_color, is_assignment=False):
        for widget in container.winfo_children():
            widget.destroy()

        if not data_list:
            tk.Label(container, text="No items to display.", bg="#f8f9fa", 
                    fg="#95a5a6", font=("Arial", 10, "italic")).pack(pady=20)
            return

        columns = 3
        for i, data in enumerate(data_list):
            row = i // columns
            col = i % columns

            info_text = f"⏰ Due: {data['due_date']}" if is_assignment else f"📅 Posted: {data['uploaded_at']}"
            
            card = self.create_list_card(
                container, 
                data["title"], 
                data["course_name"], 
                info_text,
                type_color
            )
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for c in range(columns):
            container.grid_columnconfigure(c, weight=1)

    # ================= REFRESH =================
    def refresh(self):
        user = self.controller.current_user
        if not user: return

        npm = user.username
        self.info_label.config(text=f"Welcome back, {user.username}! Let's continue your studies.")

        # -------- STATS --------
        stats = DashboardMahasiswaController.get_stats(npm)
        self.material_card.count_label.config(text=str(stats["total_materials"]))
        self.assignment_card.count_label.config(text=str(stats["total_assignments"]))

        # -------- MATERI --------
        materials = DashboardMahasiswaController.get_materials(npm)
        self.render_cards_grid(self.material_container, materials, "#3498db")

        # -------- ASSIGNMENT --------
        assignments = DashboardMahasiswaController.get_assignments(npm)
        self.render_cards_grid(self.assignment_container, assignments, "#e67e22", is_assignment=True)