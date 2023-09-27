import abc

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    def is_in_db(self, domain: str) -> bool:
        raise NotImplementedError() 
