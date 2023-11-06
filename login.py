from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

# Functions
def login():
    if usernameEntry.get()=='' or passwordEntry=='':
        messagebox.showerror('Error','All fields are required')
    elif usernameEntry.get()=='admin' and passwordEntry.get()=='admin':
        messagebox.showinfo('Success','Welcome to the student management system')
        window.destroy()
        import sms
        
    else:
        messagebox.showerror('Error','Please enter correct credentials')


# GUI
window=Tk()
window.geometry('1200x785+90+0')
window.resizable(False,False)
window.title('Login System Of Student Management System')
backgroundImage=ImageTk.PhotoImage(file='bg.jpg')
bglabel=Label(window,image=backgroundImage)
bglabel.place(x=0,y=0)

# loginFrame
loginFrame=Frame(window,bg='alice blue')
loginFrame.place(x=500,y=200)

# login logo
logoImage=PhotoImage(file='profile.png')
logoLabel=Label(loginFrame,image=logoImage,bg='alice blue')
logoLabel.grid(row=0,column=0,columnspan=2,pady=10)

# login username
usernameImage=PhotoImage(file='user.png')
usernameLabel=Label(loginFrame,image=usernameImage,text=' Username',compound=LEFT,font=('times new roman',20,'bold'),bg='alice blue')
usernameLabel.grid(row=1,column=0,pady=10,padx=20)
usernameEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royal blue')
usernameEntry.grid(row=1,column=1,pady=10,padx=20)

# login passowrd
passwordImage=PhotoImage(file='security.png')
passwordLabel=Label(loginFrame,image=passwordImage,text=' Password',compound=LEFT,font=('times new roman',20,'bold'),bg='alice blue')
passwordLabel.grid(row=2,column=0,pady=10,padx=20)
passwordEntry=Entry(loginFrame,font=('times new roman',20,'bold'),bd=5,fg='royalblue')
passwordEntry.grid(row=2,column=1,pady=10,padx=20)

# login button
loginButton=Button(loginFrame,text='Login',font=('times new roman',15,'bold'),width=15,fg='white',bg='cornflowerblue',activebackground='cornflowerblue',activeforeground='white',cursor='hand2',command=login)
loginButton.grid(row=3,columnspan=2,pady=10)

window.mainloop()