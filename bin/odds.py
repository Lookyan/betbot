from pprint import pprint
import typing

import requests
from requests.structures import CaseInsensitiveDict

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Referer': 'http://www.overbetting.net/v2/odds/'
}


def make_request(page=1) -> (dict, CaseInsensitiveDict):
    """

    :param page: page of odds

    :return: odds, response headers
    """
    params = {
        'cache': '5sec',
        'expand': 'sport,category,tournament,teamHome,teamAway',
        'filter': '{"sport_id":null,"category_id":null,"tournament_id":null,"interval":168,"service":"own"}',
        'page': page
    }
    r = requests.get('https://overapi.pw/odds/own/odds/index', params=params, headers=headers)
    r.raise_for_status()
    result = r.json()
    return result, r.headers


def extract() -> typing.Generator[list, None, None]:
    """
    Extracts all upcoming events with odds

    :return: list of odds
    """

    current_page = 1
    while True:
        games = []
        result, response_headers = make_request(current_page)
        for game in result:
            current_game = {}
            current_game['category'] = game['category']['name_en']
            current_game['sport'] = game['sport']['name_en']
            current_game['team_away'] = game['teamAway']['name_en']
            current_game['team_home'] = game['teamHome']['name_en']
            current_game['tournament'] = game['tournament']['name_en']
            current_game['timestamp'] = game['timestamp']
            for odd in game['odds_maintime']:
                if odd['T'] == 1:
                    current_game['w1'] = odd['bid'][0]['C']
                elif odd['T'] == 2:
                    current_game['draw'] = odd['bid'][0]['C']
                elif odd['T'] == 3:
                    current_game['w2'] = odd['bid'][0]['C']
            games.append(current_game)
        yield games
        current_page += 1
        if 'X-Pagination-Page-Count' in response_headers:
            if current_page >= int(response_headers['X-Pagination-Page-Count']):
                break
        else:
            break

if __name__ == '__main__':
    game_extractor = extract()
    for games in game_extractor:
        pprint(games)
