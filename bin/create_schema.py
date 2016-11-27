import inspect
import sys

import peewee

from lib.db import models
from lib.db.models import Sport
from lib.db.models import Tournament
from lib.db.models import Match
from lib.db.models import User
from lib.db.models import Bet


if __name__ == '__main__':
    # extracted_models = [
    #     model for name, model in inspect.getmembers(
    #         sys.modules['lib.db.models']
    #     )
    #     if type(model) == peewee.BaseModel and name != 'BaseModel' and issubclass(model, models.BaseModel)
    #     ]
    # for model in extracted_models:
    #     model.create_table(True)

    Sport.create_table(True)
    Tournament.create_table(True)
    Match.create_table(True)
    User.create_table(True)
    Bet.create_table(True)
