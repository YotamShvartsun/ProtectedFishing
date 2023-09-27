from dataclasses import dataclass
from enum import IntEnum

class IsSiteSafe(IntEnum):
    Yes = 0
    No = 1
    Unknown = 2

@dataclass
class ValidationResponse:
    status: str
    isInDb: bool
    isSafe: IsSiteSafe
    message: str = None