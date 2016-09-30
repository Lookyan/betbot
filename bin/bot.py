import os
import json

from aiotg import Bot

bot = Bot(api_token=os.environ['API_KEY'])


@bot.command(r'/start')
def start(chat, match):
    markup = {
        "keyboard": [["Make a bet"], ["Show rating"], ["F**k off"]],
        "one_time_keyboard": True
    }
    return chat.send_text('Hi!', reply_markup=json.dumps(markup))

bot.run()
