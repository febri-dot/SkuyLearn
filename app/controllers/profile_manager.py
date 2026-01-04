from app.connection import Database

class ProfileManager:
    @staticmethod
    def get_profile(user):
        """Ambil data profil menggunakan Database() tanpa bergantung pada atribut .cursor"""
        db = Database()
        if not user:
            return None
        try:
            username = user.username if hasattr(user, 'username') else str(user)
            role = user.role.lower() if hasattr(user, 'role') else ""
            user_basic = db.fetch_one(
                "SELECT username, password FROM users WHERE username = ?", 
                (username,)
            )
            if not user_basic: 
                return None
            profile_data = {
                "username": user_basic[0],
                "password": user_basic[1],
                "role": role,
                "detail_list": [] 
            }
            if role == "mahasiswa":
                data = db.fetch_one(
                    "SELECT npm, name, birthday, gender, address, phone_number FROM mahasiswa WHERE npm = ?", 
                    (username,)
                )
                if data:
                    labels = ["NPM", "Full Name", "Birthday", "Gender", "Address", "Phone Number"]
                    for i in range(len(labels)):
                        profile_data["detail_list"].append((labels[i], data[i]))
            elif role == "dosen":
                data = db.fetch_one(
                    "SELECT nidn, name, birthday, gender, address FROM dosen WHERE nidn = ?", 
                    (username,)
                )
                if data:
                    labels = ["NIDN", "Full Name", "Birthday", "Gender", "Address"]
                    for i in range(len(labels)):
                        profile_data["detail_list"].append((labels[i], data[i]))
         
            elif role == "admin":
                profile_data["detail_list"].append(("Status", "Administrator System"))
                profile_data["detail_list"].append(("Access", "Full Access"))
            return profile_data
        except Exception as e:
            print(f"Error logic ProfileManager: {e}")
            return None