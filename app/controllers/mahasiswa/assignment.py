from app.connection import Database


class AssignmentMahasiswaController:

    @staticmethod
    def get_assignments_by_student(npm):
        """
        Ambil semua tugas dari course yang diikuti mahasiswa,
        termasuk status submission.
        """
        db = Database()

        query = """
        SELECT
            a.id,
            c.course_name,
            a.title,
            a.description,
            a.due_date,
            s.assignment_path
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        JOIN enrollment_class e ON e.course_id = c.id
        LEFT JOIN submissions s
            ON s.assignment_id = a.id AND s.npm = e.npm
        WHERE e.npm = ?
        ORDER BY a.due_date ASC
        """

        rows = db.fetch_all(query, (npm,))

        assignments = []
        for row in rows:
            assignments.append({
                "id": row[0],
                "course_name": row[1],
                "title": row[2],
                "description": row[3],
                "due_date": row[4],
                "file": row[5]
            })

        return assignments

    @staticmethod
    def submit_assignment(assignment_id, npm, file_path):
        """Insert / update submission"""
        db = Database()

        query = """
        INSERT INTO submissions (assignment_id, npm, assignment_path)
        VALUES (?, ?, ?)
        ON CONFLICT(assignment_id, npm)
        DO UPDATE SET
            assignment_path = excluded.assignment_path,
            submitted_at = CURRENT_TIMESTAMP
        """

        return db.execute_query(query, (assignment_id, npm, file_path))
