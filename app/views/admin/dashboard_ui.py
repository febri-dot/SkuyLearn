import tkinter as tk
from app.controllers.admin.dashboard import DashboardController

class DashboardFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa") 
      self.controller = controller

      # --- Header Card ---
      self.header_card = tk.Frame(self, bg="white", padx=40, pady=20, 
                                    highlightbackground="#d1d1d1", highlightthickness=1)
      self.header_card.pack(side="top", fill="x", padx=20, pady=20) 

      tk.Label(self.header_card, text="SKUYLEARN DASHBOARD", bg="white", fg="#2c3e50", 
               font=("Helvetica", 24, "bold")).pack()
      
      self.info_label = tk.Label(self.header_card, text="", bg="white", fg="#7f8c8d", 
                                 font=("Helvetica", 14))
      self.info_label.pack(pady=5)

      # --- Container untuk Stat Cards  ---
      self.stats_container = tk.Frame(self, bg="#f8f9fa")
      self.stats_container.pack(fill="x", padx=15)

      # Card Mahasiswa
      self.student_card = self.create_stat_card(
         self.stats_container, "TOTAL MAHASISWA", "#3498db", 
         lambda: self.controller.show_frame("StudentDataFrame")
      )
      self.student_card.pack(side="left", expand=True, fill="both", padx=5)

      # Card Dosen
      self.lecturer_card = self.create_stat_card(
         self.stats_container, "TOTAL DOSEN", "#2ecc71", 
         lambda: self.controller.show_frame("LecturerDataFrame") 
      )
      self.lecturer_card.pack(side="left", expand=True, fill="both", padx=5)

      # --- Card Course (Full Width) ---
      self.course_container = tk.Frame(self, bg="#f8f9fa")
      self.course_container.pack(fill="x", padx=15, pady=10)

      self.course_card = self.create_stat_card(
         self.course_container, "TOTAL COURSES", "#9b59b6", 
         lambda: self.controller.show_frame("MyCoursesList") 
      )
      self.course_card.pack(fill="x", padx=5)

   def create_stat_card(self, parent, title, color, command):
      """Helper function untuk membuat kartu statistik yang bisa diklik"""
      card = tk.Frame(parent, bg="white", padx=20, pady=30, cursor="hand2",
                     highlightbackground="#d1d1d1", highlightthickness=1)
      
      # Label Title
      tk.Label(card, text=title, bg="white", fg="#7f8c8d", font=("Arial", 10, "bold")).pack()
      
      # Label Jumlah 
      count_label = tk.Label(card, text="0", bg="white", fg=color, font=("Helvetica", 32, "bold"))
      count_label.pack()

      # Binding klik (ke Frame dan semua label di dalamnya)
      for widget in (card, count_label):
         widget.bind("<Button-1>", lambda e: command())
      
      # Simpan count_label ke dalam card agar bisa diakses nanti
      card.count_label = count_label
      return card

   def refresh(self):
      user = self.controller.current_user
      if user:
         self.info_label.config(text=user.get_dashboard_info())
         
         try:
            stats = DashboardController.get_stats()
            
            self.student_card.count_label.config(text=str(stats["total_students"]))
            self.lecturer_card.count_label.config(text=str(stats["total_lecturers"]))
            self.course_card.count_label.config(text=str(stats["total_courses"]))
         except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            self.student_card.count_label.config(text="?")
            self.lecturer_card.count_label.config(text="?")
            self.course_card.count_label.config(text="?")
