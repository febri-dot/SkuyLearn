import tkinter as tk
from app.controllers.profile_manager import ProfileManager

class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#ffffff")
        self.controller = controller

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        user = self.controller.current_user
        profile = ProfileManager.get_profile(user)
        
        if not profile:
            return

        # --- 1. HEADER (Rata Tengah) ---
        header = tk.Frame(self, bg="#ffffff")
        header.pack(pady=(40, 10), fill="x")
        
        tk.Label(header, text="PROFILE", font=("Helvetica", 12, "bold"), 
                 bg="#ffffff", fg="#bdc3c7").pack(anchor="center")

        # --- 2. PROFILE SECTION (Fokus di Tengah) ---
        profile_area = tk.Frame(self, bg="#ffffff")
        profile_area.pack(pady=(0, 30), fill="x")

        # Username Besar di Tengah
        tk.Label(profile_area, text=profile['username'], font=("Helvetica", 24, "bold"), 
                 bg="#ffffff", fg="#2c3e50").pack(anchor="center")
        
        # Sub-info (Role & Password) Sejajar di Tengah
        sub_info = tk.Frame(profile_area, bg="#ffffff")
        sub_info.pack(anchor="center")

        role_text = profile.get('role', 'User').upper()
        tk.Label(sub_info, text=role_text, font=("Arial", 8, "bold"), 
                 bg="#34495e", fg="white", padx=10, pady=2).pack(side="left", padx=5)
        
        tk.Label(sub_info, text=f"Password: ••••••••", font=("Arial", 10), 
                 bg="#ffffff", fg="#95a5a6").pack(side="left", padx=5)

        # --- 3. LIST DETAIL SECTION (Rata Kiri) ---
        # Gunakan padding kiri (padx) yang cukup besar agar tidak terlalu nempel ke pinggir
        detail_wrapper = tk.Frame(self, bg="#ffffff", padx=100)
        detail_wrapper.pack(fill="both", expand=True)

        # Separator halus
        tk.Frame(detail_wrapper, bg="#f1f2f6", height=1).pack(fill="x", pady=(0, 25))

        # Judul List Detail (Kecil di Kiri)
        tk.Label(detail_wrapper, text="List Detail", font=("Helvetica", 9, "bold"), 
                 bg="#ffffff", fg="#34495e").pack(anchor="w", pady=(0, 15))

        # Render semua data dari list dengan perataan kiri dan font BESAR
        for label, value in profile["detail_list"]:
            row = tk.Frame(detail_wrapper, bg="#ffffff")
            row.pack(fill="x", pady=10) 

            # Aksen Garis Vertikal Navy (Tebal 4px)
            tk.Frame(row, bg="#34495e", width=4).pack(side="left", fill="y")

            txt_box = tk.Frame(row, bg="#ffffff", padx=20)
            txt_box.pack(side="left", fill="both")

            # Judul Field (Size 9)
            tk.Label(txt_box, text=label.upper(), font=("Helvetica", 9, "bold"), 
                     bg="#ffffff", fg="#bdc3c7").pack(anchor="w")
            
            # ISI DATA UTAMA (Size 14 Bold)
            val_text = str(value) if value else "-"
            tk.Label(txt_box, text=val_text, font=("Helvetica", 14, "bold"), 
                     bg="#ffffff", fg="#2c3e50").pack(anchor="w")
    