from operator import add
from tkinter import *
from tkinter import ttk
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__)) 
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

class control_books():
    def GUI(seld,name):
        frame=Tk()
        frame['bg'] = 'lightblue'
        frame.geometry("1000x700+200+50")
        frame.title(name)
        inner_frame = LabelFrame(frame,text=name,font=('Times New Roman', 50),bg='lightblue',fg='black')
        inner_frame.pack(fill=BOTH,expand=1,padx=40,pady=50)
        return frame,inner_frame
    
    def general_lable(self,frame,text,x,y):
        lable= Label(frame,text=text,background='lightblue',font=('Times New Roman',24))
        lable.place(x=x,y=y)

    def general_entry(self,frame,variable,x,y):
        entry = Entry(frame,textvariable=variable,justify=CENTER,font=('Times New Roman',18))
        entry.place(x=x, y=y)


    def add_book(self):
        frame,inner_frame=self.GUI("Add Book")
        self.general_lable(inner_frame,"Title:",100,50)
        frame.mainloop()

control_books().add_book()

