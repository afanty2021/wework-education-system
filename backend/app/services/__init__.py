"""Business Logic Services

业务逻辑服务层模块
"""
from app.services.auth_service import AuthBusinessService
from app.services.course_service import CourseService
from app.services.student_service import StudentService
from app.services.contract_service import ContractService
from app.services.schedule_service import (
    ScheduleService,
    ScheduleNotFoundError,
    CourseNotFoundError as ScheduleCourseNotFoundError,
    TeacherNotFoundError,
    ClassroomNotFoundError,
    StudentNotFoundError as ScheduleStudentNotFoundError,
    ScheduleConflictError,
    InvalidScheduleDataError,
    ScheduleCapacityError,
    InvalidScheduleStatusError,
    ScheduleServiceError,
)
from app.services.schedule_service import ScheduleService
from app.services.payment_service import (
    PaymentService,
    PaymentServiceError,
    PaymentNotFoundError,
    PaymentNoExistsError,
    ContractNotFoundError as PaymentContractNotFoundError,
    InvalidPaymentDataError,
    InvalidPaymentStatusError,
)
from app.services.attendance_service import (
    AttendanceService,
    AttendanceServiceError,
    AttendanceNotFoundError,
    ScheduleNotFoundError as AttendanceScheduleNotFoundError,
    StudentNotFoundError as AttendanceStudentNotFoundError,
    DuplicateAttendanceError,
    InvalidAttendanceDataError,
    InvalidAttendanceStatusError,
)

__all__ = [
    "AuthBusinessService",
    "CourseService",
    "StudentService",
    "ContractService",
    "ScheduleService",
    "ScheduleNotFoundError",
    "ScheduleCourseNotFoundError",
    "TeacherNotFoundError",
    "ClassroomNotFoundError",
    "ScheduleStudentNotFoundError",
    "ScheduleConflictError",
    "InvalidScheduleDataError",
    "ScheduleCapacityError",
    "InvalidScheduleStatusError",
    "ScheduleServiceError",
    "ScheduleService",
    "PaymentService",
    "PaymentServiceError",
    "PaymentNotFoundError",
    "PaymentNoExistsError",
    "PaymentContractNotFoundError",
    "InvalidPaymentDataError",
    "InvalidPaymentStatusError",
    "AttendanceService",
    "AttendanceServiceError",
    "AttendanceNotFoundError",
    "AttendanceScheduleNotFoundError",
    "AttendanceStudentNotFoundError",
    "DuplicateAttendanceError",
    "InvalidAttendanceDataError",
    "InvalidAttendanceStatusError",
]
