from app.connection import Database

class MyCourseController:
    @staticmethod
    def get_courses_for_user(user):
        db = Database()
        # Samakan urutan kolom untuk semua role: id(0), name(1), desc(2), key(3), owner(4), lecturer_name(5)
        if user.role == "mahasiswa":
            query = """
                SELECT c.id, c.course_name, c.description, c.enrollment_key, c.owner, d.name
                FROM courses c
                JOIN enrollment_class e ON e.course_id = c.id
                JOIN dosen d ON c.owner = d.nidn
                WHERE e.npm = ?
            """
            return db.fetch_all(query, (user.npm,))

        elif user.role == "dosen":
            query = """
                SELECT c.id, c.course_name, c.description, c.enrollment_key, c.owner, d.name
                FROM courses c
                JOIN dosen d ON c.owner = d.nidn
                WHERE c.owner = ?
            """
            return db.fetch_all(query, (user.nidn,))

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
        # Gunakan MAX agar lebih aman jika ada data yang dihapus di tengah
        result = db.fetch_all("SELECT MAX(id) FROM courses")
        if result and result[0][0] is not None:
            return int(result[0][0]) + 1
        return 1


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
        
    @staticmethod
    def get_all_courses_with_owner():
        """Mengambil semua course beserta nama dosen pengampunya"""
        db = Database()
        query = """
            SELECT c.id, c.course_name, d.name as owner_name, c.description 
            FROM courses c
            JOIN dosen d ON c.owner = d.nidn
        """
        return db.fetch_all(query)

    @staticmethod
    def enroll_student(course_id, student_id, provided_key):
        """Mendaftarkan mahasiswa ke dalam course dengan validasi key"""
        db = Database()
        try:
            # 1. Ambil enrollment key yang asli dari tabel courses
            course = db.fetch_one("SELECT enrollment_key FROM courses WHERE id = ?", (course_id,))
            
            if not course:
                return False, "Course not found."
            
            # 2. Bandingkan key yang dimasukkan dengan yang ada di DB
            # course[0] karena fetch_one mengembalikan tuple/list
            if provided_key != course[0]:
                return False, "Invalid Enrollment Key. Please try again."

            # 3. Cek apakah mahasiswa sudah terdaftar (agar tidak double)
            exists = db.fetch_one(
                "SELECT * FROM enrollment_class WHERE course_id = ? AND npm = ?", 
                (course_id, student_id)
            )
            if exists:
                return False, "You are already enrolled in this course."
            
            # 4. Jika key benar dan belum terdaftar, lakukan pendaftaran
            db.execute_query(
                "INSERT INTO enrollment_class (course_id, npm) VALUES (?, ?)", 
                (course_id, student_id)
            )
            return True, "Successfully enrolled!"
            
        except Exception as e:
            return False, f"System error: {str(e)}"