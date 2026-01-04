import tkinter as tk
from app.controllers.mycourse import MyCourseController


class MyCourseFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f4f7f6")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(self, bg="#f4f7f6")
        header.pack(fill="x", padx=40, pady=(30, 10))

        tk.Label(
            header,
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
        for w in self.course_container.winfo_children():
            w.destroy()

        user = self.controller.current_user
        if not user:
            return

        courses = MyCourseController.get_courses_for_user(user)

        if not courses:
            tk.Label(
                self.course_container,
                text="No courses available",
                bg="#f4f7f6",
                fg="#7f8c8d"
            ).pack(pady=50)
            return

        NUM_COLUMNS = 3
        for i in range(NUM_COLUMNS):
            self.course_container.grid_columnconfigure(i, weight=1)

        for index, course in enumerate(courses):
            row = index // NUM_COLUMNS
            col = index % NUM_COLUMNS
            self.create_card(course, row, col)

    # ================= CARD =================
    def create_card(self, course, r, c):
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

        title = course["course_name"]
        description = course.get("description", "-")

        tk.Label(
            card,
            text=title,
            font=("Helvetica", 13, "bold"),
            bg="white",
            fg="#2d3436",
            wraplength=200,
            justify="left"
        ).pack(anchor="w", fill="x")

        tk.Frame(card, bg="#3498db", height=3, width=40).pack(anchor="w", pady=10)

        tk.Label(
            card,
            text=description,
            font=("Arial", 10),
            bg="white",
            fg="#636e72",
            wraplength=200,
            justify="left"
        ).pack(anchor="w", fill="x", pady=(5, 10))

        open_label = tk.Label(
            card,
            text="Open Course →",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#3498db",
            cursor="hand2"
        )
        open_label.pack(anchor="w")

        # ⬇️ TAMBAHKAN BIND INI
        open_label.bind("<Button-1>", lambda e: self.open_course(course))


    # ================= NAVIGASI =================
    def open_course(self, course):
        self.controller.current_course = course

        role = self.controller.current_user.role
        if role == "dosen":
            self.controller.show_frame("AssignmentDosen")
        else:
            self.controller.show_frame("AssignmentMahasiswa")

    # ================= REFRESH =================
    def refresh(self):
        self.load_courses()
