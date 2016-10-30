import os
import json

from aiotg import Bot

from lib.db.models import User
from lib.db.models import Sport

bot = Bot(api_token=os.environ['API_KEY'])


@bot.command(r'/start')
def start(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    markup = {
        'keyboard': [["Choose sport"], ["Show rating"], ["Your bets"], ["Your balance"]],
        'one_time_keyboard': False
    }
    return chat.send_text(
        'Hello! Please make a bet. Your balance: {}'.format(user.balance),
        reply_markup=json.dumps(markup)
    )


@bot.command(r'Your balance')
def your_balance(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)

    return chat.send_text('Your balance: {}'.format(user.balance))


@bot.command(r'Choose sport')
def choose_sport(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)

    markup = {
        "keyboard": [],
        "one_time_keyboard": False
    }

    sports = Sport.select()
    for sport in sports:
        markup["keyboard"].append(['/sport {}'.format(sport.name)])

    return chat.send_text(
        'Ok, choose sport',
        reply_markup=json.dumps(markup)
    )


@bot.command(r'/sport (.+)')
def sport(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    sport_name = match.group(1)
    try:
        sport = Sport.get(name=sport_name)
    except Sport.DoesNotExist:
        return chat.send_text('Wow! We have no such sport')

    return chat.send_text('Wow! {} is a good choice'.format(sport.name))


@bot.command(r'/champ (.+)')
def championship(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    return chat.send_text('Great! You chose {}. Luck is on your side. Choose a game.'.format(match.group(1)))


@bot.command(r'/game (.+)')
def game(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    return chat.send_text('Great game! Coeffs are (1 - X - 2) : (1,26 - 2,34 - 2,75)')


@bot.command(r'/makebet (.+)')
def make_bet(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    return chat.send_text('Accepted! You will be noticed about results')


@bot.command(r'/result')
def sport(chat, match):
    user, _ = User.get_user_by_chat_id(chat.id)
    return chat.send_text('Your bet won!!! Your balance: 1026')

bot.run()
