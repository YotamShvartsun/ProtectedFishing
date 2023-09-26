SITE_NOT_FOUND = -1 

class base_db_api:
    def __init__(self):
        self._latest_list = None
    
    def is_site_safe(self, domain: str) -> bool:
        return SITE_NOT_FOUND != self._latest_list.rank(domain)