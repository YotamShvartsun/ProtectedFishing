from typing import List
from tranco import Tranco

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
        if self._tranco_db is None:
            self._tranco_db = Tranco(cache=True, cache_dir=self._TRANCO_BASE_CACHE_DIR)
        self._latest_list = self._tranco_db.list()
        new_top_sites_list = self._latest_list.top()
        self._top_sitest_list = new_top_sites_list
