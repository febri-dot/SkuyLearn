from app.connection import Database

class MyCourseController:
    @staticmethod
    def get_courses_for_user(user):
        db = Database()

        if user.role == "mahasiswa":
            query = """
            SELECT c.id, c.course_name, c.description
            FROM courses c
            JOIN enrollment_class e ON e.course_id = c.id
            WHERE e.npm = ?
            """
            rows = db.fetch_all(query, (user.npm,))
        else:
            query = """
            SELECT id, course_name, description
            FROM courses
            WHERE owner = ?
            """
            rows = db.fetch_all(query, (user.nidn,))

        courses = []
        for r in rows:
            courses.append({
                "id": r[0],
                "course_name": r[1],
                "description": r[2]
            })

        return courses
