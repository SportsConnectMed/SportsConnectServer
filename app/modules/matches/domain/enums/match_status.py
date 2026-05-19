from enum import Enum


class MatchStatus(str, Enum):
    OPEN = "OPEN"
    FULL = "FULL"
    FINISHED = "FINISHED"
    CANCELLED = "CANCELLED"
