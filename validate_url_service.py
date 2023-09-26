from typing import List
import base_db_api
import url_status_code

allDBs: List[base_db_api]

def initialize_db():
    """
    initialize all dbs
    (maybe with bootstrapper)
    """

def validate_url(url: str) -> bool:
    for db in allDBs:
        if (!db.is_site_safe(url)):
            """give resone why not safe"""
            return False
    return True