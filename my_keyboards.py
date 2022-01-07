import telebot
from telebot import types


def keyboard_start(message, admins):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if message.from_user.id in admins and message.from_user.id == message.chat.id:
        keyboard.add(*[types.KeyboardButton(name) for name in ['Admin Panel']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Choose a quiz', 'The end']])
    return keyboard


def keyboard_start1(message, admins):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if message.from_user.id in admins and message.from_user.id == message.chat.id:
        keyboard.add(*[types.KeyboardButton(name) for name in ['Admin Panel']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Take the quiz', 'The end']])
    return keyboard


def keyboard_two_quizzes():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['The first quiz', 'The second quiz']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Back']])
    return keyboard


def keyboard_start_remove():
    start_keyboard = types.ReplyKeyboardRemove(selective=False)
    return start_keyboard


def keyboard_admin():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Add channel', 'Clear channel list']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Create a quiz', 'Clear the quiz']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Change the text', 'URL-button']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Information', 'Exit']])
    return keyboard


def keyboard_add_quiz():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Add question', 'Add answer']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Right answer', 'Back']])
    return keyboard


def keyboard_channel():
    start_keyboard = types.InlineKeyboardMarkup(keyboard=None, row_width=2)
    soroka = types.InlineKeyboardButton("Soroka", url='https://t.me/+FZKU6Vo-IAUxZDli')
    family = types.InlineKeyboardButton("MyFamily", url='https://t.me/+Y7FFqm-mrMliZDli')
    start_keyboard.add(soroka, family)
    return start_keyboard


def keyboard_add_channel():
    add_keyboard = types.InlineKeyboardMarkup(keyboard=None, row_width=2)
    add = types.InlineKeyboardButton("Add channel", switch_inline_query="add")
    # family = types.InlineKeyboardButton("MyFamily", url='https://t.me/+Y7FFqm-mrMliZDli')
    add_keyboard.add(add)
    return add_keyboard


def keyboard_poll():
    poll_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    poll_keyboard.add(telebot.types.KeyboardButton(text="Створити вікторину",
                                                   request_poll=types.KeyboardButtonPollType(type='quiz')))
    poll_keyboard.add(types.KeyboardButton(text="Information"))
    return poll_keyboard


def keyboard_two_question():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Bye']])
    return keyboard


def keyboard_сhange_text():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Start text', 'Welcome text']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Final text', 'Back']])
    return keyboard


def keyboard_сhange_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Add start button', 'Add welcome button']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Add final button', 'Del URL-button']])
    keyboard.add(*[types.KeyboardButton(name) for name in ['Back']])
    return keyboard


def keyboard_continue_question():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Continue', 'Back']])
    return keyboard


def keyboard_url_button(URL_button, text_URL):
    keyboard = types.InlineKeyboardMarkup(keyboard=None, row_width=2)
    url = types.InlineKeyboardButton(text=URL_button, url=text_URL)
    keyboard.add(url)
    return keyboard


def keyboard_add_url_button(name, text):
    keyboard = types.InlineKeyboardMarkup(keyboard=None, row_width=2)
    name_button = types.InlineKeyboardButton(text='Name button', callback_data=name)
    text_button = types.InlineKeyboardButton(text='Text URL', callback_data=text)
    keyboard.add(name_button, text_button)
    return keyboard


# def keyboard_add_url_button(name, text):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     keyboard.add(*[types.KeyboardButton(name) for name in ['Name button', 'Text URL']])
#     return keyboard


def keyboard_del_url_button():
    keyboard = types.InlineKeyboardMarkup(keyboard=None, row_width=3)
    start = types.InlineKeyboardButton(text='Start', callback_data='URL start')
    welcome = types.InlineKeyboardButton(text='Welcome', callback_data='URL welcome')
    final = types.InlineKeyboardButton(text='Final', callback_data='URL final')
    keyboard.add(start, welcome, final)
    return keyboard

