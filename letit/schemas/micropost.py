from enum import Enum, unique

@unique
class PostType(str, Enum):
    TEXT = "TEXT"
    MEDIA = "MEDIA"