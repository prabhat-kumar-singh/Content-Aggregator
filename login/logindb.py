import sqlite3 as sql
from helper import *
from tkinter import *
from tkinter import messagebox
from home import news_feed

connection = sql.connect('user.db')

#create cursor
c = connection.cursor()

create_user_table = '''
CREATE TABLE IF NOT EXISTS USER(
    email_id TEXT,
    user_name TEXT,
    password TEXT,
    is_admin INT,
    PRIMARY KEY(email_id)
);
'''

#create user table
c.execute(create_user_table)

# sign_up(c, "hello123@gmail.com", "Prince", "12345", 0)
# print(login(c, 'hello123@gmail.com', '12345').fetchall())

# users = get_users(c)
# print(users.fetchall())


# You should use .withdraw() and .deiconify() to make it hide or show.

root = Tk()
def txt(root, text):
    return Label(root, text = text)

def entry_box(root):
    return Entry(root)

has_logged_in = False
has_signed_up = False

#Check whether user has already an account or not
def login_checker(email, password):
    #call login function from helper
    global has_logged_in

    if email and password:
        has_logged_in = login(c, email, password)
        if bool(has_logged_in.fetchall()):
            print("Loading.....")
            news_feed(email)
        else:
            #Show password or email missing error
            messagebox.showerror(title = "Error", message = "Please Check your email id/password :)")
    else:
        messagebox.showerror(title = "Error", message = "Kindly fill all the entries")
    

#Enter user details in the database if provided
def signup_checker(email, name, password):
    if email and name and password:
        has_signed_up = sign_up(c, email, name, password)
        if has_signed_up:
            connection.commit()
            print("Loading.....")
            news_feed(email)
            connection.close()
        else:
            messagebox.showwarning(title = "warning", message = "EmailId Already Exists")
    else:
        messagebox.showwarning(title = "warning", message = "Kindly Fill all the entries")

#Window where user can login with their account
def open_login_menu():
    root.title("LogIn Page")
    root.geometry("500x700")

    # make the top right close button minimize (iconify) the main window

    # root.protocol("WM_DELETE_WINDOW", root.iconify)
    # # make Esc exit the program
    # root.bind('<Escape>', lambda e: root.destroy())

    header = txt(root, "LogIn Here")
    header.grid(row = 0, columnspan = 2)

    header_two = txt(root, "WELCOME TO TDC")
    header_two.grid(row = 1, columnspan = 2)

    email = txt(root, "Email: ")
    password = txt(root, "Password:")

    email.grid(row = 3, column = 0)
    password.grid(row = 4, column = 0)

    email_entry = entry_box(root)
    password_entry = entry_box(root)

    email_entry.grid(row = 3, column = 1)
    password_entry.grid(row = 4, column = 1)

    login_btn = Button(root, text = "Login", padx = 30, pady = 15, command = lambda: login_checker(email_entry.get(), password_entry.get()))
    login_btn.grid(row = 5, column = 1)

    root.mainloop()

#Window where new user can sign in 
def open_signup_menu():
    root.title("Signup Page")
    root.geometry("500x700")

    # make the top right close button minimize (iconify) the main window
    
    # root.protocol("WM_DELETE_WINDOW", root.iconify)
    # # make Esc exit the program
    # root.bind('<Escape>', lambda e: root.destroy())

    header = txt(root, "Signup Here")
    header.grid(row = 0, columnspan = 2)

    header_two = txt(root, "WELCOME TO TDC")
    header_two.grid(row = 1, columnspan = 2)
    
    name = txt(root, "Name: ")
    email = txt(root, "Email: ")
    password = txt(root, "Password:")
    
    name.grid(row = 2, column = 0)
    email.grid(row = 3, column = 0)
    password.grid(row = 4, column = 0)

    name_entry = entry_box(root)
    email_entry = entry_box(root)
    password_entry = entry_box(root)

    name_entry.grid(row = 2, column = 1)
    email_entry.grid(row = 3, column = 1)
    password_entry.grid(row = 4, column = 1)

    signup_btn = Button(root, text = "Signup", padx = 30, pady = 15, command = lambda: signup_checker(email_entry.get(), name_entry.get(), password_entry.get()))
    signup_btn.grid(row = 5, column = 1)

    root.mainloop()    

def open_user_details():
    root.title("Users")
    root.geometry("300x500")

    txt(root, "Email").grid(row = 0, column = 0)    #email
    txt(root, "Name").grid(row = 0, column = 1)     #name   
    txt(root, "Is_Admin").grid(row = 0, column = 2)

    for i, user in enumerate(get_users(c)):
        txt(root, user[0]).grid(row = i+1, column = 0)    #email
        txt(root, user[1]).grid(row = i+1, column = 1)    #name   
        txt(root, user[2]).grid(row = i+1, column = 2)    #is_admin

# connection.commit()

# #Close the connection
# if has_logged_in or has_signed_up:
#     connection.close()