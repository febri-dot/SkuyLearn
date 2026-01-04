import tkinter as tk
from tkinter import messagebox
from app.controllers.mycourse import MyCourseController

class CourseWindow(tk.Toplevel):
   def __init__(self, parent, course_data=None):
      super().__init__(parent)
      self.caller = parent 
      self.is_edit = course_data is not None
      
      # Mengambil user yang sedang login dari controller utama
      self.current_user = parent.controller.current_user
      
      self.title("Edit Course" if self.is_edit else "Add New Course")
      self.geometry("450x650")
      self.configure(bg="#f8f9fa")
      self.grab_set()

      self.main_frame = tk.Frame(self, bg="white", padx=30, pady=25, highlightthickness=1, highlightbackground="#d1d1d1")
      self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

      tk.Label(self.main_frame, text="COURSE INFORMATION", font=("Helvetica", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

      self.entries = {}
      fields = [
         ("Course ID (Auto)", "id"),
         ("Course Name", "name"),
         ("Description", "desc"),
         ("Enrollment Code", "code"),
         ("Owner (Lecturer NIDN)", "owner")
      ]

      for label_text, key in fields:
         tk.Label(self.main_frame, text=label_text, bg="white", font=("Arial", 9, "bold"), fg="#34495e").pack(anchor="w")
         
         if key == "desc":
               entry = tk.Text(self.main_frame, font=("Arial", 11), bg="#f1f3f5", relief="flat", height=4)
         else:
               entry = tk.Entry(self.main_frame, font=("Arial", 11), bg="#f1f3f5", relief="flat")
         
         # --- LOGIKA AUTO GENERATE ID & OWNER ---
         if self.is_edit:
               # Mode Edit: mapping data index sesuai database
               val = course_data[0] if key=="id" else course_data[1] if key=="name" else \
                     course_data[2] if key=="desc" else course_data[3] if key=="code" else course_data[4]
               
               if key == "desc": entry.insert("1.0", val)
               else: entry.insert(0, val)
               
               # Saat edit, ID selalu readonly
               if key == "id": entry.config(state="readonly", readonlybackground="#e9ecef")
         else:
               # Mode Tambah Baru
               if key == "id":
                  # Ambil Last ID + 1 dari Controller
                  next_id = MyCourseController.get_next_id()
                  entry.insert(0, str(next_id))
                  entry.config(state="readonly", readonlybackground="#e9ecef")
               
               # Jika yang buka adalah DOSEN, NIDN otomatis terisi & readonly
               if key == "owner" and self.current_user.role.lower() == "dosen":
                  # Pastikan objek user kamu punya atribut 'nidn' atau 'username'
                  nidn_dosen = getattr(self.current_user, 'nidn', self.current_user.username)
                  entry.insert(0, nidn_dosen)
                  entry.config(state="readonly", readonlybackground="#e9ecef")

         entry.pack(fill="x", pady=(5, 12), ipady=7 if key != "desc" else 0)
         self.entries[key] = entry

      btn_bg = "#f1c40f" if self.is_edit else "#2ecc71"
      tk.Button(self.main_frame, text="SAVE COURSE", bg=btn_bg, fg="white", 
               font=("Arial", 11, "bold"), height=2, relief="flat", cursor="hand2",
               command=self.handle_save).pack(fill="x", pady=15)

   def handle_save(self):
      data = {}
      for k, w in self.entries.items():
         if k == "desc":
               data[k] = w.get("1.0", "end-1c").strip()
         else:
               # Ambil teks meski state sedang readonly
               curr_state = w.cget("state")
               w.config(state="normal")
               data[k] = w.get().strip()
               w.config(state=curr_state)

      if not data['name'] or not data['owner']:
         messagebox.showwarning("Warning", "Course Name and Owner are required!")
         return

      success, msg = MyCourseController.save_course(data, self.is_edit)
      if success:
         messagebox.showinfo("Success", msg)
         if hasattr(self.caller, 'refresh'):
               self.caller.refresh()
         self.destroy()
      else:
         messagebox.showerror("Error", msg)