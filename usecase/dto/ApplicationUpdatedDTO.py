from dataclasses import dataclass

@dataclass
class ApplicationUpdatedDTO:
    applicationId: int
    amount: int
    deadline: int
    applicationStatus: str
    email: str
