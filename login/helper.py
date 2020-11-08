#Signup function
def sign_up(c, email_id, user_name, password, is_admin = 0):
    #Add user into the database
    try:
        values = (email_id, user_name, password, is_admin)
        print(f"INSERT INTO USER ( email_id, user_name, password, is_admin) VALUES ({email_id}, {user_name}, {password}, {is_admin})")
        c.execute("INSERT INTO USER (email_id, user_name, password, is_admin) VALUES (?, ?, ?, ?)", values)
    except Exception as e:
        print(f"Unable to add user into database, Please try again!{e}")
        return False
    else:
        return True


#get all the data from the database
def get_users(c):
    users = c.execute("SELECT email_id, user_name, is_admin FROM USER")
    #returns a tuple (email, name, is_admin)
    return users

#Login
def show_profile(c, email_id):
    user = c.execute("SELECT * FROM USER WHERE email_id = ?", (email_id,))
    return user

def login(c, email_id, password):
    try:
        has_logged_in = c.execute("SELECT * FROM USER WHERE email_id =? AND password =?", (email_id, password))
        return has_logged_in
    except Exception as e:
        print(f"{e}, Try Again:(")


    


