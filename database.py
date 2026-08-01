import sqlite3
conn=sqlite3.connect("chats.db",check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS user(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME VARCHAR,
    EMAIL VARCHAR UNIQUE,
    PASSWORD VARCHAR
   );    
""")
conn.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USER_ID INTEGER,
    MESSAGE TEXT NOT NULL,
    ROLE TEXT NOT NULL,
    CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (USER_ID) REFERENCES user(ID)             
);

""")

def create_user_index(column_name:str):
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{column_name} ON user ({column_name});")
    conn.commit()

def create_messages_index(colunm_name:str):
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx1_{colunm_name} ON messages ({colunm_name});")
    conn.commit()


def show_user_indexs():
    cursor.execute("PRAGMA index_list('user');")
    indexs=cursor.fetchall()
    for index in indexs:
        print(index)

def show_messages_index():
    cursor.execute("PRAGMA index_list('messages');")
    indexs=cursor.fetchall()
    for index in indexs:
        print(index)
    

def get_message():
    cursor.execute("SELECT ROLE,MESSAGE FROM messages;")
    conn.commit()


def get_username(USER_ID:int)->str:
    cursor.execute("SELECT USERNAME FROM user WHERE ID = ?",(USER_ID,))
    conn.commit()
    name=cursor.fetchall()
    return name[0][0]

def get_password(USER_ID:int)->str:
    cursor.execute("SELECT PASSWORD FROM user WHERE ID = ?",(USER_ID,))
    conn.commit()
    password=cursor.fetchall()
    return password[0][0]

def get_user_id(EMAIL:str):
    cursor.execute("SELECT ID FROM user WHERE EMAIL = ?",(EMAIL,))
    conn.commit()
    result=cursor.fetchone()
    if result == None:
        return ""
    else:
        return result[0]

def add_user(USERNAME,EMAIL,PASSWORD):
    try:
        cursor.execute("INSERT INTO user (USERNAME,EMAIL,PASSWORD) VALUES (?,?,?)",(USERNAME,EMAIL,PASSWORD))
        conn.commit()
    except Exception as e:
        return "Exception: User already exists"

def add_message(ROLE :str,MESSAGE :str,USER_ID :int):
    cursor.execute(
    "SELECT ID FROM user WHERE ID = ? ",
    (USER_ID,)
    )
    result = cursor.fetchone()
    if result:
        ID = result[0]
        cursor.execute(
            "INSERT INTO messages (USER_ID,MESSAGE, ROLE) VALUES ( ?, ? ,?)",
            (USER_ID,MESSAGE, ROLE)
        )
        conn.commit()
    else:
        return "User does not exist."

def show_all_data():
    print("USER'S data.")
    show_user_data()
    print("MESSAGES data.")
    show_messages_data()

def Check_user_password(EMAIL,PASSWORD):
    cursor.execute("SELECT ID FROM user WHERE EMAIL = ? AND PASSWORD = ?",(EMAIL,PASSWORD))
    conn.commit()
    result=cursor.fetchone()
    if result==None:
        return False
    else:
        # print(result)
        return True
        

def show_messages_data():
    cursor.execute("SELECT * FROM messages;")
    conn.commit()
    results=cursor.fetchall()   #fetchall() returns a list of tuples
    for result in results:
        print(result)

def show_user_data():
    cursor.execute("SELECT * FROM user;")
    conn.commit()
    results=cursor.fetchall()
    for result in results:
        print(result)

def show_no_row_messages():
    cursor.execute("SELECT COUNT(*) FROM messages;")
    conn.commit()
    print(cursor.fetchone())

def show_chat_history(USER_ID:int):
    cursor.execute("SELECT ROLE,MESSAGE FROM messages WHERE USER_ID = ? ORDER BY ID;",(USER_ID,))
    conn.commit()
    results=cursor.fetchall()
    for result in results:
        print(result)

def show_recent_chat_history(USER_ID:int):
    cursor.execute("SELECT ROLE,MESSAGE FROM messages WHERE USER_ID = ? ORDER BY ID DESC LIMIT 20;",(USER_ID,))
    conn.commit()
    results=cursor.fetchall()
    results.reverse()
    history=[]
    for result in results:
        history.append(result)
    return history

def delete_all_database():
    delete_all_user()
    delete_all_chats()

def delete_chat(USER_ID:int):
    cursor.execute("DELETE FROM messages WHERE USER_ID = ?;",(USER_ID,))
    conn.commit()

def delete_all_chats():
    cursor.execute("DELETE FROM messages;")
    conn.commit()

def delete_user(USER_ID:int):
    cursor.execute("DELETE FROM user WHERE ID = ?;",(USER_ID,))
    conn.commit()

def delete_all_user():
    cursor.execute("DELETE FROM user;")

#test
# user_id=int(input("Enter your id:"))
# username=input("Enter you name:")
# add_user(user_id,username)
# message=input("Enter your message:")
# role=input("Enter your role:")
# id=int(input("Enter your user id:"))
# add_message(role,message,id)


