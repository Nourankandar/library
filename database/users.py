import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import MySQLdb
import re
from .connect_DB import database

def is_valid_email(email):
    """
    يتحقق من أن البريد الإلكتروني يطابق التنسيق القياسي.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(regex, email):
        return True
    return False
class Users():

    def __init__(self):
        print("hello")
        self.create_user_table()
        

    def create_user_table(self):
        connect = database().connect()
        if connect is None:
            return
        try:
            connection=connect.cursor()
            connection.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100),
                    email VARCHAR(100) UNIQUE,
                    password_hash VARCHAR(255),
                    role VARCHAR(50) DEFAULT 'user',
                    must_change_pass BOOLEAN DEFAULT 0,
                    is_verified BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            connection.execute("SELECT COUNT(*) FROM users WHERE email = %s", ('admin@library.com',))
            count = connection.fetchone()[0]
            if count == 0:
                default_hashed_pass = "$2b$12$EXAMPLE_HASH_FOR_ADMIN_12345" # استخدم تجزئة حقيقية

                sql = "INSERT INTO users (full_name, email, password_hash, role, must_change_pass,is_verified) VALUES (%s, %s, %s, %s, %s,%s)"
                values = ('Default Admin', 'admin@library.com', default_hashed_pass, 'admin', 1,1) # القيمة 1 تجعل التغيير إجبارياً
                
                connection.execute(sql, values)
                print("Default Admin account created: admin@library.com. Change is mandatory.")
            connect.commit()
            print("User table created/verified.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            connect.close()
    

    def insert_user(self,full_name,email,password_hash):
        
        if not is_valid_email(email):
            print(f"Error: Invalid email format for {email}.")
            return 2
        connect = database().connect()
        if connect is None:
            return 0
        try:
            connection=connect.cursor()
            is_verified = 0
            sql = "INSERT INTO users (full_name, email, password_hash, role,is_verified) VALUES (%s, %s, %s, %s,%s)"
            values = (full_name, email, password_hash,'user',is_verified)
            connection.execute(sql, values)
            connect.commit()
            print("User inserted successfully.")
            return 1
        except MySQLdb.IntegrityError as e:
            print(f"Error: Email {email} already exists.")
            return 0
        except Exception as e:
            print(f"Error inserting user: {e}")
            return 0
        finally:
            connect.close()
    def delete_user(self, email):
        
        connect = database().connect()
        if connect is None:
            return False # الرجوع بقيمة False للاشارة الى فشل العملية بسبب عدم وجود اتصال
        try:
            connection = connect.cursor()
            sql = "DELETE FROM users WHERE email = %s"
            values = (email,) # لاحظ الفاصلة للحفاظ على القيم كـ Tuple حتى لو كانت قيمة واحدة
            
            connection.execute(sql, values)
            
            # الحصول على عدد الصفوف المتأثرة (المحذوفة)
            rows_affected = connection.rowcount
            
            connect.commit()
            
            if rows_affected > 0:
                print(f"User with email {email} deleted successfully.")
                return True
            else:
                # هذا يعني أن المستخدم لم يتم العثور عليه أو حذفه
                print(f"Error: User with email {email} not found or not deleted.")
                return False
                
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        finally:
            connect.close()


    def update_full_name(self, user_id, new_full_name):
        """
        تحديث الاسم الكامل للمستخدم.
        """
        connect = database().connect()
        if connect is None: return False
        try:
            cursor = connect.cursor()
            sql = "UPDATE users SET full_name = %s WHERE id = %s"
            cursor.execute(sql, (new_full_name, user_id))
            connect.commit()
            print(f"Full name updated successfully for user ID: {user_id}")
            return True
        except Exception as e:
            print(f"Error updating full name: {e}")
            return False
        finally:
            connect.close()
    
    def update_email(self, user_id, new_email):
        """
        تحديث البريد الإلكتروني للمستخدم، مع التحقق من تفرده.
        """
        connect = database().connect()
        if connect is None: return False
        try:
            cursor = connect.cursor()
            sql = "UPDATE users SET email = %s WHERE id = %s"
            cursor.execute(sql, (new_email, user_id))
            connect.commit()
            print(f"Email updated successfully for user ID: {user_id}")
            return True
        except MySQLdb.IntegrityError:
            print("Error: The new email is already in use by another account.")
            return False
        except Exception as e:
            print(f"Error updating email: {e}")
            return False
        finally:
            connect.close()

    def update_password(self, user_id, new_password_hash):
        """
        تحديث كلمة المرور.
        """
        connect = database().connect()
        if connect is None: return False
        try:
            cursor = connect.cursor()
            sql = "UPDATE users SET password_hash = %s, must_change_pass = 0 WHERE id = %s"
            cursor.execute(sql, (new_password_hash, user_id))
            connect.commit()
            print(f"Password updated successfully for user ID: {user_id}")
            return True
        except Exception as e:
            print(f"Error updating password: {e}")
            return False
        finally:
            connect.close()
    
    def get_user_login(self, email):
        connect = database().connect()
        if connect is None: return None
        try:
            cursor = connect.cursor()
            sql = "SELECT id,email, password_hash, role,is_verified,must_change_pass FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user_data = cursor.fetchone()
            return user_data
            
        except Exception as e:
            print(f"Error retrieving user data for login: {e}")
            return None
        finally:
            connect.close()
