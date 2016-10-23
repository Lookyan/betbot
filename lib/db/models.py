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


class BaseModel(Model):
    class Meta:
        database = psql_db


class User(BaseModel):
    username = CharField()
    balance = FloatField()


class Bet(BaseModel):
    user = ForeignKeyField(User)
    match = ForeignKeyField(Match)
    sum_of_bet = FloatField()
    bet_coeff = FloatField()                        #coefficient related to the user selected team/player
    bet_type = IntegerField()                       #-1 if bet set on "Loose", 1 if set on "Win", 0 if set on "Dead Heat"
    bet_status = BooleanField(default=False)        #"False" for awaiting, "True" for done


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
