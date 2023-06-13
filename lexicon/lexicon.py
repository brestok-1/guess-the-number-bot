from config_data.config import ATTEMPTS
from models.models import users

LEXICON_EN = {
    '/start': "Hello!\nLet's play the game 'Guess the number'!\n\n"
              'To get the rules of the game and the list of available '
              'commands - send a command /help',
    '/help': f'The rules:\n\nI guess a number from 1 to 100, '
             f'and you need to guess it\nYou have {ATTEMPTS} '
             f'attempts\n\nAvailable:\n/help - rules '
             f'of the game and list of commands\n/cancel - exit the game\n'
             f"/stat - show statistic\n\nLet's play?",
    '/cancel_in_game': "You're out of the game. If you want to play "
                       'again - write it',
    '/cancel_not_in_game': "We're not playing with you. "
                           "Can we play once?",
    'positive_answer': 'Hooray!\n\n I guessed a number from 1 to 100, '
                       'try to guess!',
    'negative_answer': "Sorry : (\n if you want to play - just write about it",
    "can't react": 'While we are playing in this game '
                   'I can react only to number from 1 to 100 '
                   'and to commands /cancel or /stat',
    'guessed': 'Hooray! You have guessed the number!\n\n Can we play some more?',
    'not_in_game': "We don't play the game. Do you want to start?",
    'number+': 'My number is bigger',
    'number-': 'My number is less',
    'other_in_game': 'We are currently playing. Please, send the numbers from 1 to 100',
    'other_not_in_game': "I don't understand you. Let's play the game!"
}


def get_phrase(key, message):
    lexicon_phrase = {
        '/stat': f'Total games: {users[message.from_user.id].total_games}\n'
                 f'Total wins: {users[message.from_user.id].wins}',
        'not_guessed': "Unfortunately, you haven't any more attempts. You have lost\n"
                       f"My number was {users[message.from_user.id].secret_number}. "
                       "Do you want to play again?",
    }
    return lexicon_phrase[key]
