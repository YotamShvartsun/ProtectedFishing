from typing import List
from tranco import Tranco
from tranco.tranco import TrancoList

class TrancoDbNotInitilizedError(Exception):
    pass


# The tranco.rank function returns -1 when the domain is not in the list
TRANCO_NOT_FOUND = -1


class TrancoApi:
    _TRANCO_BASE_CACHE_DIR = '.tranco'

    def __init__(self):
        self._tranco_db: Tranco = None
        self._latest_list: TrancoList = None
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
    
    def is_site_safe(self, domain: str) -> bool:
        if self._latest_list is None:
            self.set_db()
        return TRANCO_NOT_FOUND != self._latest_list.rank(domain)

    def set_db(self) -> None:
        if self._tranco_db is None:
            self._tranco_db = Tranco(cache=True, cache_dir=self._TRANCO_BASE_CACHE_DIR)
        self._latest_list = self._tranco_db.list()
        self._top_sitest_list = self._latest_list.top()
