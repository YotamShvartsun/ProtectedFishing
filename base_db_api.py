class BaseDBAPI:
    def __init__(self):
        self._latest_list = None
    
    def is_site_safe(self, domain: str) -> bool:
        raise NotImplementedError() 