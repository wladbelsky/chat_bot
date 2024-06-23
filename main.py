import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from routes.gpt import router as gpt_router
from routes.start import router as start_router
from config import TOKEN, WEBHOOK_PATH, WEBHOOK_SECRET, BASE_WEBHOOK_URL, WEB_SERVER_HOST, WEB_SERVER_PORT, DB_CONFIG
from database.postgres import Database


async def register_webhook(bot: Bot) -> None:
    await bot.set_webhook(
        url=f"{BASE_WEBHOOK_URL}/{WEBHOOK_PATH}",
        secret_token=WEBHOOK_SECRET,
    )


async def prepare_db() -> None:
    db = Database(DB_CONFIG)
    await db.prepare_tables()


async def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("aiogram").setLevel(logging.INFO)


def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(prepare_db)
    dp.startup.register(setup_logging)
    dp.include_router(start_router)
    dp.include_router(gpt_router)
    if BASE_WEBHOOK_URL and WEBHOOK_PATH:
        dp.startup.register(register_webhook)
        app = web.Application()
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)
        setup_application(app, dp, bot=bot)
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    else:
        asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
