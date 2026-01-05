# app/controllers/dosen/assignment.py
import os
import shutil
from datetime import datetime
from app.connection import Database

class AssignmentDosenController:
    STORAGE_PATH = os.path.join("storage", "assignments")

    @staticmethod
    def create_assignment(course_id, title, description, due_date, source_path):
        db = Database()
        final_storage_path = ""

        # Handle File Upload to Storage
        if source_path and os.path.exists(source_path):
            try:
                if not os.path.exists(AssignmentDosenController.STORAGE_PATH):
                    os.makedirs(AssignmentDosenController.STORAGE_PATH)

                filename = os.path.basename(source_path)
                unique_name = f"{int(datetime.now().timestamp())}_{filename}"
                final_storage_path = os.path.join(AssignmentDosenController.STORAGE_PATH, unique_name)
                
                shutil.copy(source_path, final_storage_path)
            except Exception as e:
                return False, f"File Error: {str(e)}"

        query = """
            INSERT INTO assignments (course_id, title, description, due_date, assignment_path)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (course_id, title, description, due_date, final_storage_path)
        
        try:
            db.execute_query(query, params)
            return True, "Assignment published successfully!"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def get_assignments_by_course(course_id):
        db = Database()
        return db.fetch_all("SELECT * FROM assignments WHERE course_id = ?", (course_id,))
    
    @staticmethod
    def update_assignment(assignment_id, title, description, due_date, source_path, old_path):
        db = Database()
        final_path = old_path

        # Jika ada file baru yang dipilih
        if source_path and source_path != old_path:
            try:
                # 1. Hapus file lama jika ada
                if old_path and os.path.exists(old_path):
                    os.remove(old_path)

                # 2. Simpan file baru
                if not os.path.exists(AssignmentDosenController.STORAGE_PATH):
                    os.makedirs(AssignmentDosenController.STORAGE_PATH)
                
                filename = os.path.basename(source_path)
                unique_name = f"{int(datetime.now().timestamp())}_{filename}"
                final_path = os.path.join(AssignmentDosenController.STORAGE_PATH, unique_name)
                shutil.copy(source_path, final_path)
            except Exception as e:
                return False, f"File Error: {str(e)}"

        query = """
            UPDATE assignments 
            SET title = ?, description = ?, due_date = ?, assignment_path = ?
            WHERE id = ?
        """
        params = (title, description, due_date, final_path, assignment_id)
        
        try:
            db.execute_query(query, params)
            return True, "Assignment updated successfully!"
        except Exception as e:
            return False, str(e)