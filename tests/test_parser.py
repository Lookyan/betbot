# import unittest
#
# from bin.parser import (
#     transform_to_dict,
#     parse_odds,
#     parse
# )
#
#
# class ParserTest(unittest.TestCase):
#
#     def test_transform_to_dict(self):
#         cells = ['AA÷dKLrKm2e', 'AD÷1478358000', 'AB÷1', 'CR÷1', 'AC÷1', 'CX÷Bournemouth', 'ER÷Round 11', 'AX÷0',
#                  'BX÷-1', 'WM÷BOU', 'AE÷Bournemouth', 'WU÷bournemouth', 'WN÷SUN', 'AF÷Sunderland', 'WV÷sunderland',
#                  'AW÷1', 'AN÷y', 'MW÷16', '']
#         res = transform_to_dict(cells)
#         expected_res = {'AX': '0', 'AC': '1', 'CX': 'Bournemouth', 'AB': '1', 'WN': 'SUN', 'AN': 'y',
#                         'AE': 'Bournemouth', 'MW': '16', 'CR': '1', 'BX': '-1', 'AD': '1478358000', 'AF': 'Sunderland',
#                         'AW': '1', 'WM': 'BOU', 'AA': 'dKLrKm2e', 'ER': 'Round 11', 'WU': 'bournemouth',
#                         'WV': 'sunderland'}
#
#         self.assertEqual(expected_res, res)
#
#     def test_parse_odds(self):
#         content = 'MI÷1.60|3.60|6.00¬MJ÷1.67|3.50|5.50¬MK÷1|1|1¬ML÷down|up|up¬MM÷o_1|o_0|o_2¬'
#         res = parse_odds(content)
#         expected_res = ('1.60', '3.60', '6.00')
#
#         self.assertEqual(expected_res, res)
#
#     def test_parse(self):
#         content = 'SA÷1¬~ZA÷ENGLAND: Premier League¬ZEE÷dYlOSQOD¬ZB÷198¬ZY÷England¬ZC÷fZHsKRg9¬ZD÷t¬ZE÷8Ai8InSt¬ZF÷0' \
#                   '¬ZO÷0¬ZG÷1¬ZH÷198_dYlOSQOD¬ZJ÷2¬ZL÷/england/premier-league/¬ZX÷00England     007ngland000000000014' \
#                   '7000Premier Leag014League000¬ZCC÷0¬~AA÷dKLrKm2e¬AD÷1478358000¬AB÷1¬CR÷1¬AC÷1¬CX÷Bournemouth¬ER÷Ro' \
#                   'und 11¬AX÷0¬BX÷-1¬WM÷BOU¬AE÷Bournemouth¬WU÷bournemouth¬WN÷SUN¬AF÷Sunderland¬WV÷sunderland¬AW÷1¬A' \
#                   'N÷y¬MW÷16¬~AA÷4pPjIRW7¬AD÷1478358000¬AB÷1¬CR÷1¬AC÷1¬CX÷Burnley¬ER÷Round 11¬AX÷0¬BX÷-1¬WM÷BUR¬AE÷' \
#                   'Burnley¬WU÷burnley¬WN÷CRY¬AF÷Crystal Palace¬WV÷crystal-palace¬AW÷1¬AN÷y¬MW÷16¬'
#
#         res = parse(content)
#         expected_res = {
#             'games': [{'timestamp': '1478358000', 'home': 'Bournemouth', 'away': 'Sunderland', 'event_id': 'dKLrKm2e'},
#                       {'timestamp': '1478358000', 'home': 'Burnley', 'away': 'Crystal Palace', 'event_id': '4pPjIRW7'}],
#             'sport_id': '1', 'league_name': 'ENGLAND: Premier League'}
#
#         self.assertEqual(expected_res, res)
