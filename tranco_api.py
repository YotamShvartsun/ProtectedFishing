from typing import List
from tranco import Tranco

import datetime


class TrancoDbNotInitilizedError(Exception):
    pass


class TrancoApi:
    _TRANCO_BASE_CACHE_DIR = '.tranco'

    def __init__(self):
        self._tranco_db: Tranco = None
        self._latest_list = None
        self._top_sitest_list: List[str] = None
        self._tranco_cache_dir: str = None

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

    def set_db(self) -> None:
        new_tranco_cache_dir = self._TRANCO_BASE_CACHE_DIR + \
            str(datetime.datetime.now())
        new_tranco_db = Tranco(cache=True, cache_dir=new_tranco_cache_dir)
        new_latest_list = new_tranco_db.list()
        new_top_sites_list = new_latest_list.top()
        self._tranco_cache_dir = new_tranco_cache_dir
        self._tranco_db = new_tranco_db
        self._latest_list = new_latest_list
        self._top_sitest_list = new_top_sites_list
