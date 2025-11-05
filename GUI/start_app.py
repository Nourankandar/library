
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database import authors,books,categories,users,verification
from logic.session import load_session
from main_GUI import Home
from authentication_GUI import Log_in
IMAGE_PATH = 'static/start_image/image.png' 
SPLASH_DURATION_MS = 1000
class public_Create_tables():
    def __init__(self):
        users.Create_User()
        verification.Create_Verification()
        categories.Create_Gategories()
    
    def GUI(self,name):
        frame=Tk()
        frame['bg'] = 'lightblue'
        frame.geometry("1000x700+200+50")
        frame.title(name)
        return frame
    
    def main_app_start(self, user_id=None, user_role=None):
        """
        منطق نقطة البداية الرئيسية:
        يتحقق من الجلسة ويبدأ الواجهة المناسبة (الرئيسية أو الدخول).
        """
        user_data=[user_id,user_role]
        if user_id is None:
            user_id, user_role = load_session() 
        user_data=[user_id,user_role]
        if user_id and user_role:
            print(user_data)
            print(f"Session found for user ID: {user_id}. Role: {user_role}. Starting Home.")
            Home(user_data) 
        else:
            print("No session found. Starting Log In screen.")
            Log_in()
    
    def show_splash_and_start(self):
        """تنشئ شاشة البداية المؤقتة وتنتقل إلى main_app_start بعدها."""
        splash_root = self.GUI("Welcome")

        try:
            img = Image.open(IMAGE_PATH)
            resized_img = img.resize((1000, 700), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized_img)
            
            image_label = Label(splash_root, image=photo)
            self.splash_image_reference = photo 
            
            image_label.image = self.splash_image_reference # حفظ مرجع إضافي داخل الـ Label
            image_label.pack(fill=BOTH, expand=1)
        
        except FileNotFoundError:
            print(f"Error: Image file not found at {IMAGE_PATH}. Skipping splash screen.")
            splash_root.destroy()
            self.main_app_start() 
            return
        
        except Exception as e:
            print(f"Error loading image or running splash screen: {e}")
            splash_root.destroy()
            self.main_app_start()
            return

        def close_splash_and_open_main():
            del self.splash_image_reference 
            splash_root.destroy() 
            self.main_app_start() 

        splash_root.after(SPLASH_DURATION_MS, close_splash_and_open_main) 
        splash_root.mainloop()

if __name__ == "__main__":
    app = public_Create_tables()
    app.show_splash_and_start()