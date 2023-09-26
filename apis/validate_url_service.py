from typing import List

from apis.base_db_api import BaseDBAPI


allDBs: List[BaseDBAPI]

def validate_url(url: str) -> bool:
    for db in allDBs:
        if (not db.is_site_safe(url)):
            return False
    return True
