import tkinter as tk
from app.controllers.dosen.dashboard import DashboardDosenController


class DashboardDosen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(
            self, bg="white", padx=40, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        header.pack(fill="x", padx=20, pady=20)

        tk.Label(
            header, text="DASHBOARD DOSEN",
            bg="white", fg="#2c3e50",
            font=("Helvetica", 24, "bold")
        ).pack()

        self.info_label = tk.Label(
            header, bg="white", fg="#7f8c8d",
            font=("Helvetica", 14)
        )
        self.info_label.pack(pady=5)

        # ================= CONTENT =================
        self.content = tk.Frame(self, bg="#f8f9fa")
        self.content.pack(fill="both", expand=True, padx=20)

    # ================= CARD MATERI =================
    def material_card(self, parent, materials):
        card = tk.Frame(
            parent, bg="white", padx=15, pady=15,
            highlightbackground="#d1d1d1", highlightthickness=1
        )

        tk.Label(
            card, text="📘 Materi",
            bg="white", fg="#3498db",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        if materials:
            for m in materials:
                tk.Label(
                    card,
                    text=f"- {m['title']}",
                    bg="white", fg="#2c3e50",
                    font=("Arial", 10)
                ).pack(anchor="w", pady=1)
        else:
            tk.Label(
                card, text="Belum ada materi",
                bg="white", fg="#7f8c8d",
                font=("Arial", 10)
            ).pack(anchor="w")

        return card

    # ================= CARD TUGAS =================
    def assignment_card(self, parent, assignments):
        card = tk.Frame(
            parent, bg="white", padx=15, pady=15,
            highlightbackground="#d1d1d1", highlightthickness=1
        )

        tk.Label(
            card, text="📝 Tugas",
            bg="white", fg="#e67e22",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        if assignments:
            for a in assignments:
                tk.Label(
                    card,
                    text=f"- {a['title']} (Deadline: {a['due_date']})",
                    bg="white", fg="#2c3e50",
                    font=("Arial", 10)
                ).pack(anchor="w", pady=1)
        else:
            tk.Label(
                card, text="Belum ada tugas",
                bg="white", fg="#7f8c8d",
                font=("Arial", 10)
            ).pack(anchor="w")

        return card

    # ================= COURSE SECTION =================
    def course_section(self, parent, course):
        section = tk.Frame(parent, bg="#f8f9fa")
        section.pack(fill="x", pady=10)

        # --- Course title ---
        tk.Label(
            section,
            text=course["course_name"],
            bg="#f8f9fa", fg="#2c3e50",
            font=("Helvetica", 16, "bold")
        ).pack(anchor="w")

        tk.Label(
            section,
            text=course["description"] or "-",
            bg="#f8f9fa", fg="#7f8c8d",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(0, 5))

        # --- GRID 2 KOLOM ---
        grid = tk.Frame(section, bg="#f8f9fa")
        grid.pack(fill="x")

        material = self.material_card(grid, course["materials"])
        material.grid(row=0, column=0, sticky="nsew", padx=5)

        assignment = self.assignment_card(grid, course["assignments"])
        assignment.grid(row=0, column=1, sticky="nsew", padx=5)

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    # ================= REFRESH =================
    def refresh(self):
        user = self.controller.current_user
        if not user:
            return

        self.info_label.config(text=f"Selamat datang, {user.username}")

        # clear content
        for w in self.content.winfo_children():
            w.destroy()

        courses = DashboardDosenController.get_course_detail(user.nidn)

        if not courses:
            tk.Label(
                self.content,
                text="Belum ada course yang diampu",
                bg="#f8f9fa", fg="#7f8c8d",
                font=("Arial", 12)
            ).pack(pady=40)
            return

        for course in courses:
            self.course_section(self.content, course)
