import unittest
from unittest.mock import patch

from bin.odds import extract
from bin import odds


class OddsTest(unittest.TestCase):

    def test_extract(self):
        category = 'Spain'
        sport = 'soccer'
        team_away = 'FC Barcelona'
        team_home = 'Real Madrid CF'
        tournament = 'La liga'
        timestamp = '2016-05-03 20:00:00'
        odd_home_win = 3.7
        odd_draw = 5.2
        odd_away_win = 1.4
        response = (
            [
                {
                    'category': {
                        'name_en': category
                    },
                    'sport': {
                        'name_en': sport
                    },
                    'teamAway': {
                        'name_en': team_away
                    },
                    'teamHome': {
                        'name_en': team_home
                    },
                    'tournament': {
                        'name_en': tournament
                    },
                    'timestamp': timestamp,
                    'odds_maintime': [
                        {
                            'T': 1,
                            'bid': [{'C': odd_home_win}]
                        },
                        {
                            'T': 2,
                            'bid': [{'C': odd_draw}]
                        },
                        {
                            'T': 3,
                            'bid': [{'C': odd_away_win}]
                        },
                    ]
                }
            ],
            {}
        )
        with patch.object(odds, 'make_request', return_value=response) as make_request_mock:
            extracted_games = extract()
            games = next(extracted_games)

            expected_result = [
                {
                    'category': category,
                    'draw': odd_draw,
                    'sport': sport,
                    'team_away': team_away,
                    'team_home': team_home,
                    'timestamp': timestamp,
                    'tournament': tournament,
                    'w1': odd_home_win,
                    'w2': odd_away_win
                 }
            ]

            expected_page = 1

            self.assertTrue(make_request_mock.called)
            make_request_mock.assert_called_with(expected_page)
            self.assertEqual(expected_result, games)
