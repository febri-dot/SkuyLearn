from app.views.main_frame import SkuylearnApp
from app.connection import init_db, initlize_dummy

if __name__ == "__main__":
   init_db()
   initlize_dummy()
   
   app = SkuylearnApp()
   app.mainloop()