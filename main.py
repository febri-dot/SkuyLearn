from app.views.main_frame import SkuylearnApp
from app.connection import Database

def start_app():
   db = Database()
   db.init_db() 

   app = SkuylearnApp()
   app.mainloop()

if __name__ == "__main__":
   start_app()