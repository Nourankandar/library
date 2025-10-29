from pydoc import describe
from re import L
import sys
import os

from shiboken6 import delete
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from tkinter import *
from tkinter import messagebox
from database.categories import categories 
class LO_categories():
    
    def add_category(self,name,description_value):

        name = name.get().strip()
        description = description_value.get("1.0", END).strip()
        print(name,description,"inside logic")    
        if name is None or name == "":
            messagebox.showerror("خطأ", "الرجاء ملء حقل الاسم.")
            return False
        db = categories()
        try:
            success = db.add_category(name, description)
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
        if success:
            messagebox.showinfo("نجاح", f"تمت إضافة التصنيف '{name}' بنجاح.")
            return True
        else:
            messagebox.showerror("خطأ", f"فشل في إضافة التصنيف '{name}'. قد يكون الاسم مستخدمًا بالفعل.")
            return False
    def update_category(self,category_id,name,description_value):
        name = name.get().strip()
        description = description_value.get("1.0", END).strip()
        print(name,description,"inside logic update")    
        if name is None or name == "":
            messagebox.showerror("خطأ", "الرجاء ملء حقل الاسم.")
            return False
        db = categories()
        try:
            success = db.update_category(category_id, name, description)
        except Exception as e:
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
        if success:
            messagebox.showinfo("نجاح", f"تم تحديث التصنيف '{name}' بنجاح.")
            return True
        else:
            messagebox.showerror("خطأ", f"فشل في تحديث التصنيف '{name}'. قد يكون الاسم مستخدمًا بالفعل.")
            return False
    def get_all_categories(self,category_id=None):
        db = categories()
        try:
            raw_tuples = db.get_category()
            # print(raw_tuples,"raw_tuples")
            categories_list = []
            for row_tuple in raw_tuples:
                category_dict = {
                    'name': row_tuple[1],
                    'description': row_tuple[2],
                    'id': row_tuple[0]
                }
                categories_list.append(category_dict)
            return categories_list
        except Exception as e:
            print(f"Error fetching categories: {e}")
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return []
    
    def delete_category(self,category_id):
        db = categories()
        try:
            success = db.delete_category(category_id)
            if success:
                # messagebox.showinfo("نجاح", "تم حذف التصنيف بنجاح.")
                return True
            else:
                messagebox.showerror("خطأ", "فشل في حذف التصنيف. قد لا يكون موجودًا.")
                return False
        except Exception as e:
            print(f"Error deleting category: {e}")
            messagebox.showerror("خطأ في قاعدة البيانات", f"حدث خطأ: {e}")
            return False
