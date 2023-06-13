import random
from aiogram.types import Message


def get_random_number() -> int:
    return random.randint(0, 101)

