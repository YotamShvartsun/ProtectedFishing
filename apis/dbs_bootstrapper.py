from typing import Dict, List
from apis.base_db_api import BaseDBAPI
from apis.iplocation import IPLocationDBAPI
from apis.tranco_api import TrancoApi

class DBFactory:
    def __init__(self):
        self.dbNameToObject: Dict[str, BaseDBAPI]  = {}
    
    def add_db(self, dbName: str, baseDbApi: BaseDBAPI):
        self.dbNameToObject[dbName] = baseDbApi

    def get_dbs(self) -> List[BaseDBAPI]:
        return self.dbNameToObject



def initialize_dbs() -> DBFactory:
    dbFactory = DBFactory()
    dbFactory.add_db("Tranco", TrancoApi())
    dbFactory.add_db("Geolocation", IPLocationDBAPI())
    return dbFactory