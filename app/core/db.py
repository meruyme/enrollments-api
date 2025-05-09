from pymongo import MongoClient
from mongomock import MongoClient as MongoClientMock
from app.core.constants import Environment
from app.core.settings import Settings
from pymongo.database import Database

settings = Settings()


class DatabaseProvider:
    @staticmethod
    def get_database() -> Database:
        if settings.environment == Environment.TEST:
            client = MongoClientMock()
        else:
            client = MongoClient(settings.mongo_host)
        return client[settings.database_name]
