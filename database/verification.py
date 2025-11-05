import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import MySQLdb
from .connect_DB import database

class Create_Verification():
    def create_verify_table(self):
        connect = database().connect()
        if connect is None:
            return
        try:
            cursor = connect.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS verification_codes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    code VARCHAR(10) NOT NULL,
                    purpose ENUM('registration', 'password_reset', 'email_change') NOT NULL,
                    created_at DATETIME NOT NULL,
                    expires_at DATETIME NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            connect.commit()
            print("Verification codes table created/verified.")
        except Exception as e:
            print(f"Error creating verification codes table: {e}")
        finally:
            connect.close()
    def __init__(self):
        self.create_verify_table()
class verification():
    def save_verification_code(self, user_id, code, purpose, expires_at):
        connect = database().connect()
        if connect is None: return False
        
        try:
            cursor = connect.cursor()
            cursor.execute("DELETE FROM verification_codes WHERE user_id = %s AND purpose = %s", (user_id, purpose))
            
            sql = """
                INSERT INTO verification_codes (user_id, code, purpose, created_at, expires_at) 
                VALUES (%s, %s, %s, NOW(), %s)
            """
            cursor.execute(sql, (user_id, code, purpose, expires_at))
            connect.commit()
            print(f"Verification code saved for user {user_id} for {purpose}.")
            return True
        except Exception as e:
            print(f"Error saving verification code: {e}")
            return False
        finally:
            connect.close()
    
    def get_verification_code_data(self, user_id, code, purpose):
        """
        يسترد بيانات رمز التحقق (للمقارنة والتحقق من الصلاحية).
        
        Returns:
            tuple or None: (code, expires_at) إذا تم العثور على الرمز، وإلا None.
        """
        connect = database().connect()
        if connect is None: return None
        
        try:
            cursor = connect.cursor()
            sql = """
                SELECT code, expires_at 
                FROM verification_codes 
                WHERE user_id = %s AND code = %s AND purpose = %s
            """
            cursor.execute(sql, (user_id, code, purpose))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error retrieving verification code data: {e}")
            return None
        finally:
            connect.close()

    def activate_user_and_delete_code(self, user_id, purpose):
        """
        تفعيل حساب المستخدم وحذف الرموز القديمة.
        """
        connect = database().connect()
        if connect is None: return False
        try:
            cursor = connect.cursor()
            cursor.execute("UPDATE users SET is_verified = 1 WHERE id = %s", (user_id,))
            cursor.execute("DELETE FROM verification_codes WHERE user_id = %s AND purpose = %s", (user_id, purpose))
            
            connect.commit()
            print(f"User {user_id} activated and code deleted for {purpose}.")
            return True
        except Exception as e:
            print(f"Error activating user/deleting code: {e}")
            return False
        finally:
            connect.close()
    
    def delete_code(self,user_id):
        connect = database().connect()
        if connect is None: return False
        try:
            cursor = connect.cursor()
            cursor.execute("DELETE FROM verification_codes WHERE user_id = %s AND purpose = %s", (user_id))
            
            connect.commit()
            print(f"User {user_id}  code deleted ")
            return True
        except Exception as e:
            print(f"Error activating user/deleting code: {e}")
            return False
        finally:
            connect.close()