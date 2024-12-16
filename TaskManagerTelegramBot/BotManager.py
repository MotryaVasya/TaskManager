from datetime import datetime
from aiogram.client.session import aiohttp
from aiohttp.web_routedef import route
from Task import *
from aiogram import Router, F, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import Keyboards as kb
import requests

router = Router()
task = Task()
tasks = []
API_URL = "http://localhost:5000/tasks"

class TaskAdder(StatesGroup):
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()
class ShowAllTasks(StatesGroup):
    tasks = State()
class TaskDeletter(StatesGroup):
    task = State()
@router.message(CommandStart())
async def cmd_start(message: Message):
  await message.answer("С возвращением!",
                       reply_markup=kb.main)


@router.message(F.text == 'Добавить задачу')
async def task_add(message: Message, state: FSMContext):
    await state.set_state(TaskAdder.name)
    await message.answer('Введите название задачи!')
@router.message(TaskAdder.name)
async def get_name(message: Message, state: FSMContext):
    task.name = message.text
    await state.set_state(TaskAdder.description)
    await message.answer('Введите описание задачи!')
@router.message(TaskAdder.description)
async def get_description(message: Message, state: FSMContext):
    task.description = message.text
    await state.set_state(TaskAdder.start_time)
    await message.answer('Введите дату начала задачи (в формате дд.мм.гггг)!')
@router.message(TaskAdder.start_time)
async def get_start_time(message: Message, state: FSMContext):
    try:
        task.start_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.set_state(TaskAdder.end_time)
        await message.answer('Введите дату окончания задачи (в формате дд.мм.гггг)!')
    except ValueError:
        await message.answer('Неправильный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг')
@router.message(TaskAdder.end_time)
async def get_end_time(message: Message, state: FSMContext):
    try:
        task.finish_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.set_state(TaskAdder.priority)
        await message.answer('Введите приоритет задачи (от 1 до 9)!')
    except ValueError:
        await message.answer('Неправильный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг')
@router.message(TaskAdder.priority)
async def get_priority(message: Message, state: FSMContext):
    task.priority = message.text
    await state.clear()
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={
            'name': task.name,
            'description': task.description,
            'start_date': task.start_date.strftime("%d.%m.%Y"),
            'finish_date': task.finish_date.strftime("%d.%m.%Y"),
            'priority': task.priority
        }) as response:
            if response.status == 201:
                await message.answer("Задача добавлена!",
                       reply_markup=kb.main)
            else:
                await message.answer('Ошибка при добавлении задачи!')

    print(task.name, task.start_date, task.finish_date,task.priority)

@router.message(F.text == 'Показать все задачи')
async def show_all_tasks(message: Message, state: FSMContext):
    await state.set_state(ShowAllTasks.tasks)
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                tasks = await response.json()  # Получаем список задач в формате JSON
                if tasks:
                    tasks_list = ""
                    for task in tasks:
                        tasks_list += f"ID: {task['id']}, Название: {task['name']}, Описание: {task['description']}, " \
                                      f"Дата начала: {task['start_date']}, Дата окончания: {task['finish_date']}, " \
                                      f"Приоритет: {task['priority']}\n"
                    await message.answer(f"Вот все ваши задачи:\n{tasks_list}")
                else:
                    await message.answer('Нет задач для отображения.')
            else:
                await message.answer('Ошибка при получении задач!')
    state.clear()

@router.message(F.text == 'Удалить задачу')
async def delete_task(message: Message, state: FSMContext):
    await state.set_state(TaskDeletter.task)
    await show_all_tasks(message, state)
    await message.answer('Введите ID задачи, которую хотите удалить:')

@router.message(TaskDeletter.task)
async def get_task_id_for_deletion(message: Message, state: FSMContext):
    task_id = message.text
    try:
        task_id = int(task_id)  # Преобразуем текст в целое число
    except ValueError:
        await message.answer('Пожалуйста, введите корректный ID задачи.')
        return

    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/{task_id}") as response:
            if response.status == 204:
                await message.answer('Задача успешно удалена!')
            elif response.status == 404:
                await message.answer('Задача не найдена. Проверьте ID и попробуйте снова.')
            else:
                await message.answer('Ошибка при удалении задачи!')

    await state.clear()  # Сброс состояния после завершения операции