from aiogram.client.session import aiohttp
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


@router.message(CommandStart())
async def cmd_start(message: Message):
  await message.answer("С возвращением!",
                       reply_markup=kb.main)

#<editor-fold desc="TASK_ADD">
class TaskAdder(StatesGroup):
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()
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
                await message.answer('Ошибка при добавлении задачи!', reply_markup=kb.main)

    print(task.name, task.start_date, task.finish_date,task.priority)
#</editor-fold>

#<editor-fold desc="SHOW_ALL_TASKS">
class ShowAllTasks(StatesGroup):
    tasks = State()
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
                        tasks_list += (
                            f"ID: {task['id']}\n"
                            f"Название: {task['name']}\n"
                            f"Описание: {task['description']}\n"
                            f"Дата начала: {task['start_date']}\n"
                            f"Дата окончания: {task['finish_date']}\n"
                            f"Приоритет: {task['priority']}\n"
                            "-------------------------\n"
                        )
                    await message.answer(f"Вот все ваши задачи:\n{tasks_list}", reply_markup=kb.main)
                else:
                    await message.answer('Нет задач для отображения.', reply_markup=kb.main)
            else:
                await message.answer('Ошибка при получении задач!', reply_markup=kb.main)

    await state.clear()
#</editor-fold>

#<editor-fold desc="TASK_DELETE">
class TaskDeleter(StatesGroup):
    task = State()
@router.message(F.text == 'Удалить задачу')
async def delete_task(message: Message, state: FSMContext):
    await show_all_tasks(message, state)
    await state.set_state(TaskDeleter.task)
    await message.answer('Введите ID задачи, которую хотите удалить:')
@router.message(TaskDeleter.task)
async def get_task_id_for_deletion(message: Message, state: FSMContext):

    while True:
        task_id = message.text
        try:
            task_id = int(task_id)  # Преобразуем текст в целое число
        except ValueError:
            await message.answer('Пожалуйста, введите корректный ID задачи.')
            return

        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{API_URL}/{task_id}") as response:
                if response.status == 204:
                    await message.answer('Задача успешно удалена!', reply_markup=kb.main)
                    await state.clear()
                    break
                elif response.status == 404:
                    await show_all_tasks(message, state)
                    await message.answer('Задача не найдена. Проверьте ID и попробуйте снова.')
                    return
                else:
                    await message.answer('Ошибка при удалении задачи!', reply_markup=kb.main)
                    await state.clear()
                    break
#</editor-fold>

#<editor-fold desc="TASK_UPDATE">
class TaskUpdater(StatesGroup):
    task_id = State()
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()

@router.message(F.text == 'Обновить задачу')
async def update_task(message: Message, state: FSMContext):
    await show_all_tasks(message, state)
    await message.answer('Введите ID задачи, которую хотите обновить:')
    await state.set_state(TaskUpdater.task_id)

@router.message(TaskUpdater.task_id)
async def get_task_id_for_update(message: Message, state: FSMContext):
    task_id = message.text
    try:
        task_id = int(task_id)  # Преобразуем текст в целое число
    except ValueError:
        await message.answer('Пожалуйста, введите корректный ID задачи.')
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/{task_id}") as response:
            if response.status == 200:
                task = await response.json()
                await state.update_data(task_id=task_id, name=task['name'], description=task['description'],
                                         start_date=task['start_date'], finish_date=task['finish_date'],
                                         priority=task['priority'])
                await message.answer(f"Текущие данные задачи:\n"
                                     f"Название: {task['name']}\n"
                                     f"Описание: {task['description']}\n"
                                     f"Дата начала: {task['start_date']}\n"
                                     f"Дата окончания: {task['finish_date']}\n"
                                     f"Приоритет: {task['priority']}\n"
                                     "Введите новое название задачи (или введите 'пропустить' для сохранения текущего):")
                await state.set_state(TaskUpdater.name)
            elif response.status == 404:
                await message.answer('Задача не найдена. Проверьте ID и попробуйте снова.')
            else:
                await message.answer('Ошибка при получении задачи!', reply_markup=kb.main)

@router.message(TaskUpdater.name)
async def get_new_name(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_name = data.get('name')  # Получаем текущее значение

    new_name = message.text
    if new_name.lower() != 'пропустить':
        await state.update_data(name=new_name)
    else:
        await state.update_data(name=current_name)  # Сохраняем предыдущее значение

    await message.answer('Введите новое описание задачи (или введите "пропустить" для сохранения текущего):')
    await state.set_state(TaskUpdater.description)

@router.message(TaskUpdater.description)
async def get_new_description(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_description = data.get('description')  # Получаем текущее значение

    new_description = message.text
    if new_description.lower() != 'пропустить':
        await state.update_data(description=new_description)
    else:
        await state.update_data(description=current_description)  # Сохраняем предыдущее значение

    await message.answer('Введите новую дату начала задачи (в формате дд.мм.гггг, или введите "пропустить" для сохранения текущей):')
    await state.set_state(TaskUpdater.start_time)

@router.message(TaskUpdater.start_time)
async def get_new_start_time(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_start_date = data.get('start_date')  # Получаем текущее значение

    new_start_date = message.text
    if new_start_date.lower() != 'пропустить':
        try:
            new_start_date = datetime.strptime(new_start_date, "%d.%m.%Y")
            await state.update_data(start_date=new_start_date.strftime("%d.%m.%Y"))
        except ValueError:
            await message.answer('Неправильный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг')
            return
    else:
        await state.update_data(start_date=current_start_date)  # Сохраняем предыдущее значение

    await message.answer('Введите новую дату окончания задачи (в формате дд.мм.гггг, или введите "пропустить" для сохранения текущей):')
    await state.set_state(TaskUpdater.end_time)

@router.message(TaskUpdater.end_time)
async def get_new_end_time(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_end_date = data.get('finish_date')  # Получаем текущее значение

    new_end_date = message.text
    if new_end_date.lower() != 'пропустить':
        try:
            new_end_date = datetime.strptime(new_end_date, "%d.%m.%Y")
            await state.update_data(finish_date=new_end_date.strftime("%d.%m.%Y"))
        except ValueError:
            await message.answer('Неправильный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг')
            return
    else:
        await state.update_data(finish_date=current_end_date)  # Сохраняем предыдущее значение

    await message.answer('Введите новый приоритет задачи (от 1 до 9, или введите "пропустить" для сохранения текущего):')
    await state.set_state(TaskUpdater.priority)

@router.message(TaskUpdater.priority)
async def get_new_priority(message: Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    current_priority = data.get('priority')  # Получаем текущее значение

    new_priority = message.text
    if new_priority.lower() != 'пропустить':
        try:
            new_priority = int(new_priority)
            if new_priority < 1 or new_priority > 9:
                raise ValueError
            await state.update_data(priority=new_priority)
        except ValueError:
            await message.answer('Пожалуйста, введите корректный приоритет от 1 до 9.')
            return
    else:
        await state.update_data(priority=current_priority)  # Сохраняем предыдущее значение

    # Получаем обновленные данные и отправляем запрос на обновление
    updated_data = {
        'name': data.get('name'),
        'description': data.get('description'),
        'start_date': data.get('start_date'),
        'finish_date': data.get('finish_date'),
        'priority': data.get('priority')
    }

    async with aiohttp.ClientSession() as session:
        async with session.put(f"{API_URL}/{task_id}", json=updated_data) as response:
            if response.status == 200:
                await message.answer("Задача успешно обновлена!", reply_markup=kb.main)
            else:
                await message.answer('Ошибка при обновлении задачи!', reply_markup=kb.main)

    await state.clear()  # Сброс состояния после завершения операции

#</editor-fold>