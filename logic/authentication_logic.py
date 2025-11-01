import re
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from tkinter import *
from tkinter import messagebox
import bcrypt
from database.users import Users
from service.email_service import service
from .session import save_session
def Register_Button(full_name, email, password):
    
    full_name = full_name.get().strip()
    email = email.get().strip()
    password = password.get()
    if not all([full_name, email, password]):
        messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")
        return
    
    db = Users()
    service1=service()
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        password_hash_str = hashed_password.decode('utf-8')
        if password_hash_str is None :
            messagebox.showerror("خطأ في الأمان", "حدث خطأ أثناء تجزئة كلمة المرور.")

        get_user=db.get_user_login( email)
        if get_user:
            messagebox.showerror("خطأ", "فشل في تسجيل المستخدم. قد يكون البريد الإلكتروني مستخدمًا بالفعل.")
            return
        insert_success = db.insert_user(full_name, email, password_hash_str)
        if insert_success==2:
            messagebox.showerror("the email wrong","your email is not validation")
            return False
        if insert_success==1:
            success_prep,user_id, message_prep = service1.create_code_verification(email, 'registration')
            if success_prep is None:
                messagebox.showerror("server error", "  ")
                db.delete_user(email)
                return False
            sent=service1.send_verification_email(email, message_prep)
            if sent is None:
                messagebox.showerror("خطأ في الإرسال", "فشل إرسال بريد التحقق. يرجى المحاولة لاحقاً.")
                db.delete_user(email)
                return False
            messagebox.showinfo("نجاح", "تم التسجيل بنجاح. يرجى التحقق من بريدك الإلكتروني.")
            return True
    except Exception as e:
        
        print(f"Hashing error: {e}")
        return
    
    
    
    
def LogIn_Button(email, password):
    email = email.get().strip()
    password = password.get()
    db=Users()
    service1=service()
    user=db.get_user_login(email)
    if not user:
        messagebox.showerror("Error","you are not registerd" )
        return False
    hashed_password_from_db = user[2].encode('utf-8')
    password_entered = password.encode('utf-8')
    
    try:
        if bcrypt.checkpw(password_entered, hashed_password_from_db):
            user_id = user[0]
            role = user[3]
            must_change_pass = user[5]
            is_verified = user[4]
            
            if is_verified == 0:
                messagebox.showerror("خطأ", "الرجاء تفعيل حسابك من خلال البريد الإلكتروني أولاً.")
                success_prep,user_id, message_prep = service1.create_code_verification(email, 'registration')
                if success_prep is None:
                    messagebox.showerror("server error", "  ")
                    db.delete_user(email)
                    return False ,None ,0
                sent=service1.send_verification_email(email, message_prep)
                if sent is None:
                    messagebox.showerror("خطأ في الإرسال", "فشل إرسال بريد التحقق. يرجى المحاولة لاحقاً.")
                    db.delete_user(email)
                    return False,None,0
                if sent :
                    return True,user,0
                
            else:
                messagebox.showinfo("نجاح", "تم التسجيل بنجاح. يرجى التحقق من بريدك الإلكتروني.")
                save_session(user_id,role)
                return True ,user,1

            if must_change_pass == 1:
                messagebox.showwarning("تغيير إجباري", "يجب عليك تغيير كلمة المرور الافتراضية الآن.")
                return True, user,1
            
            save_session(user_id,role)
            return True, user
        else:
            messagebox.showerror("Error", "Incorrect password.")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred during login.")
        print(f"Login error: {e}")




