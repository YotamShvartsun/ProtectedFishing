import abc
from db_type import DBType

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, dbType: DBType):
        self.dbType = dbType

    @abc.abstractmethod
    def is_in_db(self, domain: str) -> bool:
        raise NotImplementedError()
