import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
from helper import show_profile
import sqlite3


def fetch_path(path):
    # print("Path: ", path)
    #Fetch the description using above
    try:
        print("Fetching Data...")
        description = requests.get(path)
    except:
        messagebox.showerror(title = "Internet Connection", message="Please Check your internet connection/Unable to fetch data")
        
    soup = BeautifulSoup(description.text, 'html.parser')

    description_container = soup.find('div', {'class': 'description'})

    try:
        paragraph = description_container.find_all('p')
    except:
        paragraph = "Data Not Available"
    # print(paragraph)
    return paragraph
    
def get_data():
    url = "https://gadgets.ndtv.com/news/"

    try:
        print("Waiting....")
        res = requests.get(url)
    except:
        messagebox.showerror(title ="Internet Connection", message="Check your network connection/Couldn't fetch the data")

    soup = BeautifulSoup(res.text, 'html.parser')

    #Find tags
    div_container = soup.find('div', {'class': 'story_list'})

    #Select top 5
    count = 0
    heading = []
    path = []
    for li in div_container.find_all('span', {'class': 'news_listing'}):
        #Will contain the header with its link
        if count == 5:
            break
        
        heading.append(li.text)
        # print(heading, link.get('href'))
        count +=1 

    count = 0
    for link in div_container.find_all('a', {'class': None}):
        if count == 10:
            break

        path.append(link.get('href'))
        count+= 1

    # print(heading, path)
    return (heading, path)

def add_new_line(paragraph):
    'paragraph is a list of <p> tags'
    txt = ""

    #remove p tags from the string
    for p in paragraph:
        p = str(p)
        txt = txt + p[3: -4] + "\n"

    #Text With new Line character
    new_line = ""
    while txt:
        if len(txt)/80 > 0 and not(len(txt)<80):
            new_line += txt[:80] + "\n"
            txt = txt[80: ]
        else:
            new_line += txt
            txt = ""
    #Add "/n" at after every 80 characters
    # print(new_line)
    return new_line

def open_user_profile(email_id):
    connection = sqlite3.connect("user.db")
    c = connection.cursor()

    user = show_profile(c, email_id)
    #fetch email, name
    email, user_name, password, admin = user.fetchone()

    #Close the connection
    connection.close()
    
    prof_window = Tk()
    prof_window.title("Profile")
    prof_window.geometry("200x300")

    name = Label(prof_window, text = "Name: ")
    email_label = Label(prof_window, text = "Email Id: ")

    name_val = Label(prof_window, text = user_name)
    email_label_val = Label(prof_window, text = email)

    name.grid(row = 0, column = 0)
    name_val.grid(row = 0, column = 1)
    email_label.grid(row = 1, column = 0)
    email_label_val.grid(row = 1, column = 1)
    
    prof_window.mainloop()

def news_feed(email_id):
    window = Tk()
    window.title("News Feed")
    window.geometry("500x700")

    #make window scrollable

    #Add a main frame
    main_frame = Frame(window)
    main_frame.pack(fill = BOTH, expand = 1)

    #Create a canvas
    my_canvas = Canvas(main_frame)
    my_canvas.pack(side = LEFT, fill = BOTH, expand = 1)

    #Add a scrollbar to canvas
    my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
    my_scrollbar.pack(side = RIGHT, fill = Y)

    #Configure the canvas
    my_canvas.configure(yscrollcommand = my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

    #Create another frame Inside canvas
    second_frame = Frame(my_canvas)

    #Add that frame to a window in the Canvas
    my_canvas.create_window((0, 0), window = second_frame, anchor = "nw")

    # scrollbar = Scrollbar(window)
    # scrollbar.pack( side = RIGHT, fill = Y )
    # mylist = Listbox(window, width = 470 ,yscrollcommand = scrollbar.set )

    #Add menus - Home, Profile

    home_btn = Button(second_frame, text = "Home", relief = SUNKEN)
    home_btn.pack()

    profile_btn = Button(second_frame, text = "Profile", relief = SUNKEN, command = lambda: open_user_profile(email_id))
    profile_btn.pack()

    heading, path = get_data()

    index = [i for i in range(0, 11, 2)]
    for p, h in enumerate(heading):
        print(h, path[index[p]], end = " ")
        Label(second_frame, text = "Latest News").pack()
        Label(second_frame, text = "Heading").pack()
        Label(second_frame, text = h).pack()
        # mylist.insert(END, "Latest News")
        # mylist.insert(END, "Heading")
        # mylist.insert(END, h)

        paragraph = fetch_path(path[index[p]])

        #Add new line \n after every 80 characters in paragraph
        lines = add_new_line(paragraph)
        Label(second_frame, text = lines).pack(padx = 5)
        # mylist.insert(END, lines)

    # mylist.pack( side = LEFT, fill = BOTH )
    # scrollbar.config( command = mylist.yview )

    window.mainloop()

# news_feed()