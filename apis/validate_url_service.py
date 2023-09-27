import asyncio
import cachetools

from typing import List
from apis.validate_response import ValidationResponse, IsSiteSafe
from apis.db_type import DBType
from apis.base_db_api import BaseDBAPI


class URLValidator:
    _CACHE_MAX_SIZE = 10 ** 4
    _CACHE_TIMEOUT_SECONDS = 60 * 60 * 60

    def __init__(self, allDBs: List[BaseDBAPI]):
        self.white_dbs = [db for db in allDBs if db.dbType == DBType.WhiteList]
        self.black_dbs = [db for db in allDBs if db.dbType == DBType.BlackList]
        self.url_cache = cachetools.TTLCache(maxsize=self._CACHE_MAX_SIZE, ttl=self._CACHE_TIMEOUT_SECONDS)

    def _update_cache_and_return(self, url: str, validation_response: ValidationResponse) -> ValidationResponse:
        self.url_cache[url] = validation_response
        return validation_response
    
    async def validate_url(self, url: str) -> ValidationResponse:
        if url in self.url_cache:
            return self.url_cache[url]

        white_dbs_results = await asyncio.gather(*[db.is_in_db(url) for db in self.white_dbs])
        if any(white_dbs_results):
            return self._update_cache_and_return(url, ValidationResponse(DBType.WhiteList, True, IsSiteSafe.Yes))
        
        black_dbs_results = await asyncio.gather(*[db.is_in_db(url) for db in self.black_dbs])
        if any(black_dbs_results):
            return self._update_cache_and_return(url, ValidationResponse(DBType.BlackList, True, IsSiteSafe.No))

        return self._update_cache_and_return(url, ValidationResponse(None, False, IsSiteSafe.Unknown))
