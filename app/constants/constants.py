class RouteTagConstants:
    AUTH_TAG: str = "Auth"
    TASK_TAG: str = "Task"
    USER_TAG: str = "User"
    COMPANY_TAG: str = "Company"


class AuthConstants:
    BEARER_TOKEN_TYPE: str = "bearer"
    INVALID_OR_EXPIRED_TOKEN: str = "Invalid or Expired token"
    INVALID_CREDENTIAL: str = "Invalid credential"


class DetailExceptionConstants:
    INTERNAL_SERVER_ERROR: str = "Internal server error"
    FIELD_ALREADY_EXISTS: str = "{Field} already exists"
    FIELD_NOT_EXISTS: str = "{Field} not exists"
    RECORD_NOT_FOUND: str = "{Record} not found"


class UserMsgConstants:
    USER_CHANGE_PASSWORD_SUCCESSFULLY: str = "User change password successfully"
    USER_CURRENT_PASSWORD_IS_INCORRECT: str = "Current password is incorrect"
    USER_NOT_HAVE_PERMISSION: str = "You do not have permission to access this resource"
