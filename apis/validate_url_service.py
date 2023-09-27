from typing import List
from apis.validate_response import ValidationResponse, IsSiteSafe
from apis.db_type import DBType
from apis.base_db_api import BaseDBAPI

class URLValidator:
    def __init__(self, allDBs: List[BaseDBAPI]):
        self.allDBs = allDBs

    def validate_url(self, url: str) -> ValidationResponse:
        for db in self.allDBs:
            isInDb = db.is_in_db(url)
            if isInDb:
                return ValidationResponse(db.dbType, isInDb, self._is_site_safe(db.dbType, isInDb))
        return ValidationResponse("NotFound", False, IsSiteSafe(2))

    def _is_site_safe(self, dbType: DBType, isInDb: bool) -> IsSiteSafe:
        if dbType == DBType.WhiteList and isInDb:
            return IsSiteSafe.Yes
        if dbType == DBType.BlackList and isInDb:
            return IsSiteSafe.No
        return IsSiteSafe.Unknown