from apis.base_db_api import BaseDBAPI
from apis.db_type import DBType
import csv

class IsraelisApi(BaseDBAPI):
    def __init__(self, dbType: DBType):
        super().__init__(dbType)

    async def is_in_db(self, domain: str) -> bool:
        file = open("apis/israeli_sits.csv", "r")
        data = file.read().split('\n')
        file.close()
        return domain in data