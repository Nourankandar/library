import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import MySQLdb
from .connect_DB import database
import datetime
class books():
    def create_books_table(self):
        connect = database().connect()
        if connect is None:
            return
        try:
            cursor = connect.cursor()
            cursor.execute("""
                CREATE TABLE books (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                ype ENUM('Novel', 'Article', 'Short Story', 'Scientific Book', 'Poem', 'Other') NOT NULL,
                category_id INT NOT NULL,
                author_id INTEGER,
                translator VARCHAR(255) NULL, 
                page_count INT,
                pdf_path VARCHAR(255) NOT NULL,
                publication_year INT,
                created_at DATETIME NOT NULL, 
                updated_at DATETIME,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                FOREIGN KEY(author_id) REFERENCES authors(id)
                )
            """)
            connect.commit()
            print("Categories table created/verified.")
        except Exception as e:
            print(f"Error creating categories table: {e}")
        finally:
            connect.close()

    def __init__(self):
        self.create_books_table()
    
    def add_book(self, title, book_type, category_id, author, pdf_path, page_count=None, translator=None, publication_year=None):
        """يضيف كتاباً جديداً إلى قاعدة البيانات."""
        connect = database().connect()
        if connect is None:
            return False
        
        now = datetime.datetime.now()
        
        try:
            cursor = connect.cursor()
            sql = """
                INSERT INTO books (title, type, category_id, author, translator, page_count, pdf_path, publication_year, created_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (title, book_type, category_id, author, translator, page_count, pdf_path, publication_year, now)
            
            cursor.execute(sql, values)
            connect.commit()
            print(f"Book '{title}' added successfully.")
            return True
        except MySQLdb.IntegrityError as e:
            print(f"Error: Integrity constraint failed. Ensure category_id {category_id} exists. Details: {e}")
            return False
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
        finally:
            connect.close()
        
    
    # -----------------------------------------------------------------
    ## 2. Read (قراءة/جلب كتاب أو كل الكتب)

    def get_books(self, book_id=None, category_id=None, book_type=None, author=None, search_term=None, limit=None):
        """
        يجلب كتاباً واحداً، أو مجموعة من الكتب بناءً على الفلاتر، أو مصطلح البحث.
        """
        connect = database().connect()
        if connect is None:
            return None
        
        try:
            cursor = connect.cursor()
            sql = "SELECT id, title, type, category_id, author, translator, page_count, pdf_path, publication_year, created_at FROM books"
            
            conditions = []
            params = []
                        
            if search_term is not None:
                search_like = f"%{search_term}%"
                search_condition = "(title LIKE %s OR author LIKE %s OR type LIKE %s)"
                conditions.append(search_condition)
                params.extend([search_like, search_like, search_like])


            if book_id is not None:
                conditions = ["id = %s"]
                params = [book_id]
                
            if category_id is not None:
                conditions.append("category_id = %s")
                params.append(category_id)
                
            if book_type is not None:
                conditions.append("type = %s")
                params.append(book_type)

            if author is not None and search_term is None: 
                conditions.append("author LIKE %s")
                params.append(f"%{author}%")
            
            if conditions:
                sql += " WHERE " + " AND ".join(conditions)
            
            if limit is not None:
                sql += " ORDER BY created_at DESC"
            else:
                sql += " ORDER BY title" 
                
            if limit is not None:
                sql += " LIMIT %s"
                params.append(limit)
            
            cursor.execute(sql, tuple(params))
            
            if book_id is not None and len(params) == 1:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            
            return result
            
        except Exception as e:
            print(f"Error fetching books: {e}")
            return None
        finally:
            connect.close()
    
    def update_book(self, book_id, **kwargs):
        """
        يحدث حقول الكتاب المحدد بالـ ID. (مثال: update_book(5, title='New Title', author='New Author'))
        """
        if not kwargs:
            print("No fields provided for update.")
            return False
            
        connect = database().connect()
        if connect is None:
            return False
            
        now = datetime.datetime.now()

        try:
            cursor = connect.cursor()
            
            set_clauses = [f"{key} = %s" for key in kwargs.keys()]
            
            values = list(kwargs.values())
            values.append(now)
            
            values.append(book_id)
            
            sql = f"UPDATE books SET {', '.join(set_clauses)}, updated_at = %s WHERE id = %s"

            cursor.execute(sql, tuple(values))
            connect.commit()
            
            if cursor.rowcount > 0:
                print(f"Book ID {book_id} updated successfully.")
                return True
            else:
                print(f"Book ID {book_id} not found.")
                return False
                
        except MySQLdb.IntegrityError as e:
            print(f"Error: Integrity constraint failed (e.g., category_id is invalid). Details: {e}")
            return False
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
        finally:
            connect.close()

    # -----------------------------------------------------------------
    ## 4. Delete (حذف كتاب)

    def delete_book(self, book_id):
        """يحذف كتاباً حسب الـ ID."""
        connect = database().connect()
        if connect is None:
            return False
            
        try:
            cursor = connect.cursor()
            sql = "DELETE FROM books WHERE id = %s"
            cursor.execute(sql, (book_id,))
            connect.commit()
            
            if cursor.rowcount > 0:
                print(f"Book ID {book_id} deleted successfully.")
                return True
            else:
                print(f"Book ID {book_id} not found.")
                return False
                
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
        finally:
            connect.close()