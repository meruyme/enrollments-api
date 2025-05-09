from pymongo.synchronous.database import Database

from app.core.db import DatabaseProvider


def get_database() -> Database:
    return DatabaseProvider.get_database()
