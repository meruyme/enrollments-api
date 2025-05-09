from enum import Enum


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"


class EnrollmentStatus(str, Enum):
    IN_QUEUE = "in_queue"
    ACCEPTED = "accepted"
    REFUSED = "refused"
