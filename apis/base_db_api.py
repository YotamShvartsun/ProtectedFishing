import abc
from db_type import DBType

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, type: DBType):
        self.type = type

    @abc.abstractmethod
    def is_in_db(self, domain: str) -> bool:
        raise NotImplementedError()
