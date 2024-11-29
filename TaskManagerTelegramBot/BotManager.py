import telebot
from telebot import types
from MessageInfo import MessageInfo, TypeMessage

MessageInfo.Num = 0
bot = telebot.TeleBot('7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8')
mm = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)


@bot.message_handler(commands=['start'])
def start(message):
    button_add_task = types.KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskAdd))
    button_delete_task = types.KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskDelete))
    button_update_task = types.KeyboardButton(MessageInfo.GetMessage(TypeMessage.TaskUpdate))
    button_show_tasks = types.KeyboardButton(MessageInfo.GetMessage(TypeMessage.ShowTasks))
    button_modify_language = types.KeyboardButton(MessageInfo.GetMessage(TypeMessage.ModifyLanguage))
    mm.add(button_add_task, button_delete_task, button_update_task, button_show_tasks, button_modify_language)
    bot.send_message(message.chat.id, MessageInfo.GetMessage(TypeMessage.WelcomeBack), reply_markup=mm)
def ModifyLanguage():
    if MessageInfo.Num == 0:
        MessageInfo.Num = 1
    else:
        MessageInfo.Num = 0

@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == MessageInfo.GetMessage(TypeMessage.TaskAdd):
        bot.send_message(message.chat.id, "Привет!")
    if message.text == MessageInfo.GetMessage(TypeMessage.TaskDelete):
        bot.send_message(message.chat.id, "Отлично!")
    if message.text == MessageInfo.GetMessage(TypeMessage.WelcomeBack):
        ModifyLanguage()
def infinity():
    bot.infinity_polling()