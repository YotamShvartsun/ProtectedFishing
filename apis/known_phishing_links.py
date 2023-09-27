from apis.base_db_api import BaseDBAPI
from apis.db_type import DBType

class KnownURLSAPI(BaseDBAPI):
    def __init__(self, dbType: DBType):
        super().__init__(dbType)
        self._db_loaded = False 
        self.load_db()

    async def is_in_db(self, domain: str) -> bool:
        if not self._db_loaded:
            self.load_db()
        return domain in self._loaded_urls
    
    def load_db(self) -> None:
        with open('apis/known_phishing_urls.txt', 'r', encoding='utf-8') as file:
            self._loaded_urls = file.readlines()
        self._db_loaded = True