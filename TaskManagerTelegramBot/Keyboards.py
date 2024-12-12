from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Добавить задачу")],
              [KeyboardButton(text="Удалить задачу")],
              [KeyboardButton(text="Обновить задачу")],
              [KeyboardButton(text="Показать все задачи")]],
resize_keyboard=True,
one_time_keyboard=True,
input_field_placeholder="Выберите одну из опций...")