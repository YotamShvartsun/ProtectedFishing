import abc
from db_type import DBType
from validate_response import ValidationResponse

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    def __init__(self, type: DBType):
        self.type = type

    @abc.abstractmethod
    def is_site_safe(self, domain: str) -> ValidationResponse:
        raise NotImplementedError()
