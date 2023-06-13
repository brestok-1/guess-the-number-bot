from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message

from config_data.config import ATTEMPTS
from lexicon.lexicon import LEXICON_EN, get_phrase
from models.models import users, User
from utils.utils import get_random_number

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_EN['/start'])
    if message.from_user.id not in users:
        users[message.from_user.id] = User()


@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON_EN['/help'])


@router.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(get_phrase('/stat', message))


@router.message(Command(commands=['cancel']))
async def process_cancel_commands(message: Message):
    if users[message.from_user.id].in_game:
        await message.answer(LEXICON_EN['/cancel_in_game'])
        users[message.from_user.id].in_game = False
    else:
        await message.answer(LEXICON_EN['/cancel_not_in_game'])


@router.message(Text(text=['Yes', 'Ok', 'Well', "Let's go", "Let's play"], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id].in_game:
        await message.answer(LEXICON_EN['positive_answer'])
        users[message.from_user.id].in_game = True
        users[message.from_user.id].secret_number = get_random_number()
        users[message.from_user.id].attempts = ATTEMPTS
    else:
        await message.answer(LEXICON_EN["can't react"])


@router.message(Text(text=["No", "I won't"], ignore_case=True))
async def process_negative_number(message: Message):
    if not users[message.from_user.id].in_game:
        await message.answer(LEXICON_EN['negative_answer'])
    else:
        await message.answer(LEXICON_EN["can't react"])


@router.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if users[message.from_user.id].in_game:
        if int(message.text) == users[message.from_user.id].secret_number:
            await message.answer(LEXICON_EN['guessed'])
            users[message.from_user.id].in_game = False
            users[message.from_user.id].wins += 1
            users[message.from_user.id].total_games += 1
        elif int(message.text) < users[message.from_user.id].secret_number:
            await message.answer(LEXICON_EN['number+'])
            users[message.from_user.id].attempts -= 1
        elif int(message.text) > users[message.from_user.id].secret_number:
            await message.answer(LEXICON_EN['number-'])
            users[message.from_user.id].attempts -= 1

        if users[message.from_user.id].attempts == 0:
            await message.answer(get_phrase('not_guessed', message))
            users[message.from_user.id].in_game = False
            users[message.from_user.id].total_games += 1
    else:
        await message.answer(LEXICON_EN['not_in_game'])
