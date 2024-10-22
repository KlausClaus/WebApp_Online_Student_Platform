'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
    hello
'''

from bottle import template,route, get, post, redirect, error, request, static_file,response,run,default_app
import model
import hashlib

# -----------------------Adding default Admin Account--------------------------
# All_user = dict()
# All_user["Admin"] = "123456"
import sqlite3
import os.path

Msg_ID = 0
ip_white_list = ['127.0.0.1']
ip_black_list = []
# hash salt
salt = "$topsecret$"


if os.path.isfile("username_psw.db") == False:
    conn = sqlite3.connect('username_psw.db')  # Warning: This file is created in the current directory
    c = conn.cursor()
    c.execute(
        "CREATE TABLE username_psw (Username VARCHAR(50) PRIMARY KEY, Password VARCHAR(50) NOT NULL, If_admin BOOLEAN "
        "NOT NULL, If_muted BOOLEAN NOT NULL)")
    psw = 'Dfq123456NB'
    salt_psw = hashlib.md5((psw+salt).encode()).hexdigest()
    c.execute("INSERT INTO username_psw (Username, Password, If_admin, If_muted) VALUES ('Admin','{}','TRUE','FALSE') ".format(salt_psw))
    conn.commit()
    conn.close()

if os.path.isfile("post_content.db") == False:
    conn = sqlite3.connect('post_content.db')  # Warning: This file is created in the current directory
    c = conn.cursor()
    c.execute("CREATE TABLE post_content (title VARCHAR(50) PRIMARY KEY, username VARCHAR(50) NOT NULL, category "
              "VARCHAR(50) NOT NULL, content VARCHAR(1000) NOT NULL)")
    c.execute("INSERT INTO post_content (title, username, category, content) VALUES ('first test','Admin','General',"
              "'Hello world') ")
    conn.commit()
    conn.close()


    conn = sqlite3.connect('post_content.db')  # Warning: This file is created in the current directory
    c = conn.cursor()
    c.execute("CREATE TABLE post_comment (tiezi_id INTEGER NOT NULL, username VARCHAR(50) NOT NULL, content VARCHAR(1000) NOT NULL)")
    c.execute("INSERT INTO post_comment (tiezi_id, username, content) VALUES ('1','Admin','hi world') ")
    conn.commit()
    conn.close()


if os.path.isfile("Message.db") == False:
    conn = sqlite3.connect('Message.db')  # Warning: This file is created in the current directory
    c = conn.cursor()
    c.execute("CREATE TABLE Message (Msg_ID INTEGER PRIMARY KEY, Sender VARCHAR(50) NOT NULL, Target VARCHAR(50) NOT NULL, Content VARCHAR(1000) NOT NULL)")
    c.execute("INSERT INTO Message (Msg_ID, Sender, Target, Content) VALUES (0, 'tester','Klaus','Hello world') ")
    conn.commit()
    conn.close()

def escape(s):
    res = ""
    for i in s:
        if i == "&":
            res += "&amp;"
        elif i == "<":
            res += "&lt;"
        elif i == ">":
            res += "&gt;"
        elif i == '\"':
            res += "&quot;"
        elif i == "\'":
            res += "&#x27;"
        elif i == "/":
            res += "&#x2F;"
        else:
            res += i
    return res

# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')


# -----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')


# -----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------

# Redirect to login

@get('/myhome')
def get_myhome():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')
    if Logged_Username == "Admin":
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            return redirect('/login')
    try:
        conn = sqlite3.connect('username_psw.db')
        c = conn.cursor()
        sql = "SELECT Username, If_admin FROM username_psw WHERE Username = '{}'".format(Logged_Username)
        c.execute(sql)
        res = c.fetchall()  # [('Admin', '123456')]
        if res[0][1] == 'TRUE':
            c.close()
            return model.admin()
        else:
            c.close()
            username = Logged_Username

            head_file = open("./myhome_head.txt","r")
            tail_file = open("./myhome_tail.txt","r")
            head = head_file.read()
            tail = tail_file.read()
            head_file.close()
            tail_file.close()

            res = ""

            res += """
                    <div class="homeCen_right">
                                    <div class="home_self"></div>
                                    <div class="home_name"><p>{0}</p></div>
                                    <div class="home_msg">
                                        <ul>
                                            <li>University of Sydney Student</li>
                                            <li>Earth</li>
                                        </ul>
                                    </div>
                                </div>
            
                    """.format(username)

            target_file = open("./templates/home.html",'w')
            res = head + res + tail
            target_file.write(res)
            target_file.close()

            return model.myhome_init()

    except Exception:
        c.close()
        return model.User_error()

@get('/index')
def get_index():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    username = Logged_Username

    head_file = open("./post_list_head.txt", "r")
    tail_file = open("./post_list_tail.txt", "r")
    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "SELECT oid, title, category, username FROM post_content"
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    res = ""

    for i in sets:
        res += """
                <div class="indexCon_msg">
                        <div class="indexCon_msg_pic"></div>
                        <div class="indexCon_msg_detail">
                            <a href="">
                                <div class="indexCon_msg_detail_tittle">
                                    <span>{0}</span>
                                    <li>{1}</li>
                                </div>
                            </a>
                            <div class="indexCon_msg_detail_other">
                                <ul style = "padding:0; margin:0">
                                    <div class="writeFoot1"><input style = "border:0;outline:none;background-color:rgba(0,0,0,0);font-size:16px;" type = "submit" autocomplete="off" name = "{2}a" value = "{3}"></input></div>
                                </ul>
                            </div>
                        </div>
                        <div class="clear"></div>
                    </div>
            """.format(i[2], i[3], i[0], i[1])

    target_file = open("./templates/index.html", 'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()

    return model.index_init()


@post('/index')
def do_index():
    data = request.body.readlines()[0].decode()
    target = data.split("=")
    tiezi_id = int(target[0][:-1])
    if target[0][-1] == "a":
        return redirect('/Forum?id={}'.format(tiezi_id))

    return redirect("/index")


# Display the lessions page
@get('/base')
def get_base():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.base_init()


@get('/password')
def get_password():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')
    if Logged_Username == "Admin":
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            return redirect('/login')

    username = Logged_Username
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE Username = '{}'".format(username)  # get all users
    c.execute(sql)
    res = c.fetchall()
    conn.close()
    if res[0][0] == "TRUE":
        return model.admin_password_init()
    else:
        return model.password_init()


def check_change_password(username, password, new_password, new_password_repeat):
    user_password = ''
    # checking if the username is repeated in the database
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT * FROM username_psw"  # get all users
    c.execute(sql)
    res = c.fetchall()
    i = 0
    while i < len(res):
        if username == res[i][0]:
            user_password = res[i][1]
        i += 1

    if user_password == password and new_password == new_password_repeat:

        salt_new_psw = hashlib.md5((new_password+salt).encode()).hexdigest()
        sql_load = "UPDATE username_psw SET Password = '{}' WHERE Username = '{}'".format(salt_new_psw, username)
        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False


@post('/password')
def do_password():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    current_password = request.forms.get('current_psw')
    new_password = request.forms.get('new_psw')

    password = new_password
    if password.isalnum() == False or len(password)<5 or len(password)>20:
        print(password.isalnum())
        return redirect('/password?upload=False')

    repeat_new_password = request.forms.get('repeat_new_psw')
    salt_psw = hashlib.md5((current_password+salt).encode()).hexdigest()

    check = check_change_password(username, salt_psw, new_password, repeat_new_password)

    if check:
        return redirect('/myhome')
    else:
        return redirect('/password?upload=False')

@get('/write')
def get_write():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    username = Logged_Username

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_muted FROM username_psw WHERE username = '{}'".format(username)
    c.execute(sql)
    res = c.fetchall()
    mute = res[0][0]
    if mute == "TRUE":
        return redirect('/index?mute=True')

    return model.write_init()


def pre_write(username, title, category, content):
    user_title = ''
    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "SELECT title FROM post_content WHERE title = '{}'".format(title)
    c.execute(sql)
    res = c.fetchall()

    if (len(res) == 0):
        # if user_title != title:
        sql_load = "INSERT INTO post_content (username, title, category, content) VALUES ('{}','{}', '{}', '{}')".format(
            username, title, category, content)
        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

@post('/write')
def do_write():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    title = request.forms.get('title')
    title = escape(title)
    category = request.forms.get('cate')
    if category == "please choose":
        redirect('/write?cate=False')
    content = request.forms.get('content')
    if content == "":
        redirect('/write?content=False')
    
    content = escape(content)

    if pre_write(username, title, category, content):
        return redirect('/myhome')
    else:
        return model.same_title_init()

# -----------------------------------------------------------------------------
@get('/mywrite')
def get_mywrite():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')
    if Logged_Username == "Admin":
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            return redirect('/login')

    username = Logged_Username
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE username = '{}'".format(username)
    c.execute(sql)
    modify = c.fetchall()
    c.close()
    conn.close()

    if modify[0][0] == "TRUE":
        head_file = open("./admin_post_head.txt", "r")
        tail_file = open("./admin_post_tail.txt", "r")
    else:
        head_file = open("./mypost_head.txt", "r")
        tail_file = open("./mypost_tail.txt", "r")
    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "SELECT oid, title, category FROM post_content WHERE username = '{}'".format(username)
    c.execute(sql)
    sets = c.fetchall()
    c.close()
    conn.close()

    res = ""

    for i in sets:
        if len(i[1]) > 15:
            cut = i[1][:4]
            res += """
                            <div class="writeFoot">
                                <div class="writeFoot1"><input style="border:0;outline:none;background-color:rgba(0,0,0,0);font-size:18px;" type = "submit" name = "{0}a" value = "{1}..."></input></div>
                                
                                <div class="writeFoot3">{2}</div>
                                <div style = "margin: 2px" class="Delete"><input style="display: inline-block;background-color: #e43e20;width: 70px;color: white;float: right;padding: 5px;font-size: 16px;border: none;cursor: pointer;border-radius: 5px;" type = "submit" name = "{0}b" value = "delete" onclick="return confirm('Are you sure you want to DELETE this post?');" type = "submit" name = "{0}b" value = "delete" onclick="return confirm('Are you sure you want to DELETE this post?');"></input></div>
                            </div>
            """.format(i[0], cut, i[2])
        else:
            cut = i[1]
            res += """
                            <div class="writeFoot">
                                <div class="writeFoot1"><input style="border:0;outline:none;background-color:rgba(0,0,0,0);font-size:18px;" type = "submit" name = "{0}a" value = "{1}"></input></div>
                                
                                <div class="writeFoot3">{2}</div>
                                <div style = "margin: 2px" class="Delete"><input style="display: inline-block;background-color: #e43e20;width: 70px;color: white;float: right;padding: 5px;font-size: 16px;border: none;cursor: pointer;border-radius: 5px;" type = "submit" name = "{0}b" value = "delete" onclick="return confirm('Are you sure you want to DELETE this post?');" type = "submit" name = "{0}b" value = "delete" onclick="return confirm('Are you sure you want to DELETE this post?');"></input></div>
                            </div>
            """.format(i[0], cut, i[2])

    target_file = open("./templates/myWrite.html", 'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()

    return model.mywrite_init()


@post('/mywrite')
def do_write():
    # Get Post data
    data = request.body.readlines()[0].decode()

    # Get target 
    target = data.split("=")
    tiezi_id = int(target[0][:-1])
    if target[0][-1] == "a":
        return redirect('/Forum?id={}'.format(tiezi_id))
    else:

        conn = sqlite3.connect('post_content.db')
        c = conn.cursor()

        sql_load = "DELETE FROM post_content WHERE oid = '{}'".format(tiezi_id)
        c.execute(sql_load)
        conn.commit()
        conn.close()

    return redirect("/mywrite")



@get('/admin_write_msg')
def get_writeMsg():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')
    return model.admin_write_msg_init()

def admin_pre_writeMsg(Target,content):
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    connect = sqlite3.connect('username_psw.db')
    cc = connect.cursor()
    exist_user = "SELECT Username FROM username_psw WHERE Username = '{}'".format(Target)

    cc.execute(exist_user)
    res = cc.fetchall()
    connect.commit()
    connect.close()


    if (len(res) != 0):
        # if there exist the target user:
        conn = sqlite3.connect('Message.db')
        c = conn.cursor()

        mid = "SELECT Msg_ID FROM Message"
        c.execute(mid)
        temp = c.fetchall()
        sql_load = "INSERT INTO Message (Msg_ID, Target, Sender, Content) VALUES ('{}','{}', '{}', '{}')".format(len(temp), Target, username, content)
        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        return False


@post('/admin_write_msg')
def admin_do_writeMsg():
    Target = request.forms.get('Target')
    content = request.forms.get('content')
    content = escape(content)

    if admin_pre_writeMsg(Target,content):
        return model.mymsg_init()
    else:
        return model.User_error()


@get('/mymsg')
def pre_msg():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')
    if Logged_Username == "Admin":
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            return redirect('/login')

    username = Logged_Username
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE username = '{}'".format(username)
    c.execute(sql)
    modify = c.fetchall()
    c.close()
    conn.close()

    if modify[0][0] == "TRUE":
        head_file = open("./admin_msg_head.txt", "r")
        tail_file = open("./admin_msg_tail.txt", "r")
    else:
        head_file = open("./mymsg_head.txt","r")
        tail_file = open("./mymsg_tail.txt","r")

    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    cat = sqlite3.connect('Message.db')
    con = cat.cursor()
    sql = "SELECT Msg_ID, Sender, Target, Content FROM Message WHERE Target = '{}'".format(username)
    con.execute(sql)
    sets = con.fetchall()
    con.close()

    res = ""
    Existed_users = []
    Exist = False

    for i in sets:
        ##checking if the username already exist
        for u in Existed_users:
            if i[1] == u: 
                Exist = True 
        
        if not Exist: 
            Existed_users.append(i[1])
            res += """                    
                    <div class="myMsgCon">
                        <div class="myMsgCon_pic"></div>
                        <div class="myMsgCon_detail">
                            <input style="border:0;outline:none;background-color:rgba(0,0,0,0);font-size:18px;" type = "submit" name = "{0}a" value = "{1}'s chat with you"></input>
                        </div>
                    </div>
                    
                """.format(i[1],i[1])
        Exist = False

    target_file = open("./templates/myMsg.html",'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()

    return model.mymsg_init()

@post('/mymsg')
def do_mymsg():
    data = request.body.readlines()[0].decode()
    target = data.split("=")
    sender = target[0][:-1]
    print(target)
    if target[0][-1] == "a":
        return redirect('/message_content?sender={}'.format(sender))

    return redirect("/mymsg")


def pre_writeMsg(Target,content):
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    connect = sqlite3.connect('username_psw.db')
    cc = connect.cursor()

    exist_user = "SELECT Username FROM username_psw WHERE Username = '{}'".format(Target)

    cc.execute(exist_user)
    res = cc.fetchall()
    connect.commit()
    connect.close()


    if (len(res) != 0):
        # if there exist the target user:
        conn = sqlite3.connect('Message.db')
        c = conn.cursor()

        mid = "SELECT Msg_ID FROM Message"
        c.execute(mid)
        temp = c.fetchall()
        sql_load = "INSERT INTO Message (Msg_ID, Target, Sender, Content) VALUES ('{}','{}', '{}', '{}')".format(len(temp), Target, username, content)
        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        return False


@get('/message_content')
def get_message_content():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sender = request.query.get("sender")
    sql = "SELECT If_admin FROM username_psw WHERE username = '{}'".format(username)
    c.execute(sql)
    modify = c.fetchall()
    c.close()
    conn.close()

    if modify[0][0] == "TRUE":
        head_file = open("./admin_msg_content_head.txt", "r")
        tail_file = open("./admin_msg_content_tail.txt", "r")
    else:
        head_file = open("./message_head.txt","r")
        tail_file = open("./message_tail.txt","r")

    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    conn = sqlite3.connect('Message.db')

    cat = conn.cursor()
    sql = "SELECT oid, Sender, Target, Content FROM Message WHERE (Target = '{}' and Sender = '{}') OR (Sender = '{}' and Target = '{}')".format(username, sender, username, sender)
    cat.execute(sql)
    all_msg = cat.fetchall()

    res = ""
    for i in all_msg:
        if i[2] == Logged_Username: #received
            res +=  """
                        <div class="atalk">
                             <span>
                                 {0}
                             </span>
                         </div>
                    """.format(i[3])
        else:
            res +=  """
                        <div class="btalk">
                             <span>
                                 {0}
                             </span>
                         </div>
                    """.format(i[3])

    target_file = open("./templates/message_content.html",'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()


    return model.message_content()

@post('/message_content')
def post_message_content():

    Target = request.forms.get('Target')
    print(Target)
    content = request.forms.get('content')
    print("Content has been get \n")
    print(content + "\n")

    content = escape(content)

    if pre_writeMsg(Target,content):
        print("message has been sent \n")

        return model.mymsg_init()
    else:
        return model.User_error()



@get('/writeMsg')
def get_writeMsg():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.write_msg_init()



# add_friend function
def pre_AddFriend(Target,content):
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    username = Logged_Username

    connect = sqlite3.connect('username_psw.db')
    cc = connect.cursor()
    exist_user = "SELECT Username FROM username_psw WHERE Username = '{}'".format(Target)

    cc.execute(exist_user)
    res = cc.fetchall()
    connect.commit()
    connect.close()


    if (len(res) != 0):
        # if there exist the target user:
        conn = sqlite3.connect('Message.db')
        c = conn.cursor()

        mid = "SELECT Msg_ID FROM Message"
        c.execute(mid)
        temp = c.fetchall()

        sql_load = "INSERT INTO Message (Msg_ID, Target, Sender, Content) VALUES ('{}','{}', '{}', '{}')".format(len(temp), Target, username, content)

        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        return False


# add friend
@post('/writeMsg')
def do_AddFriend():
    Target = request.forms.get('Target')
    content = Target+", You have a new Friend"
    content = escape(content)

    if pre_AddFriend(Target,content):
        Logged_Username = request.get_cookie("username",secret = "gayFamily")
        username = Logged_Username

        connect = sqlite3.connect('username_psw.db')
        cc = connect.cursor()
        exist_user = "SELECT Username FROM username_psw WHERE Username = '{}'".format(Target)

        cc.execute(exist_user)
        res = cc.fetchall()
        connect.commit()
        connect.close()


        if (len(res) != 0):
            # if there exist the target user:
            conn = sqlite3.connect('Message.db')
            c = conn.cursor()

            mid = "SELECT Msg_ID FROM Message"
            c.execute(mid)
            temp = c.fetchall()

            reply = "Hello, I'm Your New Friend!"
            reply = escape(reply)

            sql_load = "INSERT INTO Message (Msg_ID, Target, Sender, Content) VALUES ('{}','{}', '{}', '{}')".format(len(temp), username, Target, reply)

            c.execute(sql_load)
            conn.commit()
            conn.close()

        return model.add_friend_success()
    else:
        return model.User_error()


@get('/lessons')
def get_lessons():
    '''
        get_lesssions

        get the lessions for students to learn
    '''
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lessions()

# -----------------------------------------------------------------------------
# Display the fourm page
@get('/Forum')
def get_fourum():
    '''
        get_index

        Serves the index page
    '''
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    tiezi_id = request.query.get("id")
    # Below is tiezi create program
    username = Logged_Username

    head_file = open("./content_head.txt","r")
    tail_file = open("./content_tail.txt","r")
    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "SELECT oid, title, content, username FROM post_content WHERE oid = '{}'".format(tiezi_id)
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    res = """
        <div class="tzCon">
            <div class="tzCon_head">
                <div class="tzCon_head_left"></div>
                    <div class="tzCon_head_right">
                        <h1>{0}</h1>
                        <ul>
                            <li>{1}</li>
                        </ul>
                    </div>
                </div>
                <div class="clear">
                </div>
                <div class="tzCon_con">
                    {2}
                </div>
            </div>
            <div class="newPending">
                <div class="newPending_head">
                    <div class="tzHeng"></div>
                    <div class="newPending_head_tittle">comments</div>
                </div>
    """.format(sets[0][1],sets[0][3],sets[0][2])

    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "SELECT username, content FROM post_comment WHERE tiezi_id = '{}'".format(tiezi_id)
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    for i in sets:
        res += """
        <div class="newPending_son">
            <div class="pendPic"></div>
            <div class="pendDetail">
                <div class="pendDetail_con">
                    <p>{0}</p>
                    <p>{1}</p>
                </div>
            </div>
            <div class="clear"></div>
        </div>
            """.format(i[0],i[1])


    res += """
        </div>
        <form action="/Forum?id={1}" method="post">
            <div class="writePending">
                <div class="writePending_con">
                    <input type="text" name = "content" autocomplete="off" placeholder="Write Your Comments..."/>
                    <input type="submit" name="{0}" value="Comment"/>
                </div>
            </div>
        </form>
    """.format(username,tiezi_id)


    target_file = open("./templates/tiezi.html",'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()

    return model.Forum_init()

@post('/Forum')
def do_forum():

    data = request.body.readlines()[0].decode().split("&")
    content = request.forms.get('content')

    tiezi_id = request.query["id"]

    username = data[1].split("=")[0]
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_muted FROM username_psw WHERE username = '{}'".format(username)
    c.execute(sql)
    res = c.fetchall()
    mute = res[0][0]
    if mute == "TRUE":
        return redirect('/index?mute=True')
    conn.close()

    if content == "" or  content.strip() == "":
        redirect('/Forum?id={}&comment=False'.format(tiezi_id))
    content = escape(content)

    conn = sqlite3.connect('post_content.db')
    c = conn.cursor()
    sql = "INSERT INTO post_comment (tiezi_id, username, content) VALUES ('{}','{}','{}')".format(tiezi_id, username, content)
    c.execute(sql)
    conn.commit()
    conn.close()

    redirect('/Forum?id={}'.format(tiezi_id))

# -----------------------------------------------------------------------------

# Display the login page
@get('/')
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    response.set_cookie("username",None,secret = "gayFamily",httponly = True)
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        client_ip = request.environ.get('REMOTE_ADDR')
    else:
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    # print(request.environ)

    print("----------Login page Visit ip: {}---------\n".format(client_ip))

    global ip_white_list
    global ip_black_list
    return model.login_form()


def check_login(username, password):
    try:
        conn = sqlite3.connect('username_psw.db')
        c = conn.cursor()
        sql = "SELECT Username, Password, If_admin FROM username_psw WHERE Username = '{}' AND Password = '{}'".format(username,
                                                                                                             password)
        c.execute(sql)
        res = c.fetchall()  # [('Admin', '123456')]
        ## preparing admin psw with salt 
        psw = res[0][1]
        salt_psw_admin = hashlib.md5((psw+salt).encode()).hexdigest()
        if res[0][0] == username and res[0][1] == password and res[0][2] == "TRUE" and password == salt_psw_admin:
            conn.close()
            return 1
        if res[0][0] == username and res[0][1] == password:
            conn.close()
            return 2
        else:
            conn.close()
            return 0
    except Exception:
        print("error")
        return 0


# -----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('user_name')
    password = request.forms.get('psw')
    salt_psw = hashlib.md5((password+salt).encode()).hexdigest()
    check = check_login(username, salt_psw)

    print("----------Try to login: username: {}, password: {}---------\n".format(username,password))


    if check == 2:
        print("----------Login success: username: {}, password: {}---------\n".format(username,password))

        response.set_cookie("username",username,secret = "gayFamily",httponly = True,max_age = 600)
        return redirect('/myhome')
    elif check == 1:


        print("----------Login success: username: {}, password: {}---------\n".format(username,password))


        response.set_cookie("username",username,secret = "gayFamily",httponly = True,max_age = 600)
        return redirect('/adminPage')
    else:


        print("----------Login failed: username: {}, password: {}---------\n".format(username,password))


        return redirect('/login?success=False')


# -----------------------------------------------------------------------------

# Display the registration page 
@get('/register')
def get_register_controller():

    client_ip = request.environ.get('REMOTE_ADDR')

    print("----------Register Visit ip: {}---------\n".format(client_ip))

    return model.register_form()


def check_registration(username, password, password_repeat):
    # checking if the username is repeated in the database
    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT * FROM username_psw"  # get all users
    c.execute(sql)
    res = c.fetchall()
    i = 0
    while i < len(res):
        if username == res[i][0]:
            conn.close()
            return False
        i += 1

    if password == password_repeat and password == username:
        conn.close()
        return False

    if password == password_repeat:
        salt_psw = hashlib.md5((password+salt).encode()).hexdigest()
        sql_load = "INSERT INTO username_psw (Username, Password, If_admin, If_muted) VALUES ('{}','{}', 'FALSE', 'FALSE')".format(
            username, salt_psw)
        c.execute(sql_load)
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

    # -----------------------------------------------------------------------------


@post('/register')
def do_register():
    username = request.forms.get('user_name')
    if username.isalnum() == False or len(username)<3 or len(username) > 8:

        print("----------Register failed, blocked by check USERNAME: {}---------\n".format(username))

        return redirect('/register?success=False')

    password = request.forms.get('psw')
    if password.isalnum() == False or len(password)<5 or len(password)>20:

        print("----------Register failed, blocked by check PASSWORD: {}---------\n".format(password))

        return redirect('/register?success=False')
    password_repeat = request.forms.get('psw_repeat')

    print("----------Try to register: username: {}, password: {}, repeat: {}---------\n".format(username,password,password_repeat))

    if check_registration(username, password, password_repeat):

        print("----------Register success: username: {}, password: {}---------\n".format(username,password))

        return redirect('/login?Success')
    else:

        print("----------Register failed: username: {}, password: {} repeat: {}---------\n".format(username,password,password_repeat))

        return redirect('/register?success=False')


# -----------------------------------------------------------------------------
@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    print("--visit useless about page\n--")
    return model.about()


# -----------------------------------------------------------------------------
@get('/adminPage')
def get_admin():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")

    if Logged_Username == None:
        print("----------Kicked out by admin check: not log in---------\n")
        return redirect('/login')

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE Username = '{}'".format(Logged_Username)
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    if sets[0][0] != "TRUE":
        print("----------Kicked out by admin check: username: {}, If_admin: {}---------\n".format(Logged_Username,sets[0][0]))
        return redirect('/login')

    print("----------View admin home page: username: {}---------\n".format(Logged_Username))

    return model.admin()


@get('/chmod')
def get_chmod():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        print("----------Kicked out by admin check: not log in---------\n")
        return redirect('/login')

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE Username = '{}'".format(Logged_Username)
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    if sets[0][0] != "TRUE":
        print("----------Kicked out by admin check: username: {}, If_admin: {}---------\n".format(Logged_Username,sets[0][0]))
        return redirect('/login')
    else:
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            print("----------Kicked out by admin check: ip not in white list: {}---------\n".format(client_ip))
            return redirect('/login')

    print("----------View admin chmod: username: {}---------\n".format(Logged_Username))

    # To create html file dynamically
    head_file = open("./chmod_head.txt", "r")
    tail_file = open("./chmod_tail.txt", "r")
    head = head_file.read()
    tail = tail_file.read()
    head_file.close()
    tail_file.close()

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT Username, If_admin, If_muted FROM username_psw"
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    res = ""
    for i in sets:
        if i[1] == "TRUE":
            res += """
                            <div class="myCon">
                                <div class="myCon_pic"></div>
                                <div class="myCon_detail">
                                    {0} (Administrator)
                                </div>
                                <input type="submit" name = "{0}1" value = "Delete" class="dropbtn" onclick="return confirm('Are you sure you want DELETE this user?\\nAll the posts and messages will not back.');"></input>
            """.format(i[0])
        else:
            res += """
                            <div class="myCon">
                                <div class="myCon_pic"></div>
                                <div class="myCon_detail">
                                    {0}
                                </div>
                                <input type="submit" name = "{0}1" value = "Delete" class="dropbtn" onclick="return confirm('Are you sure you want DELETE this user?\\nAll the posts and messages will not back.');"></input>
            """.format(i[0])
        if i[2] == "TRUE":
            res += """
                                <input type="submit" name = "{0}2" value = "Unmute" class="dropbtn"></input>
                            </div>
            """.format(i[0])
        else:
            res += """
                                <input type="submit" name = "{0}2" value = "Mute" class="dropbtn"></input>
                            </div>
            """.format(i[0])

    target_file = open("./templates/admin_chmod.html", 'w')
    res = head + res + tail
    target_file.write(res)
    target_file.close()

    return model.chmod()


@post('/chmod')
def do_chmod():
    # Get Post data
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    data = request.body.readlines()[0].decode()
    username = Logged_Username

    # Get target 
    target = data.split("=")
    if target[0] == "Add":  # when add button was pressed
        return redirect("/add")
    else:  # otherwise user-things button was pressed
        user = target[0][:-1]
        command = target[1]

        conn = sqlite3.connect('username_psw.db')
        c = conn.cursor()

        if command == "Mute":

            print("----------{} mute {}---------\n".format(Logged_Username,user))
            
            sql_load = "UPDATE username_psw SET If_muted = '{}' WHERE Username = '{}'".format("TRUE", user)
            c.execute(sql_load)
            conn.commit()
            conn.close()
        elif command == "Unmute":

            print("----------{} unmute {}---------\n".format(Logged_Username,user))

            sql_load = "UPDATE username_psw SET If_muted = '{}' WHERE Username = '{}'".format("FALSE", user)
            c.execute(sql_load)
            conn.commit()
            conn.close()
        elif command == "Delete":
            sql_load = "SELECT Username FROM username_psw WHERE username = '{}'".format(username)
            c.execute(sql_load)
            modify = c.fetchall()
            if username == user or user == "Admin":
                print("----------{} unable to delete {}---------\n".format(Logged_Username,user))
                return redirect("/chmod?delete=False")

            print("----------{} delete {}---------\n".format(Logged_Username,user))

            sql_load = "DELETE FROM username_psw WHERE Username = '{}'".format(user)
            c.execute(sql_load)
            conn.commit()
            conn.close()

    return redirect("/chmod")


@get('/add')
def get_add():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        print("----------Kicked out by admin check: not log in---------\n")
        return redirect('/login')

    conn = sqlite3.connect('username_psw.db')
    c = conn.cursor()
    sql = "SELECT If_admin FROM username_psw WHERE Username = '{}'".format(Logged_Username)
    c.execute(sql)
    sets = c.fetchall()
    c.close()

    if sets[0][0] != "TRUE":
        print("----------Kicked out by admin check: username: {}, If_admin: {}---------\n".format(Logged_Username,sets[0][0]))
        return redirect('/login')
    else:
        client_ip = request.environ.get('REMOTE_ADDR')
        if client_ip not in ip_white_list:
            print("----------Kicked out by admin check: ip not in white list: {}---------\n".format(client_ip))
            return redirect('/login')

    return model.add()


@post('/add')
def do_add():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")

    username = request.forms.get('Username')
    password = request.forms.get('password')
    repeat_password = request.forms.get('repeat_psw')
    if username == None or password == None or repeat_password == None or username == '' or password == '' or repeat_password == '':
        print("----------{} add Failed: empty entry---------\n".format(Logged_Username))
        return redirect('/add?add=False')

    if username.isalnum() == False or len(username)<3 or len(username) > 8:
        print("----------{} add Failed: invalid username: {}---------\n".format(Logged_Username,username))
        return redirect('/add?add=False')

    if password.isalnum() == False or len(password)<5 or len(password)>20:
        print("----------{} add Failed: invalid password: {}---------\n".format(Logged_Username,password))
        return redirect('/add?add=False')

    authority = request.forms.get('Authority')

    if check_registration(username, password, repeat_password) == True:
        if authority == "Administrator":
            conn = sqlite3.connect('username_psw.db')
            c = conn.cursor()
            sql_load = "UPDATE username_psw SET If_admin = '{}' WHERE Username = '{}'".format("TRUE", username)
            c.execute(sql_load)
            conn.commit()
            conn.close()
        print("----------{} add Success: username: {}, role: {}---------\n".format(Logged_Username,username,authority))
        return redirect('/add?add=True')

    print("----------{} add Failed: username: {}, password: {}---------\n".format(Logged_Username,username,password))
    return redirect('/add?add=False')

# -----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
# @error(404)
# def error(error):
#     return model.handle_errors(error)


@get('/lesson_1')
def lesson_1():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_1()


@get('/lesson_2')
def lesson_2():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_2()


@get('/lesson_3')
def lesson_3():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_3()


@get('/lesson_4')
def lesson_4():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_4()


@get('/lesson_5')
def lesson_5():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_5()


@get('/lesson_6')
def lesson_6():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_6()


@get('/lesson_7')
def lesson_7():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_7()


@get('/lesson_8')
def lesson_8():
    Logged_Username = request.get_cookie("username",secret = "gayFamily")
    if Logged_Username == None:
        return redirect('/login')

    return model.lesson_8()

if __name__ == '__main__':
    run(host="0.0.0.0", port=8129,debug=False,reloader=True)
else:
    application = default_app()