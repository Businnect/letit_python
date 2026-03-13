from enum import Enum, unique
from pydantic import BaseModel

@unique
class JobLocation(str, Enum):
    REMOTE = "REMOTE"
    ONSITE = "ONSITE"
    HYBRID = "HYBRID"


@unique
class JobType(str, Enum):
    FULLTIME = "FULLTIME"
    PARTTIME = "PARTTIME"
    CONTRACT = "CONTRACT"
    FREELANCE = "FREELANCE"
    INTERNSHIP = "INTERNSHIP"


@unique
class JobCategory(str, Enum):
    PROGRAMMING = "PROGRAMMING"
    BLOCKCHAIN = "BLOCKCHAIN"
    DESIGN = "DESIGN"
    MARKETING = "MARKETING"
    CUSTOMERSUPPORT = "CUSTOMERSUPPORT"
    WRITING = "WRITING"
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    HUMANRESOURCE = "HUMANRESOURCE"
    ELSE = "ELSE"


@unique
class JobExperienceLevel(str, Enum):
    ALL = "ALL"
    JUNIOR = "JUNIOR"
    MID = "MID"
    SENIOR = "SENIOR"
    NOEXPERIENCEREQUIRED = "NOEXPERIENCEREQUIRED"


@unique
class JobStatus(str, Enum):
    DRAFT = "DRAFT"
    PAID = "PAID"
    CONFIRMED = "CONFIRMED"
    HOLD = "HOLD"
    REVIEW = "REVIEW"
    CLOSED = "CLOSED"

class UserJobCreatedByUserResponse(BaseModel):
    slug: str