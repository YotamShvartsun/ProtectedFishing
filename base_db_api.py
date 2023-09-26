import abc

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    def is_site_safe(self, domain: str) -> bool:
        raise NotImplement