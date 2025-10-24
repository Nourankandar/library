import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import datetime
import MySQLdb
from connect_DB import database

class authors():
    def create_authors_table(self):
        connect = database().connect()
        if connect is None:
            return
        try:
            cursor = connect.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            connect.commit()
            print("authors table created/verified.")
        except Exception as e:
            print(f"Error creating authors table: {e}")
        finally:
            connect.close()

    def __init__(self):
        self.create_authors_table()
    
    # -----------------------------------------------------------------
    ## 1. Create (إضافة كاتب جديد)
    
    def add_author(self, name, description=None):
        """يضيف كاتباً جديداً إلى قاعدة البيانات."""
        connect = database().connect()
        if connect is None:
            return False
        
        try:
            cursor = connect.cursor()
            sql = "INSERT INTO authors (name, description, created_at) VALUES (%s, %s, %s)"
            now = datetime.datetime.now()
            values = (name, description, now)
            
            cursor.execute(sql, values)
            connect.commit()
            print(f"Author '{name}' added successfully.")
            return cursor.lastrowid # يُرجع معرّف الكاتب المُضاف
        
        except MySQLdb.IntegrityError as e:
            # هنا قد تكون مشكلة الاسم المكرر (لأن name فريد UNIQUE)
            print(f"Error: Author name '{name}' already exists. Details: {e}")
            return False
        except Exception as e:
            print(f"Error adding author: {e}")
            return False
        finally:
            connect.close()

    # -----------------------------------------------------------------
    ## 2. Read (قراءة/جلب كاتب أو كل الكتّاب)

    def get_author(self, author_id=None, name=None):
        """يجلب كاتباً واحداً بالـ ID أو الاسم، أو كل الكتّاب."""
        connect = database().connect()
        if connect is None:
            return None
        
        try:
            cursor = connect.cursor()
            sql = "SELECT id, name, description, created_at FROM authors"
            params = []
            
            if author_id is not None:
                sql += " WHERE id = %s"
                params.append(author_id)
                
            elif name is not None:
                # يمكنك استخدام LIKE هنا إذا كنت تريد بحثاً جزئياً
                sql += " WHERE name = %s" 
                params.append(name)
            
            sql += " ORDER BY name"
            
            cursor.execute(sql, tuple(params))
            
            if author_id is not None or name is not None:
                result = cursor.fetchone() # جلب نتيجة واحدة
            else:
                result = cursor.fetchall() # جلب كل النتائج
            
            return result
            
        except Exception as e:
            print(f"Error fetching author: {e}")
            return None
        finally:
            connect.close()

    # -----------------------------------------------------------------
    ## 3. Update (تحديث بيانات كاتب)

    def update_author(self, author_id, **kwargs):
        """يحدث حقول الكاتب المحدد بالـ ID (مثل name='New Name', description='New Desc')."""
        if not kwargs:
            print("No fields provided for update.")
            return False
            
        connect = database().connect()
        if connect is None:
            return False
            
        now = datetime.datetime.now()

        try:
            cursor = connect.cursor()
            
            # إنشاء جملة SET ديناميكياً
            set_clauses = [f"{key} = %s" for key in kwargs.keys()]
            
            # القيم التي سيتم تحديثها
            values = list(kwargs.values())
            values.append(now) # إضافة updated_at
            
            # إضافة ID الكاتب لشرط WHERE
            values.append(author_id) 
            
            sql = f"UPDATE authors SET {', '.join(set_clauses)}, updated_at = %s WHERE id = %s"

            cursor.execute(sql, tuple(values))
            connect.commit()
            
            if cursor.rowcount > 0:
                print(f"Author ID {author_id} updated successfully.")
                return True
            else:
                print(f"Author ID {author_id} not found.")
                return False
                
        except MySQLdb.IntegrityError as e:
            # معالجة فشل التحديث بسبب تكرار الاسم (UNIQUE constraint)
            print(f"Error: Integrity constraint failed (Name already exists). Details: {e}")
            return False
        except Exception as e:
            print(f"Error updating author: {e}")
            return False
        finally:
            connect.close()
            
    # -----------------------------------------------------------------
    ## 4. Delete (حذف كاتب)

    def delete_author(self, author_id):
        """يحذف كاتباً حسب الـ ID."""
        connect = database().connect()
        if connect is None:
            return False
            
        try:
            cursor = connect.cursor()
            sql = "DELETE FROM authors WHERE id = %s"
            cursor.execute(sql, (author_id,))
            connect.commit()
            
            if cursor.rowcount > 0:
                print(f"Author ID {author_id} deleted successfully.")
                return True
            else:
                print(f"Author ID {author_id} not found.")
                return False
                
        except MySQLdb.IntegrityError as e:
            print(f"Error: Cannot delete Author ID {author_id}. Books are still linked to this author. Details: {e}")
            return False
        except Exception as e:
            print(f"Error deleting author: {e}")
            return False
        finally:
            connect.close()
authors()