import abc
from functools import wraps
from typing import Callable
from urllib import parse as url_parser
from apis.db_type import DBType

def extract_domain(url: str) -> str:
    """
    This function extracts the domain from a given URL
    """
    if not url.startswith('http'):
        url = 'http://' + url
    return url_parser.urlparse(url).netloc

def extract_domain_from_url(func: Callable):
    @wraps(func)
    async def wrapper(self, url: str, *args, **kwargs):
        domain = extract_domain(url)
        return await func(self, domain, *args, **kwargs)
    return wrapper

class BaseDBAPI(abc.ABC):
    def __init__(self, dbType: DBType):
        self.dbType = dbType

    @abc.abstractmethod
    async def is_in_db(self, domain: str) -> bool:
        raise NotImplementedError() 
