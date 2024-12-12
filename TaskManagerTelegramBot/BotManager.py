from datetime import datetime
from aiohttp.web_routedef import route
from sqlalchemy.util import await_only, await_fallback
from Task import *
from aiogram import Router, F, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import Keyboards as kb


router = Router()
task = Task()
class TaskAdder(StatesGroup):
    name = State()
    description = State()
    start_time = State()
    end_time = State()
    priority = State()

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
    await message.answer('Задача добавлена!')
    print(task.name, task.start_date, task.finish_date,task.priority)