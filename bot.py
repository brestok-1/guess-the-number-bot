import asyncio

from aiogram import Bot, Dispatcher

from config_data.config import load_config
from handlers import user_handlers, other_handlers


async def main() -> None:
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
