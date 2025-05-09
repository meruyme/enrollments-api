from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"


class EnrollmentStatus(int, Enum):
    IN_QUEUE = 1
    ACCEPTED = 2
    REFUSED = 3
