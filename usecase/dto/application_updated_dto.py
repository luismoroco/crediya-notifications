from dataclasses import dataclass
from decimal import Decimal

from helper import BaseModel


@dataclass
class ApplicationUpdatedDTO(BaseModel):

    applicationId: int
    amount: int
    deadline: int
    applicationStatus: str
    email: str
    interestRate: Decimal
