from tkinter import *
from tkinter import ttk
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
    categories_button = navbar_buttons(navbar_frame,"Categories",lambda: switch_content("Categories"))
    authors_button = navbar_buttons(navbar_frame,"Authors",lambda: switch_content("Authors"))
    titles_button= navbar_buttons(navbar_frame,"Titles",lambda: switch_content("Titles"))
    general_entry(navbar_frame,search_key)
    general_lable(navbar_frame,"Search:")    

def show_latest_books(content_frame, latest_books): 
    
    for widget in content_frame.winfo_children():
        widget.destroy()

    Label(content_frame, text="Lastest Books", font=('Times New Roman', 24, 'underline'), bg='lightblue').pack(pady=10)

    books_container = Frame(content_frame, bg='lightblue')
    books_container.pack(pady=10, padx=10)
    
    COLUMNS = 5 
    
    if latest_books:
        for index, book in enumerate(latest_books):
            row = index // COLUMNS  
            column = index % COLUMNS 
            
            card = create_book_card(books_container, book) 
            card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')
            books_container.grid_columnconfigure(column, weight=1)
            
    else:
        Label(content_frame, text="لا توجد كتب متاحة حالياً.", font=('Times New Roman', 18), bg='lightblue').pack(pady=50)

def create_book_card(parent_frame, book_data):
    CARD_WIDTH = 200  
    CARD_HEIGHT = 200
    card = Frame(parent_frame, bg='#F0F0F0',  bd=1, relief=GROOVE, width=CARD_WIDTH, height=CARD_HEIGHT)
    card.pack_propagate(False)
    title_label=Label(card, text=book_data['title'], font=('Times New Roman', 14, 'bold'),cursor="hand2",wraplength=100, bg='#F0F0F0')
    title_label.pack(pady=5)
    title_label.bind("<Button-1>",lambda e:show_book_details_view (parent_frame, book_data) )
    title_label.bind("<Enter>", lambda event: title_label.config(fg="red"))
    title_label.bind("<Leave>", lambda event: title_label.config(fg="blue")) 
    Label(card, text=f"الكاتب: {book_data['author']}", font=('Times New Roman', 12),wraplength=100, bg='#F0F0F0').pack()
    Label(card, text=f"النوع: {book_data['type']} | التصنيف: {book_data['category']}",wraplength=150,font=('Times New Roman', 10), bg='#F0F0F0').pack()
    
    return card

def show_book_details_view(parent_frame, book_details):
    """
    تنظف الإطار وتنشئ واجهة عرض تفاصيل الكتاب.
    (تستقبل البيانات جاهزة ولا تتصل بقاعدة البيانات).
    """
    
    for widget in parent_frame.winfo_children():
        widget.destroy()
        
    if not book_details:
        Label(parent_frame, text="خطأ في عرض البيانات: تفاصيل الكتاب غير متوفرة.", font=('Times New Roman', 18)).pack(pady=50)
        return

    book = book_details
    
    details_frame = Frame(parent_frame, bg='lightblue', padx=20, pady=20)
    details_frame.pack(fill=BOTH, expand=1)

    details_frame.grid_columnconfigure(0, weight=1) 
    details_frame.grid_columnconfigure(1, weight=1) 
    details_frame.grid_columnconfigure(2, weight=4) 

    
    Button(
        details_frame, text="Back", 
        # command=go_back_command, 
        font=('Times New Roman', 12), bg='#555555', fg='white'
    ).grid(row=0, column=0, sticky='nw', padx=10, pady=10)
    
    cover_frame = Frame(details_frame, width=150, height=200, bg='#CCCCCC', bd=2, relief=SUNKEN)
    cover_frame.grid(row=1, column=0, sticky='n', padx=10, pady=20)
    Label(cover_frame, text="صورة الغلاف", bg='#CCCCCC').pack(expand=True, fill=BOTH)

    info_frame = Frame(details_frame, bg='lightblue')
    info_frame.grid(row=1, column=1, sticky='nwe', padx=10, pady=20)

    Label(info_frame, text=book['title'], font=('Times New Roman', 22, 'bold'), bg='lightblue', wraplength=200).pack(anchor='w', pady=5)
    Label(info_frame, text=f"الكاتب: {book['author']}", font=('Times New Roman', 16), bg='lightblue').pack(anchor='w')
    if book.get('translator'):
        Label(info_frame, text=f"المترجم: {book['translator']}", font=('Times New Roman', 14), bg='lightblue').pack(anchor='w')
    if book.get('page_count'):
        Label(info_frame, text=f"عدد الصفحات: {book['page_count']}", font=('Times New Roman', 14), bg='lightblue').pack(anchor='w')
    
    Button(info_frame, text="📎 open the pdf", command=lambda: print(f"Opening PDF: "),font=('Times New Roman', 14), bg='#0D0050', fg='white').pack(anchor='w', pady=15)
    

    description_frame = Frame(details_frame, bg='#EEEEEE', bd=1, relief=FLAT)
    description_frame.grid(row=0, column=2, rowspan=2, sticky='nsew', padx=10, pady=10)
    if book.get('page_count'):
        Label(description_frame, text="Discription", font=('Times New Roman', 18, 'underline'), bg='#EEEEEE').pack(pady=10)
        scrollbar = Scrollbar(description_frame)
        scrollbar.pack(side=LEFT, fill=Y) 

        description_text = Text(description_frame, wrap=WORD, font=('Times New Roman', 12), bg='#EEEEEE', bd=0, yscrollcommand=scrollbar.set)
        description_text.insert(END, book['description']) 
        description_text.config(state=DISABLED) 
        description_text.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=5)
        scrollbar.config(command=description_text.yview)


def books():
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
    show_latest_books(frame,latest_books)
    
    main_window.mainloop()

books()