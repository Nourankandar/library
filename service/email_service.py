
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from database.verification import verification
from database.users import Users
import datetime
from .config import *
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
def generate_verification_code(length=6):
    """توليد رمز رقمي عشوائي للتحقق."""
    return ''.join(random.choices('0123456789', k=length))

class service():
    def create_code_verification(self, email, purpose):
        db = Users()
        verify=verification()
        user = db.get_user_login(email)
        if user is None:
            return None
        user_id = user[0]

        code = generate_verification_code()
        expiry_time = datetime.datetime.now() + datetime.timedelta(minutes=10)
        
        success = verify.save_verification_code(user_id, code, purpose, expiry_time)
        if success:
            return success,user_id, code
        else:
            return None, None,None
        
    def send_verification_email(self,recipient_email, verification_code):
    
        message = MIMEMultipart("alternative")
        message["Subject"] = "رمز التحقق لحسابك"
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email

        # محتوى الرسالة (يمكنك استخدام HTML بدلاً من النص العادي)
        body = f"""
        مرحباً،
        
        رمز التحقق الخاص بك هو: {verification_code}
        
        الرجاء إدخال هذا الرمز لإكمال عملية التحقق خلال 10 دقائق.
        
        شكراً لك.
        """
        # تضمين المحتوى كنص عادي
        message.attach(MIMEText(body, "plain", "utf-8"))

        # 2. إعداد سياق التشفير (SSL Context)
        # هذا يضمن أن الاتصال آمن ومُشفَّر
        context = ssl.create_default_context()
        
        # 3. الاتصال بخادم SMTP والمحاولة
        try:
            # استخدام smtplib.SMTP للدلالة على استخدام بروتوكول SMTP
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                
                # 3.1. بدء تشفير TLS
                # TLS (Transport Layer Security) هو التشفير الحديث لضمان سرية البيانات
                server.starttls(context=context) 
                
                # 3.2. تسجيل الدخول إلى إيميل التطبيق
                # يستخدم SENDER_EMAIL و SENDER_PASSWORD للمصادقة على خادم غوغل
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                
                # 3.3. إرسال الرسالة
                # sendmail تأخذ (المرسل، المستلم، نص الرسالة مُحوَّلاً إلى سلسلة نصية)
                server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
            
            print(f"Verification code sent successfully to {recipient_email}")
            return True
        
        except smtplib.SMTPAuthenticationError:
            print("SMTP Error: Failed to login. Check SENDER_EMAIL and SENDER_PASSWORD (App Password).")
            return False
        except Exception as e:
            print(f"SMTP Error: Failed to send email: {e}")
            return False