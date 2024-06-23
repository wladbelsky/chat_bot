from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database.models import TelegramUser
from database.postgres import Database

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    db = Database()
    async with db.get_session() as session:
        user = TelegramUser(
            id=message.from_user.id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
            created_at=message.date,
            updated_at=message.date,
        )
        session.add(user)
        await session.commit()
    await message.answer(f"Привет, {message.from_user.full_name}!")
