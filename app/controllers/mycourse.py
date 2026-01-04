from app.connection import Database

class MyCourseController:

    @staticmethod
    def get_courses_for_user(user):
        db = Database()

        # ================= MAHASISWA =================
        if user.role == "mahasiswa":
            query = """
            SELECT c.course_name, c.description
            FROM courses c
            JOIN enrollment_class e ON e.course_id = c.id
            WHERE e.npm = ?
            """
            return db.fetch_all(query, (user.npm,))

        # ================= DOSEN =================
        elif user.role == "dosen":
            query = """
            SELECT course_name, description
            FROM courses
            WHERE owner = ?
            """
            return db.fetch_all(query, (user.nidn,))

        return []