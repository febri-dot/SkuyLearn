from app.connection import Database

class DashboardDosenController:

    @staticmethod
    def get_course_detail(nidn):
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
                "course_id": course_id,  # <--- TAMBAHKAN INI (Penting!)
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
    
    @staticmethod
    def delete_course(course_id):
        db = Database()
        try:
            # 1. Ambil semua path file materi & tugas untuk dihapus fisiknya
            files = db.fetch_all("""
                SELECT content_path FROM course_materials WHERE course_id = ?
                UNION
                SELECT assignment_path FROM assignments WHERE course_id = ?
            """, (course_id, course_id))

            for f in files:
                if f[0] and os.path.exists(f[0]):
                    os.remove(f[0])

            # 2. Hapus data di database (Urutan penting untuk foreign key)
            db.execute_query("DELETE FROM enrollment_class WHERE course_id = ?", (course_id,))
            db.execute_query("DELETE FROM course_materials WHERE course_id = ?", (course_id,))
            db.execute_query("DELETE FROM assignments WHERE course_id = ?", (course_id,))
            db.execute_query("DELETE FROM courses WHERE id = ?", (course_id,))
            
            return True, "Course and all related data deleted successfully."
        except Exception as e:
            return False, str(e)
