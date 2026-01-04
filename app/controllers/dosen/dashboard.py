from app.connection import Database

class DashboardDosenController:

    @staticmethod
    def get_course_detail(nidn):
        """
        Ambil course + materi + tugas yang diampu dosen
        """
        db = Database()

        courses = db.fetch_all("""
            SELECT id, course_name, description
            FROM courses
            WHERE owner = ?
            ORDER BY course_name
        """, (nidn,))

        result = []

        for c in courses:
            course_id, course_name, description = c

            materials = db.fetch_all("""
                SELECT title, uploaded_at
                FROM course_materials
                WHERE course_id = ?
                ORDER BY uploaded_at DESC
            """, (course_id,))

            assignments = db.fetch_all("""
                SELECT title, due_date
                FROM assignments
                WHERE course_id = ?
                ORDER BY due_date
            """, (course_id,))

            result.append({
                "course_name": course_name,
                "description": description,
                "materials": [
                    {"title": m[0], "uploaded_at": m[1]} for m in materials
                ],
                "assignments": [
                    {"title": a[0], "due_date": a[1]} for a in assignments
                ]
            })

        return result
