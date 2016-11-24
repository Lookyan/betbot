import os
import json

from aiotg import Bot

from lib.db.models import User
from lib.db.models import Sport
from lib.db.models import Tournament
from lib.db.models import Match
from lib.db.connection import psql_db
from lib.db.connection import database_manager


MAIN_MENU_STR = 'Main menu'

bot = Bot(api_token=os.environ['API_KEY'])


@bot.command(r'/start|{}'.format(MAIN_MENU_STR))
async def start(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)
    markup = {
        'keyboard': [["Choose sport"], ["Your bets"], ["My balance"], ["Show rating"]],
        'one_time_keyboard': False
    }
    await chat.send_text(
        'You can make a bet. Your balance: {}'.format(user.balance),
        reply_markup=json.dumps(markup)
    )


@bot.command(r'My balance')
async def your_balance(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    await chat.send_text('Your balance: {}'.format(user.balance))


@bot.command(r'Choose sport')
async def choose_sport(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    markup = {
        "keyboard": [],
        "one_time_keyboard": False
    }

    sports = await database_manager.execute(Sport.select())
    for sport in sports:
        markup["keyboard"].append(['/sport {}'.format(sport.name)])

    markup["keyboard"].append([MAIN_MENU_STR])

    await chat.send_text(
        'Ok, choose sport',
        reply_markup=json.dumps(markup)
    )


@bot.command(r'/sport (.+)')
async def sport(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)
    sport_name = match.group(1)
    try:
        sport = await database_manager.get(
            Sport,
            name=sport_name
        )
        user.chosen_sport = sport
        await database_manager.update(user)

        tournaments = await database_manager.execute(
            Tournament.select().where(Tournament.sport == sport)
        )
        markup = {
            "keyboard": [],
            "one_time_keyboard": False
        }
        for tournament in tournaments:
            markup['keyboard'].append(['/champ {}'.format(tournament.name)])

        markup['keyboard'].append([MAIN_MENU_STR])
    except Sport.DoesNotExist:
        await chat.send_text('Wow! We have no such sport')  # TODO: fix error handling
        return
    except Exception as e:
        psql_db.rollback()
        await chat.send_text('Wrong sport...')
        return

    await chat.send_text(
        'Wow! {} is a good choice! Please choose a tournament.'.format(sport.name),
        reply_markup=json.dumps(markup)
    )


@bot.command(r'/champ (.+)')
async def championship(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    tournament = await database_manager.get(
        Tournament.select().where(Tournament.name == match.group(1))
    )
    user.chosen_tournament = tournament
    await database_manager.update(user)

    matches = await database_manager.execute(
        Match.select().where(Match.tournament == tournament, Match.match_status == False)
    )

    markup = {
        "keyboard": [],
        "one_time_keyboard": False
    }

    for sport_match in matches:
        markup['keyboard'].append(
            ['/game {} - {} ({})'.format(sport_match.player1, sport_match.player2, sport_match.date)]
        )

    markup['keyboard'].append([MAIN_MENU_STR])

    await chat.send_text(
        'Great! You chose {}. Luck is on your side. Choose a game.'.format(match.group(1)),
        reply_markup=json.dumps(markup)
    )


@bot.command(r'/game (.+)')
async def game(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    # get players
    # TODO: error handling
    player1, player2 = match.group(1).split(' (', 1)[0].split(' - ', 1)

    # find a match
    current_match = await database_manager.get(
        Match.select().where(Match.player1 == player1, Match.player2 == player2)  # TODO: add time determination
    )

    user.chosen_match = current_match
    await database_manager.update(user)

    markup = {
        "keyboard": [
            ['/makebet win1'],
            ['/makebet draw'],
            ['/makebet win2']
        ],
        "one_time_keyboard": False
    }

    markup['keyboard'].append([MAIN_MENU_STR])

    await chat.send_text(
        'Great game! \n {} \nCoeffs are (1 - X - 2) : \n({} - {} - {})'.format(
            match.group(1),
            current_match.win1,
            current_match.draw,
            current_match.win2
        ),
        reply_markup=json.dumps(markup)
    )


@bot.command(r'/makebet (.+)')
async def make_bet(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    await chat.send_text('Accepted! You will be noticed about results')


@bot.command(r'/result')
async def sport(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)
    await chat.send_text('Your bet won!!! Your balance: 1026')


@bot.command('whoami')
async def whoami(chat, match):
    await chat.reply(chat.sender['id'])

if __name__ == '__main__':
    bot.run()
