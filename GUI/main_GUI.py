from tkinter import *
from tkinter import ttk
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from categories_GUI import categories
from logic.category_logic import LO_categories
sample_categories=categories().sample_categories
def GUI(name):
    frame=Tk()
    frame['bg'] = 'lightblue'
    frame.geometry("1000x700+200+50")
    frame.title(name)
    inner_frame = LabelFrame(frame,text=name,font=('Times New Roman', 50),bg='lightblue',fg='black')
    inner_frame.pack(fill=BOTH,expand=1,padx=40,pady=50)

    return frame,inner_frame
def general_lable(frame,text):
    lable= Label(frame,text=text,background='lightblue',font=('Times New Roman',18))
    lable.pack(side=RIGHT, padx=10, pady=5)

def general_entry(frame,search):
    entry = Entry(frame,textvariable=search,justify=CENTER,font=('Times New Roman',14))
    entry.pack(side=RIGHT, padx=30, pady=5)

def navbar_buttons(navbar_frame,text,command_func):
    button=Button(navbar_frame,text=text,font=('Times New Roman',14),command=command_func,bg="#605C5C", fg='white', relief=FLAT, padx=15, pady=5)
    button.pack(side=LEFT, padx=10, pady=5)

def navbar(main_window):
    search_key = StringVar()
    navbar_frame = Frame(main_window, bg="#0D0050", height=50) 
    navbar_frame.place(width=1000, height=50, x=0, y=0)
    
    
    def switch_content(view_name):
        print(f"Switching to view: {view_name}")

    home_button = navbar_buttons(navbar_frame,"Home",lambda: switch_content("Home"))
    categories_button = navbar_buttons(navbar_frame,"Categories",lambda:open_category())
    authors_button = navbar_buttons(navbar_frame,"Authors",lambda: switch_content("Authors"))
    titles_button= navbar_buttons(navbar_frame,"Titles",lambda: switch_content("Titles"))
    general_entry(navbar_frame,search_key)
    general_lable(navbar_frame,"Search:")    

def open_category():
    save_frame=categories().categories(LO_categories().get_all_categories())
    
    
def Home():
    latest_books = [
            {'title': 'مقدمة في الفيزياء', 'author': 'أحمد علي', 'category': 'علمي', 'type': 'Scientific Book'},
            {'title': 'رواية مدينة الرياح', 'author': 'سارة محمد', 'category': 'أدب', 'type': 'Novel'},
            {'title': 'فلسفة العقل الحديث', 'author': 'خالد ناصر', 'category': 'فلسفة', 'type': 'Article'},
            {'title': 'مقدمة في الفيزياء', 'author': 'أحمد علي', 'category': 'علمي', 'type': 'Scientific Book'},
            {'title': 'رواية مدينة الرياح', 'author': 'سارة محمد', 'category': 'أدب', 'type': 'Novel'},
            {'title': 'فلسفة العقل الحديث', 'author': 'خالد ناصر', 'category': 'فلسفة', 'type': 'Article'},
        ]
    main_window,frame=GUI('Our Books')
    navbar_= navbar(main_window)
    
    main_window.mainloop()

Home()