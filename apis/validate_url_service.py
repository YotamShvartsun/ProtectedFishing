import asyncio
from typing import List
from apis.validate_response import ValidationResponse, IsSiteSafe
from apis.db_type import DBType
from apis.base_db_api import BaseDBAPI

class URLValidator:
    def __init__(self, allDBs: List[BaseDBAPI]):
        self.white_dbs = [db for db in allDBs if db.dbType == DBType.WhiteList]
        self.black_dbs = [db for db in allDBs if db.dbType == DBType.BlackList]

    async def validate_url(self, url: str) -> ValidationResponse:        
        white_dbs_results = await asyncio.gather(*[db.is_in_db(url) for db in self.white_dbs])
        if any(white_dbs_results):
            return ValidationResponse(DBType.WhiteList, True, IsSiteSafe.Yes)
        
        black_dbs_results = await asyncio.gather(*[db.is_in_db(url) for db in self.black_dbs])
        if any(black_dbs_results):
            return ValidationResponse(DBType.BlackList, True, IsSiteSafe.No)
        return ValidationResponse(None, False, IsSiteSafe.Unknown)

