
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys
import os

from shiboken6 import delete
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from logic.category_logic import LO_categories
class categories():
    _main_categories_frame = None
    sample_categories=LO_categories().get_all_categories()
    
    def GUI(self,name):
        frame=Tk()
        frame['bg'] = 'lightblue'
        frame.geometry("600x600+400+100")
        frame.title(name)
        inner_frame = LabelFrame(frame,text=name,font=('Times New Roman', 50),bg='lightblue',fg='black')
        inner_frame.place(x=40,y=0,width=520,height=500)
        return frame,inner_frame
    
    def general_button(self,frame,buttontext,x,y,command_func):
        button=Button(frame,text=buttontext,font=('Times New Roman', 16, 'bold'),command=command_func,height=1,bg="#F5CDCD", fg='black', relief=FLAT,foreground='black')
        button.place(x=x,y=y)

    font=('Times New Roman',20)
    def general_lable(self,frame,text,x,y):
        lable= Label(frame,text=text,background='lightblue',font=self.font)
        lable.place(x=x,y=y)

    def general_entry(self,frame,variable,x,y):
        entry = Entry(frame,textvariable=variable,justify=CENTER,font=('Times New Roman',18),width=30)
        entry.place(x=x, y=y)
    def general_text_area(self, frame, x, y, height_val=5, width_val=40):
        text_widget = Text(
            frame, 
            height=height_val,  
            width=width_val,   
            font=('Times New Roman', 14)
        )
        text_widget.place(x=x, y=y)
        return text_widget
    
    def category_lables(self,inner_frame):
        name=StringVar()
        self.general_lable(inner_frame,"Category Name",100,30)    
        self.general_entry(inner_frame,name,100,80)
        self.general_lable(inner_frame,"Description:",100,130)
        description_widget = self.general_text_area(inner_frame, 100, 180, height_val=5, width_val=40)
        print(name,description_widget,"inside lables")
        return name,description_widget
        
    def _category(self,main_frame,title,text,textbutton,stringname,category_id=None):
        frame = Toplevel() 
        frame['bg'] = 'lightblue'
        frame.geometry("600x600+400+100")
        frame.title(title)
        inner_frame = LabelFrame(frame,text=text,font=('Times New Roman', 50),bg='lightblue',fg='black')
        inner_frame.place(x=40,y=0,width=520,height=500)
        name,description =self.category_lables(inner_frame)
        self._Button(inner_frame,frame,main_frame,name,description,textbutton,stringname,category_id)
        self.general_button(inner_frame,"back",100,300,lambda:frame.destroy())

    def _Button(self,frame,frame2,main_frame,name,description,textbutton,stringname,category_id):
        button=Button(frame,text=textbutton,font=('Times New Roman', 16, 'bold'),command=lambda:self.save_and_close(frame,frame2,main_frame, name, description,stringname,category_id),height=1,bg="#F5CDCD", fg='black', relief=FLAT,foreground='black')
        button.place(x=200,y=300
                     )
    def save_and_close(self, frame,frame2,main_frame, name, description,stringname,category_id):
        save_category=LO_categories()
        if stringname=="add":
            success=save_category.add_category(name, description) 
        else:
            success=save_category.update_category(category_id,name, description)
        if success:
            main_frame.destroy()
            frame2.destroy()
            frame.destroy()
            self.categories(LO_categories().get_all_categories())

    def create_category_card(self,parent_frame, category_data,main_window):
        CARD_WIDTH = 450  
        CARD_HEIGHT = 50
        card = Frame(parent_frame, bg='#F0F0F0',  bd=1, relief=GROOVE, width=CARD_WIDTH, height=CARD_HEIGHT)
        card.place(x=10,y=50)
        title_label=Label(card, text=category_data['name'], font=('Times New Roman', 17, 'bold'),cursor="hand2",wraplength=200, bg='#F0F0F0')
        title_label.place(x=10,y=10)
        def open_category():
            main_window.destroy() 
            self.category(category_data)
        title_label.bind("<Button-1>",lambda e:open_category())
        title_label.bind("<Enter>", lambda event: title_label.config(fg="red"))
        title_label.bind("<Leave>", lambda event: title_label.config(fg="black")) 
        self.general_button(card,"Edit",280,4,command_func=lambda:self.edit_category(category_data,main_window))
        self.general_button(card,"Delete",350,4,command_func=lambda:self.delete_category_handler(category_data['id'],card,main_window))
        return card
    
    def delete_category_handler(self, category_id, card_frame, main_frame):
        confirm = messagebox.askyesno(
            "تأكيد الحذف",
            f"هل أنت متأكد من أنك تريد حذف هذا التصنيف نهائياً؟\nسيؤدي هذا لحذف البيانات المتعلقة به.",
            icon='warning' 
        )
        if confirm:
            logic = LO_categories()
            success = logic.delete_category(category_id)
            
            if success:
                messagebox.showinfo("نجاح", "تم حذف التصنيف بنجاح.")
                card_frame.destroy()
                main_frame.destroy()
                updated_categories = logic.get_all_categories()
                self.categories(updated_categories)
            else:
                messagebox.showerror("خطأ", "فشل في حذف التصنيف. يرجى التحقق من الاتصال بقاعدة البيانات.")
    def edit_category(self,category_data,main_window):
        self._category(main_window,"Edit Category",f"Edit Category: {category_data['name']}","Update Category","update",category_data['id'])

    def categories(self,sample_categories=None):
        print(self._main_categories_frame,"checking existing frame")
        if categories._main_categories_frame and categories._main_categories_frame.winfo_exists():
            categories._main_categories_frame.lift() 
            return categories._main_categories_frame
        
        main_frame, content_container = categories.GUI(self, "Categories")
        self._main_categories_frame = main_frame
        print(self._main_categories_frame,"checking existing frame")
        if sample_categories is None:
            Label(content_container,text="No Categories yet !",background='lightblue',font=('Times New Roman',24)).pack(pady=200)
            
        else:
            scrollbar = Scrollbar(content_container,orient=VERTICAL)
            scrollbar.pack(side=LEFT, fill=Y) 
            scrollable_canvas = Canvas(content_container, yscrollcommand=scrollbar.set,background='lightblue',border=0,highlightthickness=0)
            scrollable_canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.config(command=scrollable_canvas.yview)
            categories_frame = Frame(scrollable_canvas,background='lightblue')
            window_id = scrollable_canvas.create_window((0, 0), window=categories_frame, anchor="nw")        
            categories_frame.bind("<Configure>",lambda e: scrollable_canvas.configure(scrollregion=scrollable_canvas.bbox("all")))

            def on_canvas_configure(event):
                scrollable_canvas.itemconfig(window_id, width=event.width)
                scrollable_canvas.configure(scrollregion=scrollable_canvas.bbox("all"))

            scrollable_canvas.bind('<Configure>', on_canvas_configure)        
            for index, category in enumerate(sample_categories):
                card = self.create_category_card(categories_frame, category,main_frame) 
                card.pack(pady=5, padx=30, anchor='w')
                
            self.general_button(main_frame,"Add Category",370,520,command_func=lambda:self._category(main_frame,"add category","Add category","Add Category","add"))
            self.general_button(main_frame,"back",200,520,command_func=lambda:main_frame.destroy())
        main_frame.mainloop()
        return main_frame
    
    
    def category(self,category_data):
        main_frame, content_container = self.GUI(f"Category: {category_data['name']}")
        describe=category_data['description']
        Label(content_container, text=f"Welcome to the {category_data['name']} page!", font=('Times New Roman', 20), bg='lightblue').pack(pady=50)
        Label(content_container, text=describe, font=('Times New Roman', 16), bg='lightblue').pack(pady=20)
        def go_back(current_frame):
            current_frame.destroy()
            self.categories(self.sample_categories)

        self.general_button(main_frame, "Back to Categories", 40, 520,command_func=lambda: go_back(main_frame))
        
    
    
    


