import datetime

import requests
import peewee
from bs4 import BeautifulSoup

from lib.db.models import Sport
from lib.db.models import Match
from lib.db.models import Tournament
from lib.db.connection import psql_db

soccer_leagues = [
    '/england/premier-league/',
    '/france/ligue-1/',
    '/germany/bundesliga/',
    '/italy/serie-a/',
    '/netherlands/eredivisie/',
    '/spain/laliga/',
    '/europe/champions-league/',
    '/europe/europa-league/',
    '/world/world-cup/',  # world cup 2018 Russia
    '/russia/premier-league/'
]

base_url = 'http://www.soccer24.com'

JS_ROW_END = '~'
JS_CELL_END = '¬'
JS_INDEX = '÷'
LEAGUE_INDEX = 'ZA'
SPORT_INDEX = 'SA'
EVENT_INDEX = 'AA'
MOVED_EVENTS_INDEX = 'QA'
TOP_LEAGUES_INDEX = 'SG'
U_304_INDEX = 'A1'
REFRESH_UTIME_INDEX = 'A2'
DOWNLOAD_UL_FEED_INDEX = 'UL'
PAST_FUTURE_GAMES_INDEX = 'FG'
PARTICIPANT_INDEX = 'PR'
SPECIAL_INDEX = 'ST'
STATS_RESULTS_TYPE_INDEX = 'RAA'
STATS_RESULTS_VALUE_INDEX = 'RAB'
feed_sign = 'SW9D1eZo'
u_304 = 'd41d8cd98f00b204e9800998ecf8427e'


def transform_to_dict(cells):
    result_dict = {}
    for cell in cells:
        indexes = cell.split(JS_INDEX)
        if len(indexes) >= 2:
            result_dict[indexes[0]] = indexes[1]

    return result_dict


def get_odds(event_id):
    r = requests.get(base_url + '/x/feed/df_dos_2_' + event_id + '_', headers={'X-Fsign': feed_sign})
    content = r.content.decode()
    return parse_odds(content)


def parse_odds(content):
    cells = content.split(JS_CELL_END)
    data = transform_to_dict(cells)
    if 'MI' in data:
        return tuple(data['MI'].split('|'))


def parse(content, match_result=False):
    data = content.split(JS_ROW_END)
    result = {
        'games': []
    }
    for row in data:
        sport_data = row.split(JS_CELL_END)
        if sport_data[0].startswith(SPORT_INDEX):
            indexes = sport_data[0].split(JS_INDEX)
            result['sport_id'] = indexes[1]
        elif sport_data[0].startswith(LEAGUE_INDEX):
            indexes = sport_data[0].split(JS_INDEX)
            result['league_name'] = indexes[1]
        elif sport_data[0].startswith(EVENT_INDEX):
            events = transform_to_dict(sport_data)
            game = {}
            if 'AA' in events:
                game['event_id'] = events['AA']
                if match_result:
                    game['odds'] = get_odds(game['event_id'])
                    if '-' in game['odds']:
                        continue
            if 'AE' in events:
                game['home'] = events['AE']
            if 'AF' in events:
                game['away'] = events['AF']
            if 'AD' in events:
                game['timestamp'] = events['AD']
            if 'AG' in events:
                game['home_goals'] = events['AG']
            if 'AH' in events:
                game['away_goals'] = events['AH']
            if 'AS' in events:
                game['winner'] = events['AS']  # 1 if home is winner, 2 if away is winner, draw otherwise
            result['games'].append(game)

    return result


if __name__ == '__main__':

    sport_name = 'soccer'
    sport, _ = Sport.get_or_create(name=sport_name)

    for league in soccer_leagues:

        r = requests.get(base_url + league)
        content = r.content.decode()
        soup = BeautifulSoup(content, 'html.parser')
        upcoming_matches_data = soup.find(id='tournament-page-data-summary-fixtures').next
        upcoming_matches = parse(upcoming_matches_data, match_result=True)

        matches_results_data = soup.find(id='tournament-page-data-summary-results').next
        matches_results = parse(matches_results_data)

        # add upcoming matches

        tournament, _ = Tournament.get_or_create(name=upcoming_matches['league_name'], sport=sport)

        for upcoming_match in upcoming_matches['games']:
            match = Match(
                tournament=tournament,
                date=datetime.datetime.fromtimestamp(int(upcoming_match['timestamp'])).strftime('%Y-%m-%d %H:%M:%S'),
                player1=upcoming_match['home'],
                player2=upcoming_match['away'],
                win1=float(upcoming_match['odds'][0]),
                draw=float(upcoming_match['odds'][1]),
                win2=float(upcoming_match['odds'][2])
            )
            try:
                match.save()
            except peewee.IntegrityError:
                psql_db.rollback()
            except:
                psql_db.rollback()
