from typing import List
import logging
from urllib import parse as url_parser

from apis.base_db_api import BaseDBAPI

_logger = logging.getLogger('app.apis.validate-service')

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

    def validate_url(self, url: str) -> bool:
        domain = self.extract_domain(url)
        _logger.error(f'{url}, and {domain}')
        for db in self.allDBs:
            if (not db.is_site_safe(domain)):
                return False
        return True
