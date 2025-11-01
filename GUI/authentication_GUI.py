from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import bcrypt
from main_GUI import Home
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from logic.authentication_logic import Register_Button, LogIn_Button
from logic.verification_logic import verify_user_code
from logic.reset_password import request_password_reset_logic,reset_password_logic

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
        open_verification_window(email_var)
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

def handle_login(email_var, password_var, login_frame):
    try:
        success, user_data,verify_status = LogIn_Button(email_var, password_var)
        if success:
            if verify_status == 0:
                login_frame.destroy()
                open_verification_window(email_var)
                
            elif verify_status == 1:
                login_frame.destroy()
                Home(user_data)
    except Exception as e:
        messagebox.showerror("Error", "An error occurred during login.")
        print(f"Login error: {e}")

def logIn_Button(logIn_frame,frame,email_var, password_var):
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
    button=ttk.Button(logIn_frame,text='Log In',style='Rounded.TButton',command=lambda: handle_login(email_var, password_var, frame))
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

def create_clickable_label(parent_frame,name,x,y,command):
    clickable_label = Label(
        parent_frame,
        text=name,
        fg="black",         
        cursor="hand2",    
        font =('Times New Roman',12)
    )
    clickable_label.place(x=x,y=y)
    clickable_label.bind("<Button-1>", command)
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
    logIn_Button(logIn_frame,frame,email_var,password_var)
    sign_up_Button(logIn_frame,frame)
    create_clickable_label(frame,"Forget Password ?",200,520)
    frame.mainloop()

def handle_verify(email, code_var, verification_frame):
    code = code_var.get()
    if not code:
        messagebox.showerror("خطأ", "الرجاء إدخال كود التحقق.")

    result = verify_user_code(email, code, 'registration')
    if result is None:
        messagebox.showerror("خطأ", "فشل التحقق. لم يتم العثور على بيانات المستخدم.")
    elif result is True:
        messagebox.showinfo("نجاح", "تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.")
        verification_frame.destroy()
        Log_in() 
    elif result is False:
        messagebox.showerror("خطأ", "كود التحقق غير صحيح أو انتهت صلاحيته.")

def open_verification_window(email_var):
    frame=Tk()
    frame['bg'] = 'lightblue'
    frame.geometry("400x400+500+200")
    frame.title("Verification")
    inner_frame = LabelFrame(frame,text="Verification",font=('Times New Roman', 40),bg='lightblue',fg='black')
    inner_frame.pack(fill=BOTH,expand=1,padx=40,pady=40)
    code = StringVar()
    general_lable(inner_frame,"Enter The code:",40,40)    
    general_entry(inner_frame,code,40,90)
    general_button(inner_frame,'Verify',90,140,"",40,200,command_func=lambda: handle_verify(email_var,code,frame))

    general_button(inner_frame,'close',150,140,"",40,200,command_func=lambda: switch_to_register(frame))

    create_clickable_label(inner_frame,"didnt recive ? resend again",80,190 ,command_func=lambda e: [frame.destroy(), Forget_Password_GUI()])
    frame.mainloop()
    
#-----------------------FORGET PASSWORD --------------------------

def Forget_Password_GUI():
    """واجهة لطلب البريد الإلكتروني لبدء عملية إعادة التعيين."""
    frame, inner_frame = GUI("Forget Password")
    
    email_var = StringVar()
    
    general_lable(inner_frame, "Enter Your Email:", 40, 40)
    general_entry(inner_frame, email_var, 40, 90)

    def handle_request():
        email = email_var.get().strip()
        if not email:
            messagebox.showerror("خطأ", "الرجاء إدخال البريد الإلكتروني.")
            return

        # استدعاء منطق طلب إعادة التعيين (سيُضاف في الخطوة 2)
        success, message = request_password_reset_logic(email)
        
        if success:
            messagebox.showinfo("نجاح", "تم إرسال كود التحقق إلى بريدك الإلكتروني.")
            frame.destroy()
            Reset_Password_GUI(email_var)  
        else:
            messagebox.showerror("خطأ", message)

    request_button = Button(inner_frame, text="Request Reset Code", 
                            font=('Times New Roman', 18), bg='darkblue', fg='white',
                            command=handle_request)
    request_button.place(x=40, y=140)
    
    frame.mainloop()

def Reset_Password_GUI(email_var):
    """واجهة لإدخال كود التحقق وكلمة المرور الجديدة."""
    email = email_var.get().strip()
    frame, inner_frame = GUI("Reset Password")
    
    code_var = StringVar()
    new_password_var = StringVar()
    
    general_lable(inner_frame, "Verification Code:", 40, 40)
    general_entry(inner_frame, code_var, 40, 90)

    general_lable(inner_frame, "New Password:", 40, 140)
    general_entry(inner_frame, new_password_var, 40, 190)

    def handle_reset():
        code = code_var.get().strip()
        new_password = new_password_var.get()
        
        if not all([code, new_password]):
            messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول.")
            return
            
        # استدعاء منطق إعادة التعيين (سيُضاف في الخطوة 2)
        success, message = reset_password_logic(email, code, new_password)
        
        if success:
            messagebox.showinfo("نجاح", "تم تغيير كلمة المرور بنجاح! يمكنك الآن تسجيل الدخول.")
            frame.destroy()
            Log_in() # العودة إلى شاشة تسجيل الدخول
        else:
            messagebox.showerror("خطأ", message)

    reset_button = Button(inner_frame, text="Reset Password", 
                          font=('Times New Roman', 18), bg='darkred', fg='white',
                          command=handle_reset)
    reset_button.place(x=40, y=240)
    
    frame.mainloop()


