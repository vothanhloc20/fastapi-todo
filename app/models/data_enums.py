from enum import Enum


class BaseDataEnum(Enum):
    @classmethod
    def as_array(cls):
        res = []
        for item in cls:
            res.append((item.name, item.value))

        return res

    @classmethod
    def names_as_array(cls):
        res = []
        for item in cls:
            res.append(item.name)

        return res


class CompanyMode(BaseDataEnum):
    Active = "Active"
    TemporarilyClosed = "Temporarily Closed"


class TaskStatus(BaseDataEnum):
    NotStarted = "Not Started"
    InProgress = "In Progress"
    OnHold = "On Hold"
    Review = "Review"
    Completed = "Completed"
    Closed = "Closed"


class TaskPriority(BaseDataEnum):
    HighPriority = "High Priority"
    MediumPriority = "Medium Priority"
    LowPriority = "Low Priority"
