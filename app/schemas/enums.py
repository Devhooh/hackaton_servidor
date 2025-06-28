from enum import Enum

class UserTypeEnum(str, Enum):
    HEARING = "hearing"
    DEAF_MUTE = "deaf-mute"

class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
