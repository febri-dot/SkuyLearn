from app.connection import Database


class AssignmentDosenController:

    @staticmethod
    def get_assignments_by_course(course_id):
        db = Database()

        query = """
        SELECT id, title, description, due_date
        FROM assignments
        WHERE course_id = ?
        ORDER BY due_date ASC
        """

        rows = db.fetch_all(query, (course_id,))

        return [{
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "due_date": r[3]
        } for r in rows]

    @staticmethod
    def create_assignment(course_id, title, description, due_date):
        db = Database()

        query = """
        INSERT INTO assignments (course_id, title, description, due_date)
        VALUES (?, ?, ?, ?)
        """

        return db.execute_query(
            query,
            (course_id, title, description, due_date)
        )
