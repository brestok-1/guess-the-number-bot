import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import Message, ContentType
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5


class User:
    in_game = False
    secret_number: int = None
    attempts: int = None
    total_games = 0
    wins = 0


users = {}


def get_random_number() -> int:
    return random.randint(0, 101)


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer("Hello!\nLet's play the game 'Guess the number'!\n\n"
                         'To get the rules of the game and the list of available '
                         'commands - send a command /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = User()


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(f'The rules:\n\nI guess a number from 1 to 100, '
                         f'and you need to guess it\nYou have {ATTEMPTS} '
                         f'attempts\n\nAvailable:\n/help - rules '
                         f'of the game and list of commands\n/cancel - exit the game\n'
                         f"/stat - show statistic\n\nLet's play?")


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Total games: {users[message.from_user.id].total_games}\n'
                         f'Total wins: {users[message.from_user.id].wins}')


@dp.message(Command(commands=['cancel']))
async def process_cancel_commands(message: Message):
    if users[message.from_user.id].in_game:
        await message.answer("You're out of the game. If you want to play "
                             'again - write it')
        users[message.from_user.id].in_game = False
    else:
        await message.answer("We're not playing with you. "
                             "Can we play once?")


@dp.message(Text(text=['Yes', 'Ok', 'Well', "Let's go", "Let's play"], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id].in_game:
        await message.answer('Hooray!\n\n I guessed a number from 1 to 100, '
                             'try to guess!')
        users[message.from_user.id].in_game = True
        users[message.from_user.id].secret_number = get_random_number()
        users[message.from_user.id].attempts = ATTEMPTS
    else:
        await message.answer('While we are playing in this game '
                             'I can react only to number from 1 to 100 '
                             'and to commands /cancel or /stat')


@dp.message(Text(text=["No", "I won't"], ignore_case=True))
async def process_negative_number(message: Message):
    if not users[message.from_user.id].in_game:
        await message.answer("Sorry : (\n if you want to play - just write about it")
    else:
        await message.answer('While we are playing in this game '
                             'I can react only to number from 1 to 100 '
                             'and to commands /cancel or /stat')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_number_answer(message: Message):
    if users[message.from_user.id].in_game:
        if int(message.text) == users[message.from_user.id].secret_number:
            await message.answer('Hooray! You have guessed the number!\n\n Can we play some more?')
            users[message.from_user.id].in_game = False
            users[message.from_user.id].wins += 1
            users[message.from_user.id].total_games += 1
        elif int(message.text) < users[message.from_user.id].secret_number:
            await message.answer('My number is bigger')
            users[message.from_user.id].attempts -= 1
        elif int(message.text) > users[message.from_user.id].secret_number:
            await message.answer('My number is less')
            users[message.from_user.id].attempts -= 1

        if users[message.from_user.id].attempts == 0:
            await message.answer("Unfortunately, you haven't any more attempts. You have lost\n"
                                 f"My number was {users[message.from_user.id].secret_number}. "
                                 "Do you want to play again?")
            users[message.from_user.id].in_game = False
            users[message.from_user.id].total_games += 1
    else:
        await message.answer("We don't play the game. Do you want to start?")


@dp.message()
async def process_other_text_answer(message: Message):
    if users[message.from_user.id].in_game:
        await message.answer('We are currently playing. Please, send the numbers from 1 to 100')
    else:
        await message.answer("I don't understand you. Let's play the game!")


if __name__ == '__main__':
    dp.run_polling(bot)
