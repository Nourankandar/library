import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import MySQLdb
from .connect_DB import database
import datetime
class Create_Gategories():
    def create_categories_table(self):
        connect = database().connect()
        if connect is None:
            return
        try:
            cursor = connect.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, 
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
            connect.commit()
            print("Categories table created/verified.")
        except Exception as e:
            print(f"Error creating categories table: {e}")
        finally:
            connect.close()

    def __init__(self):
        self.create_categories_table()

class categories():
    
    def add_category(self, name, description):
        """يضيف تصنيفاً جديداً."""
        name = name.strip()
        description = description.strip()
        connect = database().connect()
        if connect is None:
            return False
        
        now = datetime.datetime.now()
        try:
            cursor = connect.cursor()
            sql = "INSERT INTO categories (name,description, created_at) VALUES (%s, %s,%s)"
            values = (name,description, now)
            cursor.execute(sql, values)
            connect.commit()
            print(f"Category '{name}' added successfully.")
            return True
        except MySQLdb.IntegrityError:
            print(f"Error: Category '{name}' already exists.")
            return False
        except Exception as e:
            print(f"Error adding category: {e}")
            return False
        finally:
            connect.close()

    # -----------------------------------------------------------------
    ## 2. Read (قراءة/جلب تصنيف أو كل التصنيفات)
    def get_category(self, category_id=None):
        """
        يجلب تصنيف واحد بالـ ID أو يجلب جميع التصنيفات إذا كان ID فارغاً.
        """
        connect = database().connect()
        if connect is None:
            return None
        
        try:
            cursor = connect.cursor()
            
            if category_id is None:
                sql = "SELECT id, name,description  FROM categories ORDER BY name"
                cursor.execute(sql)
                result = cursor.fetchall()
            else:
                sql = "SELECT id, name,description  FROM categories WHERE id = %s"
                cursor.execute(sql, (category_id,))
                result = cursor.fetchone() 
            
            return result
            
        except Exception as e:
            print(f"Error fetching category: {e}")
            return None
        finally:
            connect.close()

    # -----------------------------------------------------------------
    ## 3. Update (تحديث اسم تصنيف موجود)

    def update_category(self, category_id, new_name,description):
        """يحدث اسم التصنيف حسب الـ ID."""
        new_name = new_name.strip()
        description = description.strip()
        connect = database().connect()
        if connect is None:
            return False
            
        now = datetime.datetime.now()

        try:
            cursor = connect.cursor()
            sql = "UPDATE categories SET name = %s, description = %s, updated_at = %s WHERE id = %s"
            values = (new_name,description, now, category_id)
            cursor.execute(sql, values)
            connect.commit()
            if cursor.rowcount > 0:
                print(f"Category ID {category_id} updated to '{new_name}' successfully.")
                return True
            else:
                print(f"Category ID {category_id} not found.")
                return False
                
        except MySQLdb.IntegrityError:
            print(f"Error: Category name '{new_name}' already exists.")
            return False
        except Exception as e:
            print(f"Error updating category: {e}")
            return False
        finally:
            connect.close()
    
    def delete_category(self, category_id):
        """يحذف التصنيف حسب الـ ID."""
        connect = database().connect()
        if connect is None:
            return False
            
        try:
            cursor = connect.cursor()
            sql = "DELETE FROM categories WHERE id = %s"
            cursor.execute(sql, (category_id,))
            connect.commit()
            
            # التحقق مما إذا تم حذف صف فعلاً
            if cursor.rowcount > 0:
                print(f"Category ID {category_id} deleted successfully.")
                return True
            else:
                print(f"Category ID {category_id} not found.")
                return False
                
        except Exception as e:
            print(f"Error deleting category: {e}")
            return False
        finally:
            connect.close()