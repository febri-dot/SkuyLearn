# app/controllers/profile_manager.py
from app.connection import Database

class ProfileManager:
    @staticmethod
    def get_profile(user):
        """Ambil data profil lengkap berdasarkan role"""
        db = Database()
        if not user: return None
        try:
            username = user.username if hasattr(user, 'username') else str(user)
            role = user.role.lower() if hasattr(user, 'role') else ""
            
            user_basic = db.fetch_one(
                "SELECT username, password FROM users WHERE username = ?", 
                (username,)
            )
            if not user_basic: return None

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
                    # Menggunakan key underscore agar konsisten dan aman (tanpa spasi)
                    keys = ["npm", "name", "birthday", "gender", "address", "phone_number"]
                    for i in range(len(labels)):
                        profile_data["detail_list"].append((labels[i], data[i], keys[i]))

            elif role == "dosen":
                data = db.fetch_one(
                    "SELECT nidn, name, birthday, gender, address FROM dosen WHERE nidn = ?", 
                    (username,)
                )
                if data:
                    labels = ["NIDN", "Full Name", "Birthday", "Gender", "Address"]
                    keys = ["nidn", "name", "birthday", "gender", "address"]
                    for i in range(len(labels)):
                        profile_data["detail_list"].append((labels[i], data[i], keys[i]))

            return profile_data
        except Exception as e:
            print(f"Error get_profile: {e}")
            return None

    @staticmethod
    def update_profile(user, updated_data):
        """Update data ke tabel users dan tabel detail (mahasiswa/dosen)"""
        db = Database()
        role = user.role.lower()
        old_username = user.username

        try:
            # 1. Ambil data dasar
            new_username = updated_data.get('username')
            new_password = updated_data.get('password')

            # 2. Update Tabel USERS
            if new_password and new_password.strip() != "" and new_password != "********":
                db.execute_query(
                    "UPDATE users SET username = ?, password = ? WHERE username = ?",
                    (new_username, new_password, old_username)
                )
            else:
                db.execute_query(
                    "UPDATE users SET username = ? WHERE username = ?",
                    (new_username, old_username)
                )

            # 3. Update Tabel Detail (Menggunakan data dari updated_data)
            # Tips: .get('key') akan mengambil data berdasarkan key yang kita set di UI
            if role == "mahasiswa":
                db.execute_query(
                    """UPDATE mahasiswa SET 
                        name = ?, birthday = ?, gender = ?, address = ?, phone_number = ? 
                        WHERE npm = ?""",
                    (updated_data.get('name') or updated_data.get('full name'), 
                        updated_data.get('birthday'),
                        updated_data.get('gender'), 
                        updated_data.get('address'), 
                        updated_data.get('phone_number') or updated_data.get('phone number'), 
                        old_username)
                )

            elif role == "dosen":
                db.execute_query(
                    """UPDATE dosen SET 
                        name = ?, birthday = ?, gender = ?, address = ? 
                        WHERE nidn = ?""",
                    (updated_data.get('name') or updated_data.get('full name'), 
                        updated_data.get('birthday'),
                        updated_data.get('gender'), 
                        updated_data.get('address'), 
                        old_username)
                )

            # 4. Update Session di Python agar tetap sinkron
            user.username = new_username
            
            return True, "Profile updated successfully!"

        except Exception as e:
            print(f"Update Error logic: {e}")
            return False, f"Database Error: {str(e)}"