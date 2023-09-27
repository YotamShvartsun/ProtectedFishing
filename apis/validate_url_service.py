import asyncio
from typing import List

from apis.base_db_api import BaseDBAPI

class URLValidator:
    def __init__(self, allDBs: List[BaseDBAPI]):
        self.allDBs = allDBs

    async def validate_url(self, url: str) -> bool:
        results = await asyncio.gather(*[db.is_site_safe(url) for db in self.allDBs])
        return False not in results
