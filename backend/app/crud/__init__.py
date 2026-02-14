from app.crud.base import CRUDBase
from app.crud.user import CRUDUser
from app.crud.student import CRUDStudent
from app.crud.course import CRUDCourse
from app.crud.contract import CRUDContract
from app.crud.payment import CRUDPayment

__all__ = [
    "CRUDBase",
    "CRUDUser",
    "CRUDStudent",
    "CRUDCourse",
    "CRUDContract",
    "CRUDPayment",
]
