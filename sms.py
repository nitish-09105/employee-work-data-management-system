import time
from tkinter import *
import ttkthemes
from tkinter import ttk,messagebox,filedialog
import pymysql,pandas

# **********************************************************************************************************************************************

# functionality

# exit button function
def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass

# save data 
def export_data():
    url=filedialog.asksaveasfilename(defaultextension='.csv')
    indexing=studentTable.get_children()
    newlist=[]
    for index in indexing:
        content=studentTable.item(index)
        datalist=content['values']
        newlist.append(datalist)
    table=pandas.DataFrame(newlist,columns=['Id','Name','Mobile','Email','Address','Gender','DOB','Added Date','Added Time'])
    table.to_csv(url,index=False)
    messagebox.showinfo('Success','Data is saved successfully')


# gui for update search and add button
def toplevel_data(title,button_text,command):
    global idEntry,phoneEntry,nameEntry,emailEntry,addressEntry,genderEntry,dobEntry,screen
    screen=Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(0,0)
    
    idLabel=Label(screen,text='Id',font=('times new roman',28,'bold'))
    idLabel.grid(padx=30,pady=15,sticky=W)
    idEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    idEntry.grid(row=0,column=1,pady=15,padx=10)

    nameLabel=Label(screen,text='Name',font=('times new roman',28,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15,sticky=W)
    nameEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    nameEntry.grid(row=1,column=1,pady=15,padx=10)

    phoneLabel=Label(screen,text='Phone',font=('times new roman',28,'bold'))
    phoneLabel.grid(row=2,column=0,padx=30,pady=15,sticky=W)
    phoneEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    phoneEntry.grid(row=2,column=1,pady=15,padx=10)

    emailLabel=Label(screen,text='Email',font=('times new roman',28,'bold'))
    emailLabel.grid(row=3,column=0,padx=30,pady=15,sticky=W)
    emailEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    emailEntry.grid(row=3,column=1,pady=15,padx=10)

    addressLabel=Label(screen,text='Address',font=('times new roman',28,'bold'))
    addressLabel.grid(row=4,column=0,padx=30,pady=15,sticky=W)
    addressEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    addressEntry.grid(row=4,column=1,pady=15,padx=10)

    genderLabel=Label(screen,text='Gender',font=('times new roman',28,'bold'))
    genderLabel.grid(row=5,column=0,padx=30,pady=15,sticky=W)
    genderEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    genderEntry.grid(row=5,column=1,pady=15,padx=10)

    dobLabel=Label(screen,text='D.O.B',font=('times new roman',28,'bold'))
    dobLabel.grid(row=6,column=0,padx=30,pady=15,sticky=W)
    dobEntry=Entry(screen,font=('roman',15,'bold'),width=24)
    dobEntry.grid(row=6,column=1,pady=15,padx=10)

    student_button=ttk.Button(screen,text=button_text,command=command)
    student_button.grid(row=7,columnspan=2,pady=15,padx=10)

    # run only when update button will clicked
    if title=='Update_Student':
        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        listdata=content['values']
        idEntry.insert(0,listdata[0])
        nameEntry.insert(0,listdata[1])
        phoneEntry.insert(0,listdata[2])
        emailEntry.insert(0,listdata[3])
        addressEntry.insert(0,listdata[4])
        genderEntry.insert(0,listdata[5])
        dobEntry.insert(0,listdata[6])



# update data button function
def update_data():
    query='update student set name=%s, mobile=%s,email=%s,address=%s,dob=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),dobEntry.get(),date,currenttime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',f'Id {idEntry.get()} is modified successfully',parent=screen)
    screen.destroy()
    show_student()


# show student button function
def show_student():
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)


# delete student button function
def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,content_id)
    con.commit()
    messagebox.showinfo('Deleted',f'Id {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)


# search student button functions
def search_data():
    query = 'SELECT * FROM student WHERE id=%s OR name=%s OR mobile=%s OR email=%s OR address=%s OR gender=%s OR dob=%s'
    mycursor.execute(query, (idEntry.get(), nameEntry.get(), phoneEntry.get(), emailEntry.get(), addressEntry.get(), genderEntry.get(), dobEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', 'end', values=data) 


# add student button function
def add_data():
    if idEntry.get()=='' or nameEntry.get()==''or phoneEntry.get()==''or emailEntry.get()==''or addressEntry.get()==''or genderEntry.get()==''or dobEntry.get()=='':
        messagebox.showerror('Error','All fields are required',parent=screen)
    else:    
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),phoneEntry.get(),emailEntry.get(),addressEntry.get(),genderEntry.get(),dobEntry.get(),date,currenttime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully, Do you want to clean the form?',parent=screen)
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                phoneEntry.delete(0,END)
                emailEntry.delete(0,END)
                addressEntry.delete(0,END)
                genderEntry.delete(0,END)
                dobEntry.delete(0,END)
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        
        query='select * from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            data_list=list(data)
            studentTable.insert('',END,values=data_list)


# database connection
def connect_database():

    def connect():
        global mycursor,con
        try:        
            con=pymysql.connect(host=hostEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Invalid Details',parent=connectWindow)
            return
        
        try:
            query='create database studentmanagementsystem'
            mycursor.execute(query)
            query='use studentmanagementsystem'
            mycursor.execute(query)
            query='create table student(id int not null primary key,name varchar(30),mobile varchar(10),email varchar(30),address varchar(100),gender varchar(20),dob varchar(20),date varchar(50),time varchar(50))'
            mycursor.execute(query)
        except:
            query='use studentmanagementsystem'
            mycursor.execute(query)
        messagebox.showinfo('Success','Database Connection is Successful',parent=connectWindow)
        connectWindow.destroy()
        addstudentButton.config(state=NORMAL)
        searchstudentButton.config(state=NORMAL)
        deletestudentButton.config(state=NORMAL)
        updatestudentButton.config(state=NORMAL)
        showstudentButton.config(state=NORMAL)
        ExportdataButton.config(state=NORMAL)
        

    # database connection gui
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('500x300+500+200')
    connectWindow.resizable(False,False)
    connectWindow.title('Database Connection')

    hostnameLabel=Label(connectWindow,text='Host Name',font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)
    hostEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    hostEntry.grid(row=0,column=1,padx=40,pady=20)

    usernameLabel=Label(connectWindow,text='User Name',font=('arial',20,'bold'))
    usernameLabel.grid(row=1,column=0,padx=20)
    usernameEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    usernameEntry.grid(row=1,column=1,padx=40,pady=20)
    
    passwordLabel=Label(connectWindow,text='Password',font=('arial',20,'bold'))
    passwordLabel.grid(row=2,column=0,padx=20)
    passwordEntry=Entry(connectWindow,font=('roman',15,'bold'),bd=2)
    passwordEntry.grid(row=2,column=1,padx=40,pady=20)

    connectButton=ttk.Button(connectWindow,text='CONNECT',command=connect)
    connectButton.grid(row=3,columnspan=2,padx=20,pady=20)


# Heading slider funtion
count=0
text=''
def slider():
    global text,count
    if count==len(s):
        count=0
        text=''
    text=text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(100,slider)

# clock function
def clock():
    global currenttime,date
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'   Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000,clock)

# *********************************************************************************************************************************************

# GUI
root=ttkthemes.ThemedTk()
root.get_themes()

root.set_theme('radiance')
root.geometry('1200x785+90+0')
root.resizable(False,False)
root.title('Student Management System')

# date and time
datetimeLabel=Label(root,font=('times new roman',18,'bold'),foreground='dark blue')
datetimeLabel.place(x=5,y=5)
clock()

# slider
s='Student Management System'
sliderLabel=Label(root,text=s,font=('arial',28,'italic bold'),width=30,foreground='dark red')
sliderLabel.place(x=300,y=0)
slider()
# connect button
connectButton=ttk.Button(root,text='connect Database',command=connect_database)
connectButton.place(x=1000,y=5)

# left frame
leftFrame=Frame(root)
leftFrame.place(x=60,y=90,width=300,height=800)
# logo
logo_image=PhotoImage(file='student.png')
logo_Label=Label(leftFrame,image=logo_image)
logo_Label.grid(row=0,column=0)
# 1
addstudentButton=ttk.Button(leftFrame,text='Add Student',width=25,state=DISABLED,command=lambda:toplevel_data('Add Student', 'ADD',add_data))
addstudentButton.grid(row=1,column=0,pady=25)
# 2
searchstudentButton=ttk.Button(leftFrame,text='Search Student',width=25,state=DISABLED,command=lambda:toplevel_data('Search Student', 'SEARCH',search_data))
searchstudentButton.grid(row=2,column=0,pady=25)
# 3
deletestudentButton=ttk.Button(leftFrame,text='Delete Student',width=25,state=DISABLED,command=delete_student)
deletestudentButton.grid(row=3,column=0,pady=25)
# 4
updatestudentButton=ttk.Button(leftFrame,text='Update Student',width=25,state=DISABLED,command=lambda:toplevel_data('Update_Student', 'UPDATE',update_data))
updatestudentButton.grid(row=4,column=0,pady=25)
# 5
showstudentButton=ttk.Button(leftFrame,text='Show Student',width=25,state=DISABLED,command=show_student)
showstudentButton.grid(row=5,column=0,pady=25)
# 6
ExportdataButton=ttk.Button(leftFrame,text='Export Data',width=25,state=DISABLED,command=export_data)
ExportdataButton.grid(row=6,column=0,pady=25)
# 7
exitButton=ttk.Button(leftFrame,text='Exit',width=25,command=iexit)
exitButton.grid(row=7,column=0,pady=25)


# right frame
rightFrame=Frame(root)
rightFrame.place(x=380,y=90,width=820,height=690)

ScrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
ScrollBarY=Scrollbar(rightFrame)

studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Mobile','Email','Address','Gender','D.O.B','Added Date','Added Time'),xscrollcommand=ScrollBarX.set,yscrollcommand=ScrollBarY.set)

ScrollBarX.config(command=studentTable.xview)
ScrollBarY.config(command=studentTable.yview)
ScrollBarX.pack(side=BOTTOM,fill=X)
ScrollBarY.pack(side=RIGHT,fill=Y)
studentTable.pack(fill=BOTH,expand=1)

studentTable.heading('Id',text='Id')
studentTable.heading('Name',text='Name')
studentTable.heading('Mobile',text='Mobile No.')
studentTable.heading('Email',text='Email')
studentTable.heading('Address',text='Address')
studentTable.heading('Gender',text='Gender')
studentTable.heading('D.O.B',text='D.O.B')
studentTable.heading('Added Date',text='Added Date')
studentTable.heading('Added Time',text='Added Time')

studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=200,anchor=CENTER)
studentTable.column('Mobile',width=200,anchor=CENTER)
studentTable.column('Email',width=200,anchor=CENTER)
studentTable.column('Address',width=200,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=150,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=150,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),background='gray90',fieldbackground='gray90')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='dark red')


studentTable.config(show='headings')
root.mainloop()