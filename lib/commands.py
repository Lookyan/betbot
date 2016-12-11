from datetime import datetime
import os
import json
import logging

from aiotg import Bot

from lib.db.models import User
from lib.db.models import Sport
from lib.db.models import Tournament
from lib.db.models import Match
from lib.db.models import Bet
from lib.db.connection import psql_db
from lib.db.connection import database_manager
from lib.emoji import get_digit_smile


MAIN_MENU_STR = 'Main menu'

bot = Bot(api_token=os.environ['API_KEY'])
logger = logging.getLogger(__name__)


def get_reply_markup(keyboard: list) -> dict:
    markup = {
        'keyboard': keyboard,
        'one_time_keyboard': False
    }
    markup["keyboard"].append([MAIN_MENU_STR])

    return json.dumps(markup)


@bot.command(r'/start|{}'.format(MAIN_MENU_STR))
async def start(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)
    markup = {
        'keyboard': [["Choose sport"], ["My bets"], ["My balance"], ["Show rating"]],
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

    keyboard = []

    sports = await database_manager.execute(Sport.select())
    for sport in sports:
        keyboard.append(['/sport {}'.format(sport.name)])

    await chat.send_text(
        'Ok, choose sport',
        reply_markup=get_reply_markup(keyboard)
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
        keyboard = []
        for tournament in tournaments:
            tournament_games_count = await database_manager.count(
                Match.select().where(
                    Match.tournament == tournament,
                    Match.match_status == False,
                    Match.date > datetime.utcnow()
                )
            )
            if tournament_games_count != 0:
                keyboard.append(['/champ {}'.format(tournament.name)])

    except Sport.DoesNotExist:
        return await chat.send_text('Wow! We have no such sport')
    except Exception as e:
        psql_db.rollback()
        return await chat.send_text('Wrong sport...')

    await chat.send_text(
        'Wow! {} is a good choice! Please choose a tournament.'.format(sport.name),
        reply_markup=get_reply_markup(keyboard)
    )


@bot.command(r'/champ (.+)')
async def championship(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    try:
        tournament = await database_manager.get(
            Tournament.select().where(Tournament.name == match.group(1))
        )
    except Tournament.DoesNotExist:
        return await chat.send_text('Unfortunately we have no such tournament')

    user.chosen_tournament = tournament
    await database_manager.update(user)

    matches = await database_manager.execute(
        Match.select().where(
            Match.tournament == tournament,
            Match.match_status == False,
            Match.date > datetime.utcnow()
        )
    )

    keyboard = []

    for sport_match in matches:
        keyboard.append(
            ['/game {} - {} ({})'.format(sport_match.player1, sport_match.player2, sport_match.date)]
        )

    await chat.send_text(
        'Great! You chose {}. Luck is on your side. Choose a game.'.format(match.group(1)),
        reply_markup=get_reply_markup(keyboard)
    )


@bot.command(r'/game (.+)')
async def game(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    # get players
    try:
        players, date = match.group(1).split(' (', 1)
        player1, player2 = players.split(' - ', 1)
        date = date[:-2]
    except (IndexError, ValueError):
        return await chat.send_text('Unfortunately we have no such game')

    # find a match
    try:
        current_match = await database_manager.get(
            Match.select().where(
                Match.player1 == player1,
                Match.player2 == player2,
                Match.date == date
            )
        )
    except Match.DoesNotExist:
        return await chat.send_text(
            'Unfortunately we have no such game'
        )

    if not current_match.check_actual():
        return await chat.send_text('Match has been already started, you can\'t make a bet.')

    user.chosen_match = current_match
    await database_manager.update(user)

    keyboard = [
        ['/makebet win1'],
        ['/makebet draw'],
        ['/makebet win2']
    ]

    await chat.send_text(
        'Great game! \n {} \nCoeffs are (1 - X - 2) : \n({} - {} - {})'.format(
            match.group(1),
            current_match.win1,
            current_match.draw,
            current_match.win2
        ),
        reply_markup=get_reply_markup(keyboard)
    )


@bot.command(r'/makebet (.+)')
async def make_bet(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    # get chosen match
    chosen_match = user.chosen_match

    if not chosen_match.check_actual():
        return await chat.send_text(
            'Match {}-{} has been already started, you can\'t make a bet.'.format(
                chosen_match.player1, chosen_match.player2
            )
        )

    choice = match.group(1)

    res = await user.save_chosen_result(choice)

    if not res:
        return await chat.send_text('Smth went wrong!')

    await database_manager.update(user)

    await chat.send_text(
        'Please enter amount. Your balance {}'.format(user.balance),
        reply_markup=get_reply_markup([])
    )


@bot.command(r'^[+]?\d+([.]\d+)?$')
async def amount(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    try:
        amount = float(match.group())
    except (ValueError, TypeError):
        return await chat.send_text(
            'Wrong amount. Please reenter.'
        )

    if user.balance < amount:
        return await chat.send_text(
            'You have only {}\nPlease reenter'.format(user.balance)
        )

    chosen_match = user.chosen_match

    if not chosen_match:
        return await chat.send_text(
            'Please choose a match first'
        )

    if not chosen_match.check_actual():
        return await chat.send_text(
            'Match {}-{} has been already started, you can\'t make a bet.'.format(
                chosen_match.player1, chosen_match.player2
            )
        )

    # bet creation

    chosen_match = user.chosen_match

    bet_coeff = chosen_match.get_coeff_by_chosen_result(user.chosen_result)

    bet = {
        'user': user,
        'match': chosen_match,
        'amount': amount,
        'bet_coeff': bet_coeff,
        'bet_type': user.chosen_result
    }

    # TODO: transaction mechanism
    await database_manager.create(Bet, **bet)

    user.balance -= amount
    await database_manager.update(user)

    await chat.send_text(
        'Accepted! You will be noticed about results'
    )


@bot.command(r'My bets')
async def your_bets(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    bets = await database_manager.execute(
        Bet.select().where(Bet.user == user, Bet.bet_status == False)
    )

    fmt_bets = ''
    for bet in bets:
        current_bet = '{}-{} [Amount: {} Coeff: {} Result: {}]\n\n'.format(
            bet.match.player1,
            bet.match.player2,
            bet.amount,
            bet.bet_coeff,
            Match.get_text_result(bet.bet_type)
        )
        fmt_bets += current_bet

    await chat.send_text(
        'Your current bets\n\n{}'.format(fmt_bets)
    )


@bot.command(r'Show rating')
async def show_rating(chat, match):
    user, _ = await User.get_user_by_chat_id(chat.id)

    rank = await database_manager.count(User.select().where(User.balance > user.balance))

    # top 3 users
    rank_table = await database_manager.execute(
        User.select().order_by(User.balance.desc()).limit(3)
    )

    top = ''
    for pos, item in enumerate(rank_table):
        current_user = '{} - {} points\n'.format(get_digit_smile(pos + 1), item.balance)
        top += current_user

    await chat.send_text(
        'Your rank is {}.\nHere is a top 3 players:\n{}'.format(rank + 1, top)
    )


@bot.command(r'whoami')
async def whoami(chat, match):
    await chat.reply(chat.sender['id'])
