'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
login_view = view.View().load_template("login")
register_view = view.View().load_template("register")

# -----------------------------------------------------------------------------
# Index
# -----------------------------------------------------------------------------
def lesson_1():
    return page_view("lesson_1")
def lesson_2():
    return page_view("lesson_2")
def lesson_3():
    return page_view("lesson_3")
def lesson_4():
    return page_view("lesson_4")
def lesson_5():
    return page_view("lesson_5")
def lesson_6():
    return page_view("lesson_6")
def lesson_7():
    return page_view("lesson_7")
def lesson_8():
    return page_view("lesson_8")
def index_init():
    return page_view("index")

def myhome_init():
    return page_view("home")

def Header_init():
    return page_view("header")

def same_title_init():
    return page_view("same_title")

def base_init():
    return page_view("base")

def Forum_init():
    return page_view("tiezi")

def Unser_Centre_init():
    return page_view("Unser_centre")

def password_init():
    return page_view("upload_password")

def admin_password_init():
    return page_view("admin_password")

def write_init():
    return page_view("write")

def mywrite_init():
    return page_view("myWrite")

def admin_write_msg_init():
    return page_view("admin_write_msg")

def mymsg_init():
    return page_view("myMsg")

def write_msg_init():
    return page_view("write_msg")

def add_friend_success():
    return page_view("add_friend")

def message_content():
    return page_view("message_content")

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return login_view

def register_form():
    return register_view

# -----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True

    if username != "admin":  # Wrong Username
        err_str = "Incorrect Username"
        login = False

    if password != "password":  # Wrong password
        err_str = "Incorrect Password"
        login = False

    if login:
        return page_view("valid", name=username)
        # return page_view("Forum")
    else:
        return page_view("invalid", reason=err_str)


# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

#-----------------------------------------------------------------------------
# Lessions
#-----------------------------------------------------------------------------

def lessions():
    '''
        lessions
        Returns the lessions in lessions page
    '''
    return page_view("lessons")

#-----------------------------------------------------------------------------
# Admin Page
#-----------------------------------------------------------------------------

def admin():
    return page_view("adminPage")

def chmod():
    return page_view("admin_chmod")

def add():
    return page_view("admin_add_user")
    
# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
              "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
              "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
              "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
              "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
              "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


# -----------------------------------------------------------------------------
# Debug
# -----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


# -----------------------------------------------------------------------------
# 404
# Custom 404 error page
# -----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)

def User_error():
    return page_view("error")


def User_error():
    return page_view("AddFriendError")

def Login_error():
    return page_view("Login_error")