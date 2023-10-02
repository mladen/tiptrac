from enum import Enum


# ENUMERATIONS
# Enumerations for the role field (admin, manager, user)
class Role(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


# Enumerations for the status field (todo, in_progress, done)
class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
