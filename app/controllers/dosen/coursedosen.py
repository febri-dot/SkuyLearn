from app.connection import Database

# =================================================================
# CONTROLLER: Logika Database
# =================================================================
class CourseDosenController:
    @staticmethod
    def get_materials_by_course(course_id):
        """Mengambil materi berdasarkan urutan kolom di gambar database"""
        db = Database()
        # Menggunakan ROWID karena di gambar tabel course_materials tidak terlihat kolom ID unik manual
        query = "SELECT ROWID, title, content, content_path FROM course_materials WHERE course_id = ?"
        rows = db.fetch_all(query, (course_id,))
        return [{
            "id": r[0],
            "title": r[1],
            "description": r[2], # Mapping dari kolom 'content'
            "file": r[3]         # Mapping dari kolom 'content_path'
        } for r in rows]

    @staticmethod
    def get_assignments_by_course(course_id):
        """Mengambil tugas berdasarkan urutan kolom di gambar database"""
        db = Database()
        # Kolom: id, course_id, title, description, assignment_path, due_date
        query = "SELECT id, title, description, due_date FROM assignments WHERE course_id = ?"
        rows = db.fetch_all(query, (course_id,))
        return [{
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "due_date": r[3]
        } for r in rows]

    @staticmethod
    def delete_material(row_id):
        """Menghapus materi menggunakan ROWID"""
        db = Database()
        query = "DELETE FROM course_materials WHERE ROWID = ?"
        return db.execute_query(query, (row_id,))

    @staticmethod
    def delete_assignment(assignment_id):
        """Menghapus tugas menggunakan ID"""
        db = Database()
        query = "DELETE FROM assignments WHERE id = ?"
        return db.execute_query(query, (assignment_id,))