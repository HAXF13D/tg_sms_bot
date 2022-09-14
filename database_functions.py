import sqlite3

from config import database_name

# Фунуция создания базы данных, если она ещё не создана
def make_database():
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                    user_id INT PRIMARY KEY,
                    chat_id INT,
                    screen TEXT)''')
    con.commit()
    con.close()

def add_user(user_id, chat_id):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
    status = cur.fetchone()
    if status is None:
        cur.execute(f"INSERT INTO users(user_id, chat_id, screen) VALUES("
                    f"'{user_id}', "
                    f"'{chat_id}', "
                    f"'start_screen')"
                    )
    con.commit()
    con.close()

def get_chat_id(user_id):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(f'''SELECT chat_id FROM users WHERE user_id = {user_id}''')
    result = cur.fetchone()[0]
    con.commit()
    con.close()
    return result

def get_screen(user_id):
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(f'''SELECT screen FROM users WHERE user_id = {user_id}''')
    screen = cur.fetchone()[0]
    con.commit()
    con.close()
    return screen

def change_screen(user_id, target_screen):
    con = sqlite3.connect(database_name)
    cur = con.cursor()

    query = "UPDATE users SET screen = '{0}' WHERE user_id = '{1}'".format(target_screen, user_id)
    cur.execute(query)

    con.commit()
    con.close()

