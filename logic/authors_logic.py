
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from tkinter import *
from tkinter import messagebox
from database.authors import authors 
class authors_():
    
    def add_author(self,name,description_value):

        name = name.get().strip()
        description = description_value.get("1.0", END).strip()
        print(name,description,"inside logic")    
        if name is None or name == "":
            messagebox.showerror("خطأ", "الرجاء ملء حقل الاسم.")
            return False
        db = authors()
        try:
            success = db.add_author(name, description)
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
        if success:
            messagebox.showinfo("نجاح", f"تمت إضافة الكاتب  '{name}' بنجاح.")
            return True
        else:
            messagebox.showerror("خطأ", f"فشل في إضافة الكاتب  '{name}'. قد يكون الاسم مستخدمًا بالفعل.")
            return False
    def update_author(self,author_id,name,description_value):
        name = name.get().strip()
        description = description_value.get("1.0", END).strip()
        print(name,description,"inside logic update")    
        if name is None or name == "":
            messagebox.showerror("خطأ", "الرجاء ملء حقل الاسم.")
            return False
        db = authors()
        try:
            success = db.update_author(author_id, name, description)
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
        if success:
            messagebox.showinfo("نجاح", f"تم تحديث الكاتب  '{name}' بنجاح.")
            return True
        else:
            messagebox.showerror("خطأ", f"فشل في تحديث الكاتب  '{name}'. قد يكون الاسم مستخدمًا بالفعل.")
            return False
    def get_all_authors(self,author_id=None):
        db = authors()
        try:
            raw_tuples = db.get_author(author_id,)
            # print(raw_tuples,"raw_tuples")
            categories_list = []
            for row_tuple in raw_tuples:
                author_dict = {
                    'name': row_tuple[1],
                    'description': row_tuple[2],
                    'id': row_tuple[0]
                }
                categories_list.append(author_dict)
            return categories_list
        except Exception as e:
            print(f"Error fetching categories: {e}")
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return []
    
    def delete_author(self,author_id):
        db = authors()
        try:
            success = db.delete_author(author_id)
            if success:
                # messagebox.showinfo("نجاح", "تم حذف الكاتب  بنجاح.")
                return True
            else:
                messagebox.showerror("خطأ", "فشل في حذف الكاتب . قد لا يكون موجودًا.")
                return False
        except Exception as e:
            print(f"Error deleting author: {e}")
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
