from typehints import Dict
import base_db_api


class DBFactory:
    def __init__():
        self.dbNameToObject: Dict[str, BaseDbApi]  = {}
    
    def add_db(dbName: str, baseDbApi: BaseDbApi):
        self.dbNameToObject[dbName] = baseDbApi

    def get_db(dbName: str):
        self.dbNameToObject[dbName]



def initialize_dbs() -> DBFactory:
    dbFactory = DBFactory()
    """dbFactory.add_db("Tranco", TrancoApi)"""