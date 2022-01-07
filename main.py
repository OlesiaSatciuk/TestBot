import mysql.connector
import telebot
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

import my_database
import my_keyboards
import copy

bot: TeleBot = telebot.TeleBot("5091957616:AAFFi9pltzHexgPU4NviTBSIu_GNbj1sKp8")

CHANNEL_DICTIONARY_BY_ID = {-1001680753757: 'MyFirstTestBotChannel'}
CHANNEL_ID = CHANNEL_DICTIONARY_BY_ID.keys()
# CHANNEL_ID = [-1001504627195,]
CHANNEL_TITLE = CHANNEL_DICTIONARY_BY_ID.values()
ADMINS = [360421180, 414838934, ]
CHANNEL_LIST = ''
QUESTION_QUIZ_TWO = ['What?', 'When?', 'Where?']
ANSWERS_QUIZ_TWO = [['It', 'That'], ['Here', 'There'], ['Now', 'Later', 'Before']]
RIGHT_ANSWERS_TWO = [0, 1, 2]
RIGHT_ANSWER_TWO = 0
USER_ANSWERS_TWO = {}
NUMBER_CORRECT_ANSWERS_TWO = 0
QUESTION_QUIZ = ['Число Пі (значення)', 'Які три числа дають однаковий результат при множенні і при додаванні?', 'Яка країна раніше називалась Сіамом?']
ANSWERS_QUIZ = [['3,14159265458979', '3,14159265358979', '3,14159365358979'], ['1, 2 і 3', '1, 1 і 1', '4, 8 і 10'], ['Тібет', 'Непал', 'Тайланд']]
RIGHT_ANSWERS = [1, 0, 2]
RIGHT_ANSWER = 0
USER_ANSWERS = {}
NUMBER_CORRECT_ANSWERS = 0
WELCOME_TEXT = 'Вітаю, тепер ти можеш пройти вікторину'
FINAL_TEXT = 'Вікторину завершено'
START_TEXT = ''
TEXT_URL = {'START': '', 'WELCOME': '', 'FINAL': ''}
URL_BUTTON = {'START': '', 'WELCOME': '', 'FINAL': ''}


print(ANSWERS_QUIZ_TWO[0])


def is_subscribed(chat_ids, user_id):
    print(chat_ids)
    if len(chat_ids) > 0:
        for i in chat_ids:
            try:
                print(i)
                print(bot.get_chat_member(i, user_id).status)
                if bot.get_chat_member(i, user_id).status == 'left' or bot.get_chat_member(i, user_id).status == 'kicked':
                    return False
            except ApiTelegramException as e:
                if e.result_json['description'] == 'Bad Request: user not found':
                    return False
    return True


mytb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port="3306",
    database="myTestBotDatabase",
    auth_plugin='mysql_native_password'
)
my_cursor = mytb.cursor()


my_id = bot.get_me().id
print(my_id)


@bot.channel_post_handler(content_types=['text'], func=lambda m: "add" in m.text)
def channel_func(message):
    print(message.chat.id, message.chat.title)
    global CHANNEL_DICTIONARY_BY_ID
    global CHANNEL_LIST
    CHANNEL_DICTIONARY_BY_ID[message.chat.id] = message.chat.title
    bot.send_message(message.chat.id, message.chat.title)
    print(CHANNEL_DICTIONARY_BY_ID, CHANNEL_ID, list(CHANNEL_TITLE))
    print(type(CHANNEL_DICTIONARY_BY_ID), type(CHANNEL_ID), type(CHANNEL_TITLE))
    CHANNEL_LIST = ", @".join(list(CHANNEL_TITLE))


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message)
    global CHANNEL_LIST
    global USER_ANSWERS
    global TEXT_URL
    global URL_BUTTON
    my_database.write_new_user(message.from_user.id,
                               message.from_user.first_name,
                               message.from_user.last_name,
                               message.from_user.username)

    if message.from_user.id in ADMINS:
        bot.send_message(message.from_user.id, '\u263A Привіт Admin\, *{0}*\.'.
                         format(message.from_user.first_name),
                         reply_markup=my_keyboards.keyboard_start(message, ADMINS), parse_mode='MarkdownV2')
    elif is_subscribed(chat_ids=list(CHANNEL_ID), user_id=message.from_user.id):
        if TEXT_URL['WELCOME'] == '' or URL_BUTTON['WELCOME'] == '':
            bot.send_message(message.from_user.id, '\u263A Привіт, {0}. {1}'.
                             format(message.from_user.first_name, WELCOME_TEXT),
                             reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        elif TEXT_URL['WELCOME'] and URL_BUTTON['WELCOME']:
            bot.send_message(message.from_user.id, '\u263A Привіт, {0}.'.
                             format(message.from_user.first_name),
                             reply_markup=my_keyboards.keyboard_start(message, ADMINS))
            bot.send_message(message.from_user.id, '\u263A{0}'.format(WELCOME_TEXT),
                             reply_markup=my_keyboards.keyboard_url_button(URL_BUTTON['WELCOME'], TEXT_URL['WELCOME']))
        my_database.write_new_user(message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.last_name,
                                   message.from_user.username)
        return
    else:
        if TEXT_URL['START'] == '' or URL_BUTTON['START'] == '':
            bot.send_message(message.from_user.id,
                             "\u263A Привіт, {0}. \U0001F449, "
                             "Щоб перейти далі, підпишись на канал @{1} та натисни /start. {2}".
                             format(message.from_user.first_name, CHANNEL_LIST, START_TEXT),
                             reply_markup=my_keyboards.keyboard_start_remove())
        elif TEXT_URL['START'] and URL_BUTTON['START']:
            bot.send_message(message.from_user.id,
                         "\u263A Привіт, {0}. \U0001F449, Щоб перейти далі, підпишись на канал @{1} та натисни /start".
                         format(message.from_user.first_name, CHANNEL_LIST), reply_markup=my_keyboards.keyboard_url_button(URL_BUTTON['START'], TEXT_URL['START']))


@bot.message_handler(content_types=['text'], func=lambda m: m.text == "Admin Panel" and m.from_user.id in ADMINS)
def start_panel(message):
    global ANSWERS_QUIZ
    global QUESTION_QUIZ
    global RIGHT_ANSWERS
    global RIGHT_ANSWER
    if len(ANSWERS_QUIZ) == len(QUESTION_QUIZ) == len(RIGHT_ANSWERS):
        bot.send_message(message.chat.id, 'Hi, Admin', reply_markup=my_keyboards.keyboard_admin())
    else:
        bot.send_message(ADMINS[0], "*Вікторина некоректна/!*", reply_markup=my_keyboards.keyboard_admin(),
                         parse_mode='MarkdownV2')
    bot.register_next_step_handler(message, admin_panel)


@bot.message_handler(content_types=['text'], func=lambda m: m.from_user.id in ADMINS and m.from_user.id == m.chat.id)
def admin_panel(message):
    if message.text == 'Add channel':
        bot.send_message(message.chat.id, "Із переліку каналів, де ти є адміном, обери потрібний, використовуючи кнопку",
                         reply_markup=my_keyboards.keyboard_add_channel())
    elif message.text == 'Clear channel list':
        global CHANNEL_DICTIONARY_BY_ID
        CHANNEL_DICTIONARY_BY_ID = {}
        global CHANNEL_ID
        global CHANNEL_LIST
        global CHANNEL_TITLE
        CHANNEL_ID = CHANNEL_DICTIONARY_BY_ID.keys()
        CHANNEL_TITLE = CHANNEL_DICTIONARY_BY_ID.values()
        CHANNEL_LIST = ''
        bot.reply_to(message, 'Список каналів очищеною.')
        print(CHANNEL_TITLE, CHANNEL_LIST)
    elif message.text == 'Create a quiz':
        bot.send_message(message.chat.id, "Щоб створити віктонину натисни кнопку нижче",
                         reply_markup=my_keyboards.keyboard_add_quiz())
        bot.register_next_step_handler(message, add_quiz)
    elif message.text == 'Clear the quiz':
        global ANSWERS_QUIZ
        global QUESTION_QUIZ
        global RIGHT_ANSWERS
        ANSWERS_QUIZ = []
        QUESTION_QUIZ = []
        RIGHT_ANSWERS = []
        bot.send_message(message.chat.id, 'Вікторину очищено', reply_markup=my_keyboards.keyboard_admin())
    elif message.text == 'Exit':
        bot.send_message(message.chat.id, 'Bye admin', reply_markup=my_keyboards.keyboard_start(message, ADMINS))
    elif message.text == 'Information':
        all_users, right_users = my_database.all_users()
        print(len(all_users), len(right_users))
        for item in ADMINS:
            bot.send_message(item, f'Кількість усіх користувачів - {len(all_users)}. \n'
                                   f'Кількість користувачів, які дали правильну відповідь - {len(right_users)}')
    elif message.text == "URL-button":
        bot.send_message(message.chat.id, "Щоб додати URL-кнопку натисни кнопку нижче",
                         reply_markup=my_keyboards.keyboard_сhange_button())
        bot.register_next_step_handler(message, button_change)
    elif message.text == "Change the text":
        bot.send_message(message.chat.id, "Щоб змінити потрібний текст натисни кнопку нижче",
                         reply_markup=my_keyboards.keyboard_сhange_text())
        bot.register_next_step_handler(message, text_change)
    elif message.text == 'Choose a quiz':
        bot.send_message(message.chat.id, 'Choose one of the quizzes',
                         reply_markup=my_keyboards.keyboard_two_quizzes())
        bot.register_next_step_handler(message, two_quizzes)
    elif message.text == 'The end':
        first_quiz_panel(message)
    else:
        bot.reply_to(message, 'Ups. Press /start')


# def two_quizzes(message):
#     if message.text == 'The first quiz':
#         first_quiz_panel(message)
#     elif message.text == 'The second quiz':
#         two_quiz_panel(message)
#     else:
#         bot.send_message(message.chat.id, "Bye",
#                          reply_markup=my_keyboards.keyboard_start(message, ADMINS))
#         bot.register_next_step_handler(message, send_welcome)


def add_quiz(message):
    global ANSWERS_QUIZ
    global QUESTION_QUIZ
    global RIGHT_ANSWERS
    if message.text == 'Add question':
        bot.reply_to(message, "Напиши запитання у текстовому полі та відправ його")
        bot.register_next_step_handler(message, admin_add_question)
    elif message.text == 'Add answer':
        bot.reply_to(message, "Напиши відповіді  у текстовому полі, роздідивши їх значком * та відправ їх")
        bot.register_next_step_handler(message, admin_add_answers)
    elif message.text == 'Right answer':
        bot.reply_to(message, "Напиши номер правильної відповіді  у текстовому полі, та відправ її")
        bot.register_next_step_handler(message, admin_add_right_answer)
    elif message.text == 'Back':
        # global ANSWERS_QUIZ
        # global QUESTION_QUIZ
        # global RIGHT_ANSWERS
        if len(ANSWERS_QUIZ) == len(QUESTION_QUIZ) == len(RIGHT_ANSWERS):
            bot.send_message(message.chat.id, 'Quiz updated', reply_markup=my_keyboards.keyboard_admin())
        else:
            ANSWERS_QUIZ = []
            QUESTION_QUIZ = []
            RIGHT_ANSWERS = []
            bot.send_message(ADMINS[0], "Вікторина некоректна. Вікторину очищено",
                             reply_markup=my_keyboards.keyboard_admin())
    else:
        bot.register_next_step_handler(message, add_quiz)


def admin_add_question(message):
    # global QUESTION_QUIZ
    QUESTION_QUIZ.append(message.text)
    bot.send_message(message.chat.id, "Add_question", reply_markup=my_keyboards.keyboard_add_quiz())
    print(QUESTION_QUIZ)
    bot.register_next_step_handler(message, add_quiz)


def admin_add_answers(message):
    global ANSWERS_QUIZ
    list_answers = message.text.split('*')
    if len(list_answers) > 1:
        ANSWERS_QUIZ.append(list_answers)
        bot.send_message(message.chat.id, "Add_answers", reply_markup=my_keyboards.keyboard_add_quiz())
        print(ANSWERS_QUIZ)
    else:
        bot.send_message(message.chat.id, "Некоректні дані, Спробуй знову",
                         reply_markup=my_keyboards.keyboard_add_quiz())
    bot.register_next_step_handler(message, add_quiz)


def admin_add_right_answer(message):
    global RIGHT_ANSWERS
    try:
        if message.text and int(message.text) <= len(ANSWERS_QUIZ[-1]):
            RIGHT_ANSWERS.append(int(message.text) - 1)
            bot.send_message(message.chat.id, "Add_right_answer", reply_markup=my_keyboards.keyboard_add_quiz())
        else:
            bot.send_message(message.chat.id, "Неправильне значення 1", reply_markup=my_keyboards.keyboard_add_quiz())
    except ValueError as e:
        bot.send_message(message.chat.id, "Неправильне значення 2", reply_markup=my_keyboards.keyboard_add_quiz())
        # bot.register_next_step_handler(message, add_quiz)
    print(QUESTION_QUIZ)
    print(ANSWERS_QUIZ)
    print(RIGHT_ANSWERS)
    bot.register_next_step_handler(message, add_quiz)


def text_change(message):
    if message.text == 'Welcome text':
        bot.reply_to(message, "Напиши вітальний текст у текстовому полі та відправ його")
        bot.register_next_step_handler(message, change_welcome_text)
    elif message.text == 'Final text':
        bot.reply_to(message, "Напиши фінальний текст у текстовому полі та відправ його")
        bot.register_next_step_handler(message, change_final_text)
    elif message.text == 'Start text':
        bot.reply_to(message, "Напиши фінальний текст у текстовому полі та відправ його")
        bot.register_next_step_handler(message, change_start_text)
    else:
        bot.send_message(message.chat.id, 'Bye', reply_markup=my_keyboards.keyboard_admin())
        bot.register_next_step_handler(message, admin_panel)


def change_welcome_text(message):
    global WELCOME_TEXT
    WELCOME_TEXT = message.text
    bot.reply_to(message, 'Вітальний текст змінено')
    bot.register_next_step_handler(message, text_change)


def change_final_text(message):
    global FINAL_TEXT
    FINAL_TEXT = message.text
    bot.reply_to(message, 'Фінальний текст змінено')
    bot.register_next_step_handler(message, text_change)


def change_start_text(message):
    global WELCOME_TEXT
    WELCOME_TEXT = message.text
    bot.reply_to(message, 'Вітальний текст змінено')
    bot.register_next_step_handler(message, text_change)


def button_change(message):
    text = "Напиши назву кнопки у текстовому полі та відправ"
    button = ''
    if message.text == 'Add start button':
        button = 'START'
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, button_name, button)
    elif message.text == 'Add final button':
        button = 'FINAL'
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, button_name, button)
    elif message.text == 'Add welcome button':
        button = 'WELCOME'
        bot.reply_to(message, text)
        bot.register_next_step_handler(message, button_name, button)
    elif message.text == "Del URL-button":
        bot.send_message(message.chat.id, "Обери повідомлення, з якого хочеш видалити URL-кнопку",
                         reply_markup=my_keyboards.keyboard_del_url_button())
    else:
        bot.send_message(message.chat.id, 'Bye', reply_markup=my_keyboards.keyboard_admin())
        bot.register_next_step_handler(message, admin_panel)


def button_name(message, button):
    global URL_BUTTON
    URL_BUTTON[button] = message.text
    if message.text != '':
        URL_BUTTON[button] = message.text
        bot.reply_to(message, "Add name URL-button.\nВведи посилання у текстовe полe та відправ його")
        bot.register_next_step_handler(message, button_text, button)
    else:
        bot.send_message(message.chat.id, "Некоректні дані, Спробуй знову",
                         reply_markup=my_keyboards.keyboard_сhange_button())
        bot.register_next_step_handler(message, button_change)


@bot.message_handler(content_types=['text'], func=lambda m: m.from_user.id == m.chat.id)
def start_user_panel(message):
    if message.text == 'Choose a quiz':
        bot.send_message(message.chat.id, 'Choose one of the quizzes',
                         reply_markup=my_keyboards.keyboard_two_quizzes())
        bot.register_next_step_handler(message, two_quizzes)
    elif message.text == 'The end':
        first_quiz_panel(message)


def two_quizzes(message):
    if message.text == 'The first quiz':
        first_quiz_panel(message)
    elif message.text == 'The second quiz':
        two_quiz_panel(message)
    else:
        bot.send_message(message.chat.id, "Bye",
                         reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        bot.register_next_step_handler(message, send_welcome)


def two_quiz_panel(message):
    if not is_subscribed(chat_ids=list(CHANNEL_ID), user_id=message.from_user.id):
        bot.send_message(message.from_user.id,
                         "\u263A Привіт, {0}. \U0001F449, Щоб перейти далі, підпишись на канал @{1} та натисни /start".
                         format(message.from_user.first_name, CHANNEL_LIST),
                         reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        bot.register_next_step_handler(message, send_welcome)
        return
    global ANSWERS_QUIZ_TWO
    global QUESTION_QUIZ_TWO
    global RIGHT_ANSWERS_TWO
    global RIGHT_ANSWER_TWO
    global NUMBER_CORRECT_ANSWERS_TWO
    answers_quiz = copy.deepcopy(ANSWERS_QUIZ_TWO)
    question_quiz = copy.deepcopy(QUESTION_QUIZ_TWO)
    right_answers = copy.deepcopy(RIGHT_ANSWERS_TWO)
    keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard1.add(*[telebot.types.KeyboardButton(item) for item in ANSWERS_QUIZ_TWO[-1]])
    keyboard1.add(*[telebot.types.KeyboardButton(name) for name in ['Continue', 'Back']])

    if message.text == "The second quiz" and len(ANSWERS_QUIZ_TWO) != 0 and len(ANSWERS_QUIZ_TWO) == len(QUESTION_QUIZ_TWO) == len(RIGHT_ANSWERS_TWO):
        text = 'quiz_two'
        while len(question_quiz) != 0:
            keyboard2 = telebot.types.InlineKeyboardMarkup(keyboard=None, row_width=2)
            for i in range(0, len(answers_quiz[-1])):
                print(answers_quiz[-1][i])
                uuu = telebot.types.InlineKeyboardButton(text=answers_quiz[-1][i],
                                                         callback_data=str(i))
                print(i)
                keyboard2.add(uuu)

            bot.send_message(message.chat.id, question_quiz[-1], reply_markup=keyboard2)
            RIGHT_ANSWER_TWO = right_answers[-1]
            answers_quiz.pop()
            question_quiz.pop()
            right_answers.pop()
        if len(question_quiz) == 0:
            bot.send_message(message.chat.id, 'Дай відповідь на ці запитання', reply_markup=my_keyboards.keyboard_two_question())
            bot.register_next_step_handler(message, continue_question, text)
    elif message.text == "The end":
        bot.send_message(message.chat.id, 'Bye', reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        if TEXT_URL['FINAL'] == '' or URL_BUTTON['FINAL'] == '':
            bot.reply_to(message, FINAL_TEXT)
        elif TEXT_URL['FINAL'] and URL_BUTTON['FINAL']:
            bot.send_message(message.from_user.id, FINAL_TEXT,
                             reply_markup=my_keyboards.keyboard_url_button(URL_BUTTON['FINAL'], TEXT_URL['FINAL']))
        # bot.register_next_step_handler(message, send_welcome)
    else:
        bot.send_message(message.chat.id, 'Ups. Press /start', reply_markup=my_keyboards.keyboard_start(message, ADMINS))


# @bot.message_handler(content_types=['text'], func=lambda m: m.from_user.id == m.chat.id)
def first_quiz_panel(message):
    if not is_subscribed(chat_ids=list(CHANNEL_ID), user_id=message.from_user.id):
        bot.send_message(message.from_user.id,
                         "\u263A Привіт, {0}. \U0001F449, Щоб перейти далі, підпишись на канал @{1} та натисни /start".
                         format(message.from_user.first_name, CHANNEL_LIST),
                         reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        bot.register_next_step_handler(message, send_welcome)
        return
    global ANSWERS_QUIZ
    global QUESTION_QUIZ
    global RIGHT_ANSWERS
    global RIGHT_ANSWER
    global NUMBER_CORRECT_ANSWERS
    answers_quiz = copy.deepcopy(ANSWERS_QUIZ)
    question_quiz = copy.deepcopy(QUESTION_QUIZ)
    right_answers = copy.deepcopy(RIGHT_ANSWERS)
    if message.text == "The first quiz" and len(ANSWERS_QUIZ) != 0 and len(ANSWERS_QUIZ) == len(QUESTION_QUIZ) == len(RIGHT_ANSWERS):
        text = 'quiz_one'
        while len(question_quiz) != 0:
            bot.send_poll(message.chat.id, question_quiz[-1], answers_quiz[-1], is_anonymous=False, type='quiz',
                          correct_option_id=right_answers[-1], open_period=60)
            RIGHT_ANSWER = right_answers[-1]
            answers_quiz.pop()
            question_quiz.pop()
            right_answers.pop()
        if len(question_quiz) == 0:
            bot.send_message(message.chat.id, 'Дай відповідь на ці запитання', reply_markup=my_keyboards.keyboard_two_question())
            bot.register_next_step_handler(message, continue_question, text)
    elif message.text == "The end":
        bot.send_message(message.chat.id, 'Bye', reply_markup=my_keyboards.keyboard_start(message, ADMINS))
        if TEXT_URL['FINAL'] == '' or URL_BUTTON['FINAL'] == '':
            bot.reply_to(message, FINAL_TEXT)
        elif TEXT_URL['FINAL'] and URL_BUTTON['FINAL']:
            bot.send_message(message.from_user.id, FINAL_TEXT,
                             reply_markup=my_keyboards.keyboard_url_button(URL_BUTTON['FINAL'], TEXT_URL['FINAL']))
        # bot.register_next_step_handler(message, send_welcome)
    else:
        bot.send_message(message.chat.id, 'Ups. Press /start', reply_markup=my_keyboards.keyboard_start(message, ADMINS))


def continue_question(message, text):
    global USER_ANSWERS
    number = 0
    print(message)
    user_answers = my_database.count_answers(text, message.from_user.id)
    if message.text == 'Bye' and text == 'quiz_one' and len(user_answers)-1 <= (len(RIGHT_ANSWERS)):
        user_answers.remove('9')
        reverse_right_answers = copy.deepcopy(RIGHT_ANSWERS)
        reverse_right_answers.reverse()
        for i in range(0, len(user_answers)):
            if user_answers[i] == str(reverse_right_answers[i]):
                number += 1
        bot.send_message(message.chat.id, "Вікторину завершено. Правильних відповідей - {0}".format(number),
                         reply_markup=my_keyboards.keyboard_two_quizzes())
        bot.register_next_step_handler(message, two_quizzes)
        if number == len(RIGHT_ANSWERS):
            my_database.right_answers(message.from_user.id)
        my_database.del_answers(message.from_user.id)
    elif message.text == 'Bye' and text == 'quiz_two':
        bot.send_message(message.chat.id, "Вікторину завершено. Правильних відповідей - {0} ".format(user_answers),
                         reply_markup=my_keyboards.keyboard_two_quizzes())
        my_database.del_answers_two(message.from_user.id)
        bot.register_next_step_handler(message, two_quizzes)
    else:
        bot.reply_to(message, 'Oh')
        my_database.del_answers(message.from_user.id)


@bot.poll_answer_handler(func=lambda call: True)
def info_answers(call):
    # global USER_ANSWERS
    # global NUMBER_CORRECT_ANSWERS
    answer = my_database.get_info_answers(call.user.id)
    print(answer, call.user.id)
    if answer is None:
        my_database.add_answers(call.option_ids[0], call.user.id)
    else:
        ans = str(answer) + str(call.option_ids[0])
        print(ans, call.user.id)
        my_database.add_answers(int(ans), call.user.id)


@bot.callback_query_handler(func=lambda call: "URL" in call.data)
def kill_url_button(call):
    print(call)
    global TEXT_URL
    global URL_BUTTON
    if call.data == "URL start":
        TEXT_URL['START'] = ''
        URL_BUTTON['START'] = ''
    elif call.data == "URL welcome":
        TEXT_URL['WELCOME'] = ''
        URL_BUTTON['WELCOME'] = ''
    elif call.data == "URL final":
        TEXT_URL['FINAL'] = ''
        URL_BUTTON['FINAL'] = ''
    else:
        bot.reply_to(call.message, 'Bad text')
    bot.register_next_step_handler(call.message, button_change)


@bot.callback_query_handler(func=lambda call: True)
def two(call):
    print(type(call.data))
    # print(call.message.text)
    print('call.data', call.data)
    print(call.message.text)
    text = 'quiz_two'
    global QUESTION_QUIZ_TWO
    global RIGHT_ANSWERS_TWO
    global RIGHT_ANSWER_TWO
    index_two = QUESTION_QUIZ_TWO.index(call.message.text)

    print('type' , type(index_two))
    print(call.from_user.id)
    print('index_two -', index_two, 'RIGHT_ANSWERS_TWO -', RIGHT_ANSWERS_TWO[index_two])
    if RIGHT_ANSWERS_TWO[index_two] == int(call.data):
        RIGHT_ANSWER_TWO += 1
        my_database.add_answers_two(call.from_user.id)
        bot.reply_to(call.message, "Good")
    else:
        bot.reply_to(call.message, "Bad")
    print(RIGHT_ANSWER_TWO)
    # bot.register_next_step_handler(call.message, continue_question, text)



@bot.message_handler(func=lambda message: message.entities is not None)
def button_text(message, button):
    print('222', button)
    print(message.entities)
    if message.entities is not None:
        for entity in message.entities:
            print(entity.type)
            if entity.type in ['url'] and (message.text.startswith('https://') or message.text.startswith('http:/')):
                global TEXT_URL
                TEXT_URL[button] = message.text
                print(TEXT_URL)
            else:
                send = '{0} {1} {2}'.format('Bad link', button, '-button. Try again')
                print(send)
                bot.reply_to(message, send)
    else:
        bot.reply_to(message, '{0} {1} {2}'.format('Bad link. Try again - press "Add', button.lower(), 'button"'))
    bot.register_next_step_handler(message, button_change)
    print('1')


if __name__ == "__main__":
    bot.polling()
    # bot.infinity_polling()
