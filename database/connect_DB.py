import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import MySQLdb

class database():
    def connect(self):
        connection=MySQLdb.connect(
        host="localhost",
        user="nouran",
        passwd="nourankandar",
        db="my-data"
        )
        print("connected")
        return connection