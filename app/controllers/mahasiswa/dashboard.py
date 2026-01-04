from app.connection import Database

class DashboardMahasiswaController:

    @staticmethod
    def get_stats(npm):
        """Total materi & tugas mahasiswa"""
        db = Database()

        materi = db.fetch_one("""
            SELECT COUNT(cm.course_id)
            FROM course_materials cm
            JOIN enrollment_class ec
                ON cm.course_id = ec.course_id
            WHERE ec.npm = ?
        """, (npm,))

        tugas = db.fetch_one("""
            SELECT COUNT(a.id)
            FROM assignments a
            JOIN enrollment_class ec
                ON a.course_id = ec.course_id
            WHERE ec.npm = ?
        """, (npm,))

        return {
            "total_materials": materi[0] if materi else 0,
            "total_assignments": tugas[0] if tugas else 0
        }

    @staticmethod
    def get_materials(npm):
        """Daftar materi berdasarkan course yang diikuti"""
        db = Database()

        rows = db.fetch_all("""
            SELECT
                c.course_name,
                cm.title,
                cm.uploaded_at
            FROM course_materials cm
            JOIN courses c ON cm.course_id = c.id
            JOIN enrollment_class ec ON c.id = ec.course_id
            WHERE ec.npm = ?
            ORDER BY cm.uploaded_at DESC
        """, (npm,))

        return [
            {
                "course_name": r[0],
                "title": r[1],
                "uploaded_at": r[2]
            }
            for r in rows
        ]

    @staticmethod
    def get_assignments(npm):
        """Daftar tugas mahasiswa"""
        db = Database()

        rows = db.fetch_all("""
            SELECT
                c.course_name,
                a.title,
                a.due_date
            FROM assignments a
            JOIN courses c ON a.course_id = c.id
            JOIN enrollment_class ec ON c.id = ec.course_id
            WHERE ec.npm = ?
            ORDER BY a.due_date
        """, (npm,))

        return [
            {
                "course_name": r[0],
                "title": r[1],
                "due_date": r[2]
            }
            for r in rows
        ]
