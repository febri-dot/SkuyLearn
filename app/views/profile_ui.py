# app/views/profile_ui.py
import tkinter as tk
from tkinter import messagebox, ttk
from app.controllers.profile_manager import ProfileManager

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f8f9fa")
        self.controller = controller
        self.edit_mode = False
        self.entries = {}

        # ================= SCROLLABLE SETUP =================
        self.canvas = tk.Canvas(self, bg="#f8f9fa", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f9fa")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def refresh(self):
        self.edit_mode = False
        self.render_ui()

    def render_ui(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        profile = ProfileManager.get_profile(user)
        if not profile: return

        # ================= HEADER =================
        header = tk.Frame(self.scrollable_frame, bg="white", padx=40, pady=20, highlightthickness=1, highlightbackground="#d1d1d1")
        header.pack(fill="x", padx=20, pady=20)

        tk.Label(header, text="MY PROFILE", bg="white", fg="#2c3e50", font=("Helvetica", 20, "bold")).pack(side="left")

        btn_frame = tk.Frame(header, bg="white")
        btn_frame.pack(side="right")

        if not self.edit_mode:
            tk.Button(btn_frame, text="✎ Edit Profile", bg="#3498db", fg="white", font=("Arial", 9, "bold"),
                      padx=15, pady=8, relief="flat", command=self.toggle_edit).pack()
        else:
            tk.Button(btn_frame, text="Cancel", bg="#95a5a6", fg="white", font=("Arial", 9, "bold"),
                      padx=10, pady=5, relief="flat", command=self.toggle_edit).pack(side="right", padx=5)
            tk.Button(btn_frame, text="💾 Save", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"),
                      padx=10, pady=5, relief="flat", command=self.save_profile).pack(side="right")

        # ================= CONTENT CARD =================
        main_card = tk.Frame(self.scrollable_frame, bg="white", padx=40, pady=30, highlightthickness=1, highlightbackground="#e1e8ed")
        main_card.pack(pady=10, padx=20, fill="x")

        # Badge Role
        tk.Label(main_card, text=profile.get('role', '').upper(), font=("Arial", 8, "bold"), 
                 bg="#34495e", fg="white", padx=10).pack()
        
        # Display Name
        display_name = profile['username']
        for label, val, key in profile.get("detail_list", []):
            if key == 'name': display_name = val

        tk.Label(main_card, text=display_name, font=("Helvetica", 22, "bold"), bg="white", fg="#2c3e50").pack(pady=10)
        tk.Frame(main_card, bg="#f1f2f6", height=1).pack(fill="x", pady=20)

        # ================= FIELDS =================
        self.entries = {}
        
        # Username & Password
        self.create_info_row(main_card, "Username", profile['username'], 'username', can_edit=False)
        self.create_info_row(main_card, "Password", "********", 'password', can_edit=True)

        # Render Detail List (NPM/NIDN, Nama, Alamat, dll)
        for label, value, key in profile.get("detail_list", []):
            # Proteksi: NPM dan NIDN tidak boleh diedit
            is_id_field = key in ['npm', 'nidn']
            self.create_info_row(main_card, label, value, key, can_edit=not is_id_field)

    def create_info_row(self, parent, label, value, key, can_edit=True):
        row = tk.Frame(parent, bg="white", pady=10)
        row.pack(fill="x")

        tk.Label(row, text=label.upper(), font=("Helvetica", 8, "bold"), bg="white", fg="#bdc3c7", width=15, anchor="w").pack(side="left")

        if self.edit_mode and can_edit:
            entry = tk.Entry(row, font=("Helvetica", 11), bg="#f8f9fa", relief="flat", highlightthickness=1, highlightbackground="#d1d1d1")
            entry.pack(side="left", fill="x", expand=True, padx=(20, 0), ipady=4)
            
            if key == 'password':
                entry.insert(0, "")
            else:
                entry.insert(0, str(value) if value is not None else "")
            
            self.entries[key] = entry
        else:
            val_display = str(value) if value else "-"
            tk.Label(row, text=val_display, font=("Helvetica", 11, "bold"), bg="white", fg="#2c3e50").pack(side="left", padx=(20, 0))
            
            # Simpan variabel StringVar agar data read-only tetap terkirim saat save
            var = tk.StringVar(value=str(value) if value is not None else "")
            self.entries[key] = var

    def toggle_edit(self):
        self.edit_mode = not self.edit_mode
        self.render_ui()

    def save_profile(self):
        updated_data = {}
        for key, widget in self.entries.items():
            val = widget.get().strip() if hasattr(widget, 'get') else ""
            updated_data[key] = val

        # SINKRONISASI KEY UNTUK CONTROLLER
        # Memastikan spasi dan nama field sesuai dengan yang diminta ProfileManager
        if 'name' in updated_data:
            updated_data['full name'] = updated_data['name']
        
        # Menangani sinkronisasi spasi untuk phone number agar tidak terhapus
        if 'phone_number' in updated_data:
            updated_data['phone number'] = updated_data['phone_number']

        user = self.controller.current_user
        success, msg = ProfileManager.update_profile(user, updated_data)
        
        if success:
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.edit_mode = False
            self.render_ui()
        else:
            messagebox.showerror("Update Error", msg)