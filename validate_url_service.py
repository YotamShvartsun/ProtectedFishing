from typing import List
import base_db_api

allDBs: List[base_db_api]

def validate_url(url: str) -> bool:
    for db in allDBs:
        if (not db.is_site_safe(url)):
            return False
    return True