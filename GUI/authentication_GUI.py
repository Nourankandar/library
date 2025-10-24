from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import bcrypt
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
# =========================================================
from logic.authentication_logic import Register_Button, LogIn_Button

def GUI(name):
    frame=Tk()
    frame['bg'] = 'lightblue'
    frame.geometry("600x600+400+100")
    frame.title(name)
    inner_frame = LabelFrame(frame,text=name,font=('Times New Roman', 50),bg='lightblue',fg='black')
    inner_frame.pack(fill=BOTH,expand=1,padx=40,pady=40)

    return frame,inner_frame

font=('Times New Roman',20)
def general_lable(frame,text,x,y):
    lable= Label(frame,text=text,background='lightblue',font=font)
    lable.place(x=x,y=y)

def general_entry(frame,variable,x,y):
    entry = Entry(frame,textvariable=variable,justify=CENTER,font=('Times New Roman',18))
    entry.place(x=x, y=y)

font1 =('Times New Roman',15)
def general_button(frame,buttontext,x,y,buttonlable,x1,y1,command_func):
    lable1= Label(frame,text=buttonlable,background='lightblue',font=font1)
    lable1.place(x=x1,y=y1)
    button=Button(frame,text=buttontext,font=font1,command=command_func)
    button.place(x=x,y=y)

def register_labels(register_frame):
    name = StringVar()
    email = StringVar() 
    password = StringVar()

    general_lable(register_frame,"Full Name:",100,30)    
    general_entry(register_frame,name,100,80)

    general_lable(register_frame,"Email:",100,130)
    general_entry(register_frame,email,100,180)

    general_lable(register_frame,"Password:",100,230)
    general_entry(register_frame,password,100,280)

    return name,email,password
def logIn_labels(logIn_frame):
    email = StringVar() 
    password = StringVar()
    general_lable(logIn_frame,"Email:",100,30)
    general_entry(logIn_frame,email,100,80)

    general_lable(logIn_frame,"Password:",100,130)
    general_entry(logIn_frame,password,100,180)
    return email,password

def handle_register(full_name_var, email_var, password_var,parent_frame):
    success = Register_Button(full_name_var, email_var, password_var)
    if success: 
        parent_frame.destroy()
        open_verification_window()
    else:
        pass
    
def register_Button(register_frame,full_name_var, email_var, password_var,parent_frame):
    style = ttk.Style()
    style.configure(
    'Rounded.TButton',
    background="#4E6A87",  
    foreground='black',
    font=('Times New Roman', 16, 'bold'),
    relief='flat',
    bordercolor='#1E90FF',
    lightcolor='#1E90FF',
    darkcolor='#1E90FF',
    padding=7
    )
    button=ttk.Button(register_frame,text='Register',style='Rounded.TButton',command=lambda: handle_register(full_name_var, email_var, password_var,parent_frame))
    button.place(x=170,y=320)
def logIn_Button(logIn_frame,email_var, password_var):
    style = ttk.Style()
    style.configure(
    'Rounded.TButton',
    background="#4E6A87",  
    foreground='black',
    font=('Times New Roman', 16, 'bold'),
    relief='flat',
    bordercolor='#1E90FF',
    lightcolor='#1E90FF',
    darkcolor='#1E90FF',
    padding=7
    )
    button=ttk.Button(logIn_frame,text='Log In',style='Rounded.TButton',command=lambda: LogIn_Button(email_var, password_var))
    button.place(x=170,y=250)

def switch_to_login(current_frame):
    current_frame.destroy()
    Log_in() 
def switch_to_register(current_frame):
    current_frame.destroy()
    Register()

def sign_in_Button(register_frame,frame):
    general_button(register_frame,'Log In',280,390,"you have an account?:",100,400,command_func=lambda:switch_to_login(frame))
    
def sign_up_Button(register_frame,frame):
    general_button(register_frame,'Sign Up',290,340,"Don't have an account?:",100,350,command_func=lambda: switch_to_register(frame))

def create_clickable_label(parent_frame,name,x,y):
    clickable_label = Label(
        parent_frame,
        text=name,
        fg="black",         
        cursor="hand2",    
        font =('Times New Roman',12)
    )
    clickable_label.place(x=x,y=y)
    clickable_label.bind("<Button-1>")
    clickable_label.bind("<Enter>", lambda event: clickable_label.config(fg="red"))
    clickable_label.bind("<Leave>", lambda event: clickable_label.config(fg="blue")) 

def Register():
    frame,register_frame=GUI('Register')
    full_name_var, email_var, password_var = register_labels(register_frame)
    register_Button(register_frame,full_name_var, email_var, password_var,frame)
    sign_in_Button(register_frame,frame)
    frame.mainloop()

def Log_in():
    frame,logIn_frame=GUI('Log In')
    email_var, password_var = logIn_labels(logIn_frame)
    logIn_Button(logIn_frame,email_var,password_var)
    sign_up_Button(logIn_frame,frame)
    create_clickable_label(frame,"Forget Password ?",200,520)
    frame.mainloop()
    
def open_verification_window():
    frame=Tk()
    frame['bg'] = 'lightblue'
    frame.geometry("400x400+500+200")
    frame.title("Verification")
    inner_frame = LabelFrame(frame,text="Verification",font=('Times New Roman', 40),bg='lightblue',fg='black')
    inner_frame.pack(fill=BOTH,expand=1,padx=40,pady=40)
    code = StringVar()
    general_lable(inner_frame,"Enter The code:",40,40)    
    general_entry(inner_frame,code,40,90)
    general_button(inner_frame,'Verify',90,140,"",40,200,command_func=lambda: switch_to_register(frame))
    create_clickable_label(inner_frame,"didnt recive ? resend again",80,190)
    frame.mainloop()
    

Register()



