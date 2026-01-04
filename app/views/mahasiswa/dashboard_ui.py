import tkinter as tk
from app.controllers.mahasiswa.dashboard import DashboardMahasiswaController


class DashboardMahasiswa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        self.header_card = tk.Frame(
            self, bg="white", padx=40, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        self.header_card.pack(fill="x", padx=20, pady=20)

        tk.Label(
            self.header_card,
            text="DASHBOARD MAHASISWA",
            bg="white", fg="#2c3e50",
            font=("Helvetica", 24, "bold")
        ).pack()

        self.info_label = tk.Label(
            self.header_card, text="",
            bg="white", fg="#7f8c8d",
            font=("Helvetica", 14)
        )
        self.info_label.pack(pady=5)

        # ================= STAT CARDS =================
        self.stat_container = tk.Frame(self, bg="#f8f9fa")
        self.stat_container.pack(fill="x", padx=20)

        self.material_card = self.create_stat_card(
            self.stat_container, "TOTAL MATERI", "#3498db"
        )
        self.material_card.pack(side="left", expand=True, fill="x", padx=5)

        self.assignment_card = self.create_stat_card(
            self.stat_container, "TOTAL TUGAS", "#e67e22"
        )
        self.assignment_card.pack(side="left", expand=True, fill="x", padx=5)

        # ================= MATERI =================
        self.material_container = self.create_section("Materi Perkuliahan")

        # ================= ASSIGNMENT =================
        self.assignment_container = self.create_section("Tugas / Assignment")

    # ================= HELPER UI =================
    def create_stat_card(self, parent, title, color):
        card = tk.Frame(
            parent, bg="white", padx=20, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )

        tk.Label(
            card, text=title,
            bg="white", fg="#7f8c8d",
            font=("Arial", 10, "bold")
        ).pack()

        label = tk.Label(
            card, text="0",
            bg="white", fg=color,
            font=("Helvetica", 32, "bold")
        )
        label.pack()

        card.count_label = label
        return card

    def create_section(self, title):
        wrapper = tk.Frame(self, bg="#f8f9fa")
        wrapper.pack(fill="x", padx=20, pady=10)

        tk.Label(
            wrapper, text=title,
            bg="#f8f9fa", fg="#2c3e50",
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w", pady=5)

        container = tk.Frame(wrapper, bg="#f8f9fa")
        container.pack(fill="x")

        return container

    def create_list_card(self, parent, title, subtitle, info):
        card = tk.Frame(
            parent, bg="white", padx=15, pady=15,
            highlightbackground="#d1d1d1", highlightthickness=1
        )

        tk.Label(
            card, text=title,
            bg="white", fg="#2c3e50",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            card, text=subtitle,
            bg="white", fg="#7f8c8d",
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            card, text=info,
            bg="white", fg="#3498db",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=5)

        return card

    def render_cards_grid(self, container, data_list, create_card_fn):
        """Render card 3 kolom ke samping"""
        for widget in container.winfo_children():
            widget.destroy()

        columns = 3
        for i, data in enumerate(data_list):
            row = i // columns
            col = i % columns

            card = create_card_fn(container, data)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        for c in range(columns):
            container.grid_columnconfigure(c, weight=1)

    # ================= REFRESH =================
    def refresh(self):
        user = self.controller.current_user
        if not user:
            return

        npm = user.username
        self.info_label.config(text=f"Selamat datang, {user.username}")

        # -------- STATS --------
        stats = DashboardMahasiswaController.get_stats(npm)
        self.material_card.count_label.config(
            text=str(stats["total_materials"])
        )
        self.assignment_card.count_label.config(
            text=str(stats["total_assignments"])
        )

        # -------- MATERI --------
        materials = DashboardMahasiswaController.get_materials(npm)
        if not materials:
            tk.Label(
                self.material_container,
                text="Belum ada materi",
                bg="#f8f9fa", fg="#7f8c8d"
            ).pack(pady=10)
        else:
            self.render_cards_grid(
                self.material_container,
                materials,
                lambda parent, m: self.create_list_card(
                    parent,
                    m["title"],
                    m["course_name"],
                    f"📅 {m['uploaded_at']}"
                )
            )

        # -------- ASSIGNMENT --------
        assignments = DashboardMahasiswaController.get_assignments(npm)
        if not assignments:
            tk.Label(
                self.assignment_container,
                text="Belum ada tugas",
                bg="#f8f9fa", fg="#7f8c8d"
            ).pack(pady=10)
        else:
            self.render_cards_grid(
                self.assignment_container,
                assignments,
                lambda parent, a: self.create_list_card(
                    parent,
                    a["title"],
                    a["course_name"],
                    f"⏰ Deadline: {a['due_date']}"
                )
            )
