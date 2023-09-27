from apis.base_db_api import BaseDBAPI
from apis.db_type import DBType
from typing import List

class IsraelisApi(BaseDBAPI):
    def __init__(self, dbType: DBType):
        super().__init__(dbType)
        self._sits_list: List[str] = self._set_sits_list()

    async def is_in_db(self, domain: str) -> bool:
        return domain in self._sits_list
    
    def _set_sits_list(self) -> List[str]:
        file = open("apis/israeli_sits.csv", "r")
        data = file.read().split('\n')
        file.close()
        return data