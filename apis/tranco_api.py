import logging
from typing import List
from tranco import Tranco
from tranco.tranco import TrancoList
from apis.base_db_api import BaseDBAPI
from apis.db_type import DBType

class TrancoDbNotInitilizedError(Exception):
    pass

# The tranco.rank function returns -1 when the domain is not in the list
TRANCO_NOT_FOUND = -1

_LOGGER = logging.getLogger('app.apis.iplocation')

class TrancoApi(BaseDBAPI):
    _TRANCO_BASE_CACHE_DIR = '.tranco'

    def __init__(self, dbType: DBType):
        super().__init__(dbType)
        self._tranco_db: Tranco = None
        self._latest_list: TrancoList = None
        self._top_sitest_list: List[str] = None
        self._tranco_cache_dir: str = None
        self.set_db()

    def is_known_domain(self, domain: str) -> bool:
        if self._latest_list is not None:
            return domain in self._latest_list
        raise TrancoDbNotInitilizedError('DB is not initialized')

    def get_tranco_db(self) -> Tranco:
        if self._tranco_db is not None:
            return self._tranco_db
        raise TrancoDbNotInitilizedError('DB is not initialized')

    def get_top_sites_list(self) -> List[str]:
        if self._top_sitest_list is not None:
            return self._top_sitest_list
        raise TrancoDbNotInitilizedError('DB is not initialized')
    
    async def is_in_db(self, domain: str) -> bool:
        if self._latest_list is None:
            _LOGGER.debug('no cached list, setting db...')
            self.set_db()
            _LOGGER.info('Done setting the db')
        return self._latest_list.rank(domain) != -1

    def set_db(self) -> None:
        _LOGGER.info('Initializing the TrancoDB service...')
        if self._tranco_db is None:
            self._tranco_db = Tranco(cache=False, cache_dir=self._TRANCO_BASE_CACHE_DIR)
        self._latest_list = self._tranco_db.list()
        self._top_sitest_list = self._latest_list.top()
        _LOGGER.info('Done loading the TrancoDB')
