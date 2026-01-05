import tkinter as tk
from tkinter import messagebox, filedialog
from app.controllers.dosen.course_material import CourseMaterialController


class CourseMaterial(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller

        # ================= HEADER =================
        header = tk.Frame(
            self, bg="white", padx=30, pady=20,
            highlightbackground="#d1d1d1", highlightthickness=1
        )
        header.pack(fill="x", padx=20, pady=20)
        header.grid_columnconfigure(0, weight=1)

        self.title_label = tk.Label(
            header,
            text="COURSE MATERIALS",
            bg="white",
            fg="#2c3e50",
            font=("Helvetica", 18, "bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        tk.Button(
            header,
            text="← Back to Courses",
            bg="#e74c3c",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=lambda: controller.show_frame("MyCourseFrame")
        ).grid(row=0, column=1, sticky="e")

        # ================= FORM TAMBAH MATERI =================
        form = tk.Frame(
            self, bg="white", padx=25, pady=20,
            highlightthickness=1, highlightbackground="#e1e8ed"
        )
        form.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(
            form, text="Add Course Material",
            bg="white", fg="#34495e",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 15))

        self.title_entry = self._input(form, "Material Title")
        self.content_entry = self._input(form, "Description / Notes")

        tk.Button(
            form,
            text="+ Upload Material",
            bg="#2ecc71",
            fg="white",
            relief="flat",
            cursor="hand2",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            command=self.add_material
        ).pack(anchor="w")

        # ================= LIST MATERI =================
        tk.Label(
            self,
            text="Existing Materials",
            bg="#f8f9fa",
            fg="#34495e",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", padx=45, pady=(15, 5))

        self.content = tk.Frame(self, bg="#f8f9fa")
        self.content.pack(fill="both", expand=True, padx=40)

    # ================= INPUT =================
    def _input(self, parent, label):
        tk.Label(
            parent, text=label,
            bg="white", fg="#7f8c8d",
            font=("Arial", 9)
        ).pack(anchor="w")

        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            bg="#f1f3f5",
            relief="flat"
        )
        entry.pack(fill="x", pady=(3, 10), ipady=5)
        return entry

    # ================= TAMBAH MATERI =================
    def add_material(self):
        course = self.controller.current_course
        if not course:
            messagebox.showerror("Error", "No course selected")
            return

        title = self.title_entry.get().strip()
        content = self.content_entry.get().strip()

        if not title:
            messagebox.showwarning("Warning", "Material title is required")
            return

        success = CourseMaterialController.create_material(
            course_id=course[0],  # course tuple → id di index 0
            title=title,
            content=content,
            content_path=None
        )

        if success:
            messagebox.showinfo("Success", "Material added successfully")
            self.title_entry.delete(0, tk.END)
            self.content_entry.delete(0, tk.END)
            self.refresh()
        else:
            messagebox.showerror("Error", "Failed to add material")

    # ================= REFRESH =================
    def refresh(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        course = self.controller.current_course
        if not course:
            return

        self.title_label.config(text=f"MATERIALS: {course[1]}")

        materials = CourseMaterialController.get_materials_by_course(course[0])

        if not materials:
            tk.Label(
                self.content,
                text="No materials uploaded yet.",
                bg="#f8f9fa",
                fg="#7f8c8d",
                font=("Arial", 11, "italic")
            ).pack(pady=40)
            return

        for m in materials:
            self._material_card(m)

    # ================= CARD MATERI =================
    def _material_card(self, material):
        card = tk.Frame(
            self.content,
            bg="white",
            padx=20,
            pady=15,
            highlightbackground="#e1e8ed",
            highlightthickness=1
        )
        card.pack(fill="x", pady=6)

        tk.Label(
            card,
            text=material["title"],
            bg="white",
            fg="#2c3e50",
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        if material["content"]:
            tk.Label(
                card,
                text=material["content"],
                bg="white",
                fg="#636e72",
                font=("Arial", 10),
                wraplength=800,
                justify="left"
            ).pack(anchor="w", pady=(5, 5))

        tk.Label(
            card,
            text=f"Uploaded at: {material['uploaded_at']}",
            bg="white",
            fg="#b2bec3",
            font=("Arial", 8, "italic")
        ).pack(anchor="w")
