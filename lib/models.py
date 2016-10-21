from peewee import (
    PostgresqlDatabase,
    Model,
    PrimaryKeyField,
    ForeignKeyField,
    CharField,
    IntegerField,
    FloatField,
    BooleanField,
    DateTimeField
)


psql_db = PostgresqlDatabase('betbot', user = 'betbot_user', password = 'devpass', host = '127.0.0.1')

class BaseModel(Model):                            #database model
    class Meta :
        database = psql_db

class User(BaseModel):
    user_id = PrimaryKeyField()
    username = CharField()
    wallet_balance = IntegerField()

class Bet(BaseModel) :
    bet_id = ForeignKeyField(User)
    sum_of_bet = IntegerField()
    bet_coeff = FloatField()                        #coefficient related to the user selected team/player
    bet_type = IntegerField()                       #-1 if bet set on "Loose", 1 if set on "Win", 0 if set on "Dead Heat"
    bet_status = BooleanField(default = False)      #"False" for awaiting, "True" for done

class Sport_Type(BaseModel) :
    sport_id = PrimaryKeyField()
    sport = CharField()

class League(BaseModel) :
    league_id = ForeignKeyField(Sport_Type)
    league_name = CharField()

class Match(BaseModel) :
    match_id = ForeignKeyField(League)
    date = DateTimeField()
    opp_1 = CharField()
    opp_2 = CharField()
    coeff_1 = FloatField()                          #first opponent coefficient
    coeff_2 = FloatField()                          #second opponent coefficient
    coeff_d = FloatField()                          #dead heat coefficient
    match_status = BooleanField(default=False)      #"False" for awaiting, "True" for done


#i don't know if we need it :)
"""class Transaction(BaseModel) :
    transact_sum = IntegerField() """
