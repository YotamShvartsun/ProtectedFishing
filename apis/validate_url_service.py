import asyncio
from typing import List
import logging
from urllib import parse as url_parser

from apis.base_db_api import BaseDBAPI


class URLValidator:
    def __init__(self, allDBs: List[BaseDBAPI]):
        self.allDBs = allDBs

    def extract_domain(self, url: str) -> str:
        """
        This function extracts the domain from a given URL
        """
        if not url.startswith('http'):
            url = 'http://' + url
        return url_parser.urlparse(url).netloc
        
    async def validate_url(self, url: str) -> bool:
        domain = self.extract_domain(url)
        results = await asyncio.gather(*[db.is_site_safe(domain) for db in self.allDBs])
        return False not in results
