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
                type VARCHAR(50) NOT NULL,
                category_id INT NOT NULL,
                author VARCHAR(255) NOT NULL,
                translator VARCHAR(255) NULL, 
                page_count INT,
                pdf_path VARCHAR(255) NOT NULL,
                publication_year INT,
                created_at DATETIME NOT NULL, 
                updated_at DATETIME,
                FOREIGN KEY (category_id) REFERENCES categories(id)
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