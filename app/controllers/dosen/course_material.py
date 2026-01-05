from app.connection import Database


class CourseMaterialController:

    @staticmethod
    def get_materials_by_course(course_id):
        db = Database()

        query = """
        SELECT course_id, uploaded_at, title, content, content_path
        FROM course_materials
        WHERE course_id = ?
        ORDER BY uploaded_at DESC
        """

        rows = db.fetch_all(query, (course_id,))

        return [
            {
                "course_id": r[0],
                "uploaded_at": r[1],   # ini pengganti ID
                "title": r[2],
                "content": r[3],
                "path": r[4]
            }
            for r in rows
        ]

    @staticmethod
    def create_material(course_id, title, content, content_path):
        db = Database()

        query = """
        INSERT INTO course_materials (course_id, title, content, content_path)
        VALUES (?, ?, ?, ?)
        """

        return db.execute_query(
            query,
            (course_id, title, content, content_path)
        )
