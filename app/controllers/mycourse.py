from app.connection import Database

class MyCourseController:
    @staticmethod
    def get_courses_for_user(user):
        """
        Fetch courses based on user role (Mahasiswa, Dosen, or Admin).
        """
        db = Database()

        # ================= MAHASISWA =================
        if user.role == "mahasiswa":
            query = """
                SELECT c.id, c.course_name, c.description, c.enrollment_key, d.name
                FROM courses c
                JOIN enrollment_class e ON e.course_id = c.id
                JOIN dosen d ON c.owner = d.nidn
                WHERE e.npm = ?
            """
            return db.fetch_all(query, (user.npm,))

        # ================= DOSEN =================
        elif user.role == "dosen":
            query = """
                SELECT c.id, c.course_name, c.description, c.enrollment_key, c.owner, d.name
                FROM courses c
                JOIN dosen d ON c.owner = d.nidn
                WHERE c.owner = ?
            """
            return db.fetch_all(query, (user.nidn,))

        # ================= ADMIN (NEW: Get All) =================
        elif user.role == "admin":
            query = """
                SELECT c.id, c.course_name, c.description, c.enrollment_key, c.owner, d.name
                FROM courses c
                LEFT JOIN dosen d ON c.owner = d.nidn
            """
            return db.fetch_all(query)

        return []

    @staticmethod
    def get_next_id():
        db = Database()
        # Mengambil angka ID terakhir dari tabel courses
        result = db.fetch_all("SELECT id FROM courses ORDER BY id DESC LIMIT 1")
        if result:
            last_id = int(result[0][0])
            return last_id + 1
        return 1 # Jika tabel kosong, mulai dari 1


    @staticmethod
    def save_course(data, is_edit=False):
        db = Database()
        if is_edit:
            query = "UPDATE courses SET course_name=?, description=?, enrollment_key=?, owner=? WHERE id=?"
            params = (data['name'], data['desc'], data['code'], data['owner'], data['id'])
        else:
            query = "INSERT INTO courses (id, course_name, description, enrollment_key, owner) VALUES (?, ?, ?, ?, ?)"
            params = (data['id'], data['name'], data['desc'], data['code'], data['owner'])
        
        try:
            db.execute_query(query, params)
            return True, "Course saved successfully!"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def delete_course(course_id):
        """Logic for Admin to Delete a course."""
        db = Database()
        try:
            db.execute_query("DELETE FROM courses WHERE id = ?", (course_id,))
            return True, "Course deleted successfully!"
        except Exception as e:
            return False, str(e)