import os
import json

from aiotg import Bot

bot = Bot(api_token=os.environ['API_KEY'])


@bot.command(r'/start')
def start(chat, match):
    markup = {
        "keyboard": [["Make a bet"], ["Show rating"], ["Your bets"]],
        "one_time_keyboard": True
    }
    return chat.send_text('Hi!', reply_markup=json.dumps(markup))


@bot.command(r'/makebet')
def make_bet(chat, match):
    pass

bot.run()
