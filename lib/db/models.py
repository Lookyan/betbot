from datetime import datetime

from peewee import (
    Model,
    ForeignKeyField,
    CharField,
    IntegerField,
    FloatField,
    BooleanField,
    DateTimeField
)

from .connection import psql_db
from .connection import database_manager


DEFAULT_BALANCE = 1000

WIN1 = 1
DRAW = 2
WIN2 = 3

GAME_TYPES = (
    (WIN1, 'Win 1'),
    (DRAW, 'Draw'),
    (WIN2, 'Win 2'),
)


class BaseModel(Model):
    class Meta:
        database = psql_db


class Sport(BaseModel):
    name = CharField()


class Tournament(BaseModel):
    sport = ForeignKeyField(Sport)
    name = CharField()


class Match(BaseModel):
    tournament = ForeignKeyField(Tournament)
    date = DateTimeField()
    player1 = CharField()
    player2 = CharField()
    win1 = FloatField()
    win2 = FloatField()
    draw = FloatField()
    match_status = BooleanField(default=False)  # "False" for awaiting, "True" for done

    def get_coeff_by_chosen_result(self, result):
        if result == WIN1:
            return self.win1
        elif result == WIN2:
            return self.win2
        else:
            return self.draw

    def check_actual(self) -> bool:
        """
        :return: True if match hasn't been started, False otherwise
        """
        if self.date > datetime.utcnow():
            return True
        else:
            return False

    @staticmethod
    def get_text_result(result):
        if result == WIN1:
            return 'WIN1'
        elif result == WIN2:
            return 'WIN2'
        else:
            return 'DRAW'

    class Meta:
        indexes = (
            (('player1', 'player2', 'tournament', 'date'), True),
        )


class User(BaseModel):

    username = CharField(unique=True)
    balance = FloatField(default=DEFAULT_BALANCE)
    chosen_sport = ForeignKeyField(Sport, null=True)
    chosen_tournament = ForeignKeyField(Tournament, null=True)
    chosen_match = ForeignKeyField(Match, null=True)
    chosen_result = IntegerField(choices=GAME_TYPES, null=True)
    chosen_amount = FloatField(null=True)

    @staticmethod
    async def get_user_by_chat_id(chat_id):
        return await database_manager.create_or_get(
            User,
            username=chat_id
        )

    async def save_chosen_result(self, choice):
        if choice == 'win1':
            self.chosen_result = WIN1
        elif choice == 'draw':
            self.chosen_result = DRAW
        elif choice == 'win2':
            self.chosen_result = WIN2
        else:
            return False

        await database_manager.update(self)
        return True


class Bet(BaseModel):
    user = ForeignKeyField(User)
    match = ForeignKeyField(Match)
    amount = FloatField()
    bet_coeff = FloatField()                      # coefficient related to the user selected team/player
    bet_type = IntegerField(choices=GAME_TYPES)
    bet_status = BooleanField(default=False)      # "False" for awaiting, "True" for done
