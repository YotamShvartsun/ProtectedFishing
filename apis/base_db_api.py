import abc

class BaseDBAPI(abc.ABC):
    @abc.abstractmethod
    async def is_site_safe(self, domain: str) -> bool:
        raise NotImplementedError() 
