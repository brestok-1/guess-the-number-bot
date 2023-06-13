from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_EN
from models.models import users

router = Router()


@router.message()
async def process_other_text_answer(message: Message):
    if users[message.from_user.id].in_game:
        await message.answer(LEXICON_EN['other_in_game'])
    else:
        await message.answer(LEXICON_EN['other_not_in_game'])
