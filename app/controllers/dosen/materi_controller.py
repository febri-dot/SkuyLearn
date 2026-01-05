# app/controllers/dosen/materi_controller.py
import os
import shutil
from datetime import datetime
from app.connection import Database

class MateriController:
   STORAGE_PATH = os.path.join("storage", "materials")

   @classmethod
   def _save_to_storage(cls, source_path):
      """Helper to copy local file to project storage"""
      if not source_path or not os.path.exists(source_path):
         return ""
      
      # If already in storage, don't copy again
      if cls.STORAGE_PATH in source_path:
         return source_path

      try:
         if not os.path.exists(cls.STORAGE_PATH):
               os.makedirs(cls.STORAGE_PATH)

         filename = os.path.basename(source_path)
         # Unique name to prevent overwriting: timestamp_filename
         unique_name = f"{int(datetime.now().timestamp())}_{filename}"
         destination = os.path.join(cls.STORAGE_PATH, unique_name)
         
         shutil.copy(source_path, destination)
         return destination
      except Exception as e:
         print(f"Storage Error: {e}")
         return ""

   @staticmethod
   def save_materi(course_id, title, content, source_path):
      db = Database()
      final_path = MateriController._save_to_storage(source_path)
      
      query = """
         INSERT INTO course_materials (course_id, uploaded_at, title, content, content_path)
         VALUES (?, ?, ?, ?, ?)
      """
      params = (course_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, content, final_path)
      
      try:
         db.execute_query(query, params)
         return True, "Material successfully published and file stored!"
      except Exception as e:
         return False, str(e)

   @staticmethod
   def update_materi(course_id, old_title, new_title, new_content, source_path):
      db = Database()
      final_path = MateriController._save_to_storage(source_path)
      
      query = """
         UPDATE course_materials 
         SET title = ?, content = ?, content_path = ?
         WHERE course_id = ? AND title = ?
      """
      params = (new_title, new_content, final_path, course_id, old_title)
      
      try:
         db.execute_query(query, params)
         return True, "Material updated successfully!"
      except Exception as e:
         return False, str(e)