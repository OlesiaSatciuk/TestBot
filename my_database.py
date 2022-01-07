import mysql
import mysql.connector

import datetime


def write_new_user(user_id, first_name, last_name, user_name):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        # auth_plugin="caching_sha2_password"
    )

    my_cursor = mytb.cursor()
    try:
        bot_data = "INSERT INTO testbot_users (user_id, first_name, last_name, user_name) VALUES (%s, %s, %s, %s)"
        val = (user_id, first_name, last_name, user_name)
        my_cursor.execute(bot_data, val)
        mytb.commit()
        print("ok")
    except Exception as e:
        today = datetime.date.today().strftime('%Y%m%d')
        print(today)
        # my_cursor.execute('UPDATE bot_users SET date_visits=%s WHERE user_id=%s' % user_id)
        my_cursor.execute(f'UPDATE testbot_users SET date_visits={today} WHERE user_id={user_id}')
        mytb.commit()


def get_info_answers(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        # auth_plugin="caching_sha2_password"
    )

    my_cursor = mytb.cursor()
    my_cursor.execute("SELECT answer_one FROM testbot_users WHERE user_id = %s" % user_id)
    res = my_cursor.fetchone()
    if res:
        return res[0]
    else:
        return None


def get_info_answers_two(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        # auth_plugin="caching_sha2_password"
    )

    my_cursor = mytb.cursor()
    my_cursor.execute("SELECT answer_one FROM testbot_users WHERE user_id = %s" % user_id)
    res = my_cursor.fetchone()
    if res:
        return res[0]
    else:
        return None


def add_answers(answer, user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        # auth_plugin="caching_sha2_password"
    )
    my_cursor = mytb.cursor()
    my_cursor.execute(f'UPDATE testbot_users SET answer_one={answer} WHERE user_id={user_id}')
    mytb.commit()


def add_answers_two(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        # auth_plugin="caching_sha2_password"
    )
    my_cursor = mytb.cursor()
    my_cursor.execute("SELECT answer_two FROM testbot_users WHERE user_id = %s" % user_id)
    res = my_cursor.fetchone()
    result = res[0]+1
    print(result, 'result')
    my_cursor.execute(f'UPDATE testbot_users SET answer_two={result} WHERE user_id={user_id}')
    mytb.commit()


def del_answers(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        )
    my_cursor = mytb.cursor()
    my_cursor.execute(f'UPDATE testbot_users SET answer_one = 9 WHERE user_id = {user_id}')
    mytb.commit()


def del_answers_two(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
    )
    my_cursor = mytb.cursor()
    my_cursor.execute(f'UPDATE testbot_users SET answer_two = 0 WHERE user_id = {user_id}')
    mytb.commit()



    # my_cursor.execute("SELECT answer_one FROM testbot_users WHERE user_id = %s" % user_id)
    # res = my_cursor.fetchone()
    # if res[0] == None:
    #     print('answer_one', res)
    #     bot_data = "INSERT INTO testbot_users (answer_one) VALUES (%s) WHERE user_id = %s"
    #     val = (answer, user_id)
    #     my_cursor.execute(bot_data, val)
    #     mytb.commit()
    #     print("ok")
    #     return
    # else:
    #     return None


def count_answers(text, user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        )
    column = ''
    if text == 'quiz_one':
        column = 'answer_one'
    elif text == 'quiz_two':
        column = 'answer_two'

    my_cursor = mytb.cursor()
    my_cursor.execute(f"SELECT {column} FROM testbot_users WHERE user_id = {user_id}")
    res = my_cursor.fetchone()
    if res and text == 'quiz_one':
        return list(str(res[0]))
    elif res and text == 'quiz_two':
        return (str(res[0]))
    else:
        return None


def right_answers(user_id):
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
        )
    my_cursor = mytb.cursor()
    my_cursor.execute(f'UPDATE testbot_users SET right_answers = 1 WHERE user_id = {user_id}')
    mytb.commit()


def all_users():
    mytb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        port="3306",
        database="myTestBotDatabase",
        auth_plugin='mysql_native_password'
    )
    my_cursor = mytb.cursor()
    my_cursor.execute("SELECT user_id FROM testbot_users WHERE right_answers = 1")
    res_right = my_cursor.fetchall()
    my_cursor.execute("SELECT user_id FROM testbot_users")
    res_all = my_cursor.fetchall()

    return res_all, res_right
