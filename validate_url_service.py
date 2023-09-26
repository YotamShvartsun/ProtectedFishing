from typing import List

from base_db_api import BaseDBAPI

class URLValidator:
    def __init__(self, allDBs: List[BaseDBAPI]):
        self.allDBs = allDBs

    def validate_url(self, url: str) -> bool:
        for db in self.allDBs:
            if (not db.is_site_safe(url)):
                return False
        return True
