from datetime import date
import telebot
from telebot import types
import Task
from MessageInfo import MessageInfo as MI, TypeMessage
from Task import *

bot = telebot.TeleBot('7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8')
mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)



def check_started_bot(message): # переставить поле count в другой класс
    if MI.count > 0:
        bot.send_message(message.chat.id, MI.GetMessage(TypeMessage.ThisBotStarted))
        return False
    else:
        MI.count += 1
        return True

def ModifyLanguage():
    if MI.Num == 0:
        MI.Num = 1
    else:
        MI.Num = 0


@bot.message_handler(commands=['start'])
def start(message):
    if check_started_bot(message):
        button_add_task = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskAdd))
        button_delete_task = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskDelete))
        button_update_task = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskUpdate))
        button_show_tasks = types.KeyboardButton(MI.GetMessage(TypeMessage.ShowTasks))
        button_modify_language = types.KeyboardButton(MI.GetMessage(TypeMessage.ModifyLanguage))
        bot.send_message(message.chat.id, MI.GetMessage(TypeMessage.WelcomeBack), reply_markup=mm)
        mm.add(button_add_task, button_delete_task, button_update_task, button_show_tasks, button_modify_language)
    else:
        return



@bot.message_handler(func=lambda message: message.text == MI.GetMessage(TypeMessage.ModifyLanguage) and MI.Num == 1 or MI.Num == 0)
def modify_language(message):
    ModifyLanguage()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskAdd))
    button2 = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskDelete))
    button3 = types.KeyboardButton(MI.GetMessage(TypeMessage.TaskUpdate))
    button4 = types.KeyboardButton(MI.GetMessage(TypeMessage.ShowTasks))
    button5 = types.KeyboardButton(MI.GetMessage(TypeMessage.ModifyLanguage))
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, MI.GetMessage(TypeMessage.LanguageModified), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == MI.GetMessage(TypeMessage.TaskAdd) and MI.Num == 1 or MI.Num == 0)
def Task_Add(message):# доделать метод
    bot.send_message(message.chat.id, "Введите название задачи!")
    name = ""
    description = ""
    start_time = date
    end_time = date
    priority = 0


    task = Task.Task(name, description, start_time, end_time, priority)

def save_name(message):
        # Сохраняем текст следующего сообщения в переменную name
    name = message.chat.id+1
        # Для примера выведем имя и подтвердим его сохранение
    return name
        # Здесь можно выполнить дополнительные действия с переменной `task`


def infinity():
    bot.infinity_polling()