from tkinter import *
from tkinter import ttk
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from categories_GUI import categories
from logic.category_logic import LO_categories
from authors_GUI import authors_Class
# sample_categories=categories().sample_categories
list_of_authers= authors_Class().list_of_authers
current_user_role=" "
current_user_id=0
current_user_role = 'guest' 
current_user_id = None
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
    authors_button = navbar_buttons(navbar_frame,"Authors",lambda: open_authors())
    titles_button= navbar_buttons(navbar_frame,"Titles",lambda: switch_content("Titles"))
    general_entry(navbar_frame,search_key)
    general_lable(navbar_frame,"Search:")    

def open_category():
    # global current_user_role
    print(current_user_role)
    categories().categories(LO_categories().get_all_categories(), current_user_role)
    
def open_authors():
    # global current_user_role
    authors_Class().authors_gui(list_of_authers,current_user_role)



def Home(user_data):
    global current_user_role 
    global current_user_id
    print(user_data)
    if user_data:
        current_user_role = user_data[1] 
        current_user_id = user_data[0]
        print(f"Logged in as: {current_user_role}")
    main_window,frame=GUI('Our Books')
    navbar(main_window)
    main_window.mainloop()

# Home()