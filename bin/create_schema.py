import inspect
import sys

import peewee

from lib.db import models

if __name__ == '__main__':
    extracted_models = [
        model for name, model in inspect.getmembers(
            sys.modules['lib.db.models']
        )
        if type(model) == peewee.BaseModel and name != 'BaseModel' and issubclass(model, models.BaseModel)
        ]
    peewee.create_model_tables(extracted_models)
