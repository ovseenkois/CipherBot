import logging

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import basic, caesar, visener, vernam, constants


async def main():
    logging.basicConfig(level=logging.INFO)
    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(constants.TOKEN)
    dp.include_router(caesar.router)
    dp.include_router(visener.router)
    dp.include_router(vernam.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())