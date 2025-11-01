
import datetime
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database.verification import verification
from database.users import Users
from service.email_service import service
import bcrypt
from .verification_logic import verify_user_code
def request_password_reset_logic(email):
    """
    الخطوة الأولى: التحقق من وجود المستخدم وإنشاء رمز إعادة تعيين وإرساله.
    """
    db = Users()
    service1 = service()
    user_data = db.get_user_login(email)
    if not user_data:
        return False, "لم يتم العثور على بريد إلكتروني مسجل."   
    success_prep, user_id, message_prep = service1.create_code_verification(email, 'password_reset')
    if success_prep is None:
        return False, "حدث خطأ في تجهيز كود إعادة التعيين."
    sent = service1.send_verification_email(email, message_prep)
    if sent:
        return True, "تم إرسال كود التحقق بنجاح."
    else:
        return False, "فشل إرسال بريد التحقق. يرجى المحاولة لاحقاً."

def reset_password_logic(email, code, new_password):
    """
    الخطوة الثانية: التحقق من الكود وتحديث كلمة المرور.
    """
    db = Users()
    result = verify_user_code(email, code, 'password_reset') 
    
    if result is not True:
        return False, "كود التحقق غير صحيح أو انتهت صلاحيته."
        
    try:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        password_hash_str = hashed_password.decode('utf-8')
    except Exception:
        return False, "فشل في تجزئة كلمة المرور الجديدة."

    user_data = db.get_user_login(email)
    user_id = user_data[0]
    
    update_success = db.update_password(user_id, password_hash_str)
    
    if update_success:
        return True, "تم تحديث كلمة المرور بنجاح."
    else:
        return False, "فشل في تحديث كلمة المرور في قاعدة البيانات."