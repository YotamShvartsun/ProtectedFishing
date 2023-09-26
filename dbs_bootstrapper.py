from typing import Dict
from base_db_api import BaseDBAPI
from tranco_api import TrancoApi

class DBFactory:
    def __init__(self):
        self.dbNameToObject: Dict[str, BaseDBAPI]  = {}
    
    def add_db(self, dbName: str, baseDbApi: BaseDBAPI):
        self.dbNameToObject[dbName] = baseDbApi

    def get_db(self, dbName: str) -> BaseDBAPI:
        return self.dbNameToObject[dbName]



def initialize_dbs() -> DBFactory:
    dbFactory = DBFactory()
    dbFactory.add_db("Tranco", TrancoApi)
    return dbFactory