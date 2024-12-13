from aiogram import Bot, Dispatcher
import asyncio
from BotManager import router

async def main():
    bot = Bot(token='7559173892:AAGF9i5R8FiGhdM6M4UpjycTWDa8ku2Fyc8')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 