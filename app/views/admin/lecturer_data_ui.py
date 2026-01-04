import tkinter as tk
from tkinter import messagebox
from app.controllers.admin.lecturer_controller import LecturerController
from app.views.admin.register_ui import RegisterWindow
from app.views.admin.edit_user_ui import EditUserWindow
from app.controllers.auth_manager import AuthManager

class LecturerDataFrame(tk.Frame):
   def __init__(self, parent, controller):
      super().__init__(parent, bg="#f8f9fa")
      self.controller = controller

      # --- Column Width Definitions ---
      self.col_widths = {
         "column": 15,
         "long_column": 25,
         "actions": 20
      }

      # --- Header Section ---
      self.header = tk.Frame(self, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#d1d1d1")
      self.header.pack(fill="x", padx=20, pady=(20, 10))
      
      tk.Label(self.header, text="LECTURER LIST", font=("Helvetica", 18, "bold"), bg="white", fg="#2c3e50").pack(side="left")
      tk.Button(self.header, text="+ Add Lecturer", bg="#2ecc71", fg="white", font=("Arial", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2", command=self.add_lecturer).pack(side="right")

      # --- Table Header ---
      self.table_header_bg = tk.Frame(self, bg="#34495e")
      self.table_header_bg.pack(fill="x", padx=20)
      
      self.header_inner = tk.Frame(self.table_header_bg, bg="#34495e")
      self.header_inner.pack(anchor="nw")

      # Changed "Username" to "NIDN" for clarity
      tk.Label(self.header_inner, text="NIDN", width=self.col_widths["column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Full Name", width=self.col_widths["long_column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10, anchor="w", padx=10).pack(side="left")
      tk.Label(self.header_inner, text="Phone Number", width=self.col_widths["column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Address", width=self.col_widths["long_column"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")
      tk.Label(self.header_inner, text="Actions", width=self.col_widths["actions"], bg="#34495e", fg="white", font=("Arial", 10, "bold"), pady=10).pack(side="left")

      # --- Scrollable Area ---
      self.container = tk.Frame(self, bg="#f8f9fa")
      self.container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

      self.h_scrollbar = tk.Scrollbar(self.container, orient="horizontal")
      self.h_scrollbar.pack(side="bottom", fill="x")

      self.canvas = tk.Canvas(self.container, bg="#f8f9fa", highlightthickness=0, xscrollcommand=self.h_scrollbar.set)
      self.v_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
      
      self.scroll_frame = tk.Frame(self.canvas, bg="#f8f9fa")
      self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
      
      self.canvas_frame = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
      
      self.v_scrollbar.config(command=self.canvas.yview)
      self.h_scrollbar.config(command=self.canvas.xview)
      self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

      self.canvas.pack(side="left", fill="both", expand=True)
      self.v_scrollbar.pack(side="right", fill="y")

   def refresh(self):
      """Clear and reload data from Controller"""
      for widget in self.scroll_frame.winfo_children():
         widget.destroy()

      try:
         # Assuming you have a LecturerController with get_all_lecturers
         lecturers = LecturerController.get_all_lecturers()
         if not lecturers:
            tk.Label(self.scroll_frame, text="No lecturers found.", bg="#f8f9fa", pady=20).pack()
            return

         for l in lecturers:
            row = tk.Frame(self.scroll_frame, bg="white", highlightthickness=1, highlightbackground="#f1f1f1")
            row.pack(fill="x", pady=1)

            tk.Label(row, text=l[0], width=self.col_widths["column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)
            tk.Label(row, text=l[1], width=self.col_widths["long_column"], bg="white", font=("Arial", 10), anchor="w", padx=10).pack(side="left", pady=10)
            tk.Label(row, text=l[5], width=self.col_widths["column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)
            tk.Label(row, text=l[4], width=self.col_widths["long_column"], bg="white", font=("Arial", 10)).pack(side="left", pady=10)

            action_area = tk.Frame(row, bg="white", width=180) 
            action_area.pack(side="left", fill="y")
            action_area.pack_propagate(False) 

            btn_edit = tk.Button(action_area, text="Edit", bg="#f1c40f", fg="white", relief="flat",
                              font=("Arial", 8, "bold"), padx=10, cursor="hand2", command=lambda d=l: self.edit_lecturer(d))
            btn_edit.pack(side="left", padx=5, pady=8)

            btn_delete = tk.Button(action_area, text="Delete", bg="#e74c3c", fg="white", relief="flat",
                                    font=("Arial", 8, "bold"), padx=10, cursor="hand2", command=lambda n=l[0]: self.delete_lecturer(n))
            btn_delete.pack(side="left", padx=2, pady=8)
      except Exception as e:
         print(f"Error loading lecturers: {e}")

   # --- Actions ---
   def delete_lecturer(self, nidn):
      if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ID {nidn}?\nThis will also delete the login account and this action cannot be undone."):
         # Still using AuthManager for centralized deletion
         success, message = AuthManager.delete_user(nidn, "DOSEN")
         if success:
            messagebox.showinfo("Success", "Lecturer and account have been deleted successfully.")
            self.refresh() 
         else:
            messagebox.showerror("Error", message)

   def edit_lecturer(self, data):
      # Reusing the same EditUserWindow but passing "DOSEN" role
      EditUserWindow(self, user_data=data, role="DOSEN")

   def add_lecturer(self):
      # Reusing the same RegisterWindow but passing "DOSEN" role
      RegisterWindow(self, role="DOSEN")