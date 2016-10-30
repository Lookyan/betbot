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


DEFAULT_BALANCE = 1000


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

    class Meta:
        indexes = (
            (('player1', 'player2', 'tournament', 'date'), True),
        )


class User(BaseModel):
    username = CharField()
    balance = FloatField(default=DEFAULT_BALANCE)
    chosen_sport = ForeignKeyField(Sport, null=True)
    chosen_tournament = ForeignKeyField(Tournament, null=True)
    chosen_match = ForeignKeyField(Match, null=True)
    chosen_amount = FloatField(null=True)

    @staticmethod
    def get_user_by_chat_id(chat_id):
        return User.get_or_create(username=chat_id)


class Bet(BaseModel):
    user = ForeignKeyField(User)
    match = ForeignKeyField(Match)
    sum_of_bet = FloatField()
    bet_coeff = FloatField()                      # coefficient related to the user selected team/player
    bet_type = IntegerField()                     # -1 if bet set on "Loose", 1 if set on "Win", 0 if set on "Dead Heat"
    bet_status = BooleanField(default=False)      # "False" for awaiting, "True" for done
