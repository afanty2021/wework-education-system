from app.schemas.user import UserCreate, UserUpdate, UserResponse, TokenResponse
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentResponse
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse
from app.schemas.homework import HomeworkCreate, HomeworkUpdate, HomeworkResponse

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "TokenResponse",
    "StudentCreate", "StudentUpdate", "StudentResponse",
    "CourseCreate", "CourseUpdate", "CourseResponse",
    "ScheduleCreate", "ScheduleUpdate", "ScheduleResponse",
    "ContractCreate", "ContractUpdate", "ContractResponse",
    "PaymentCreate", "PaymentUpdate", "PaymentResponse",
    "AttendanceCreate", "AttendanceUpdate", "AttendanceResponse",
    "HomeworkCreate", "HomeworkUpdate", "HomeworkResponse",
]
