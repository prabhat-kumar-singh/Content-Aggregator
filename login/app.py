from tkinter import *
from logindb import open_login_menu, open_signup_menu, open_user_details

root = Tk()
root.title("TDC")
root.geometry("500x700")


# make the top right close button minimize (iconify) the main window
# root.protocol("WM_DELETE_WINDOW", root.iconify)
# make Esc exit the program
# root.bind('<Escape>', lambda e: root.destroy())


msg = Label(root, text = "Welcome to TDC")
login_btn = Button(root, text = "LogIn Here...", padx = 30, pady = 15, command = open_login_menu)

msg_one = Label(root, text = "Already have an account ?")
signup_btn = Button(root, text = "Sign Up", padx = 43, pady = 15, command = open_signup_menu)

user_detail = Label(root, text = "Get User Details")
user_btn = Button(root, text = "Get User Details", padx = 43, pady = 15, command = open_user_details)

msg.pack()
login_btn.pack()
msg_one.pack()
signup_btn.pack()
user_detail.pack()
user_btn.pack()


root.mainloop()