# 基础 CRUD 类
# from app.crud.base import CRUDBase  # TODO: 实现 CRUDBase
# from app.crud.user import CRUDUser
# from app.crud.course import CRUDCourse
from app.crud.contract import ContractCRUD
from app.crud.schedule import ScheduleCRUD
from app.crud.payment import PaymentCRUD
from app.crud.attendance import AttendanceCRUD
from app.crud.notification import NotificationCRUD

# 已实现的 CRUD 类
from app.crud.student import CRUDStudent

__all__ = [
    # "CRUDBase",
    # "CRUDUser",
    "CRUDStudent",
    # "CRUDCourse",
    "ContractCRUD",
    "ScheduleCRUD",
    "PaymentCRUD",
    "AttendanceCRUD",
    "NotificationCRUD",
]
