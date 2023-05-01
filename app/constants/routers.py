UUID_PATH_PARAM: str = "{uuid}"

ROUTE_AUTH: str = "/auth"
ROUTE_TASK: str = "/task"
ROUTE_USER: str = "/user"
ROUTE_COMPANY: str = "/company"

ROUTE_GET_BY_ID: str = f"/{UUID_PATH_PARAM}"
ROUTE_CREATE: str = "/create"
ROUTE_UPDATE_BY_ID: str = f"/update/{UUID_PATH_PARAM}"
ROUTE_DELETE_BY_ID: str = f"/delete/{UUID_PATH_PARAM}"
ROUTE_CHANGE_PASSWORD_BY_USER_ID: str = f"/change-password/{UUID_PATH_PARAM}"

ROUTE_TOKEN: str = "/token"
ROUTE_TOKEN_URL: str = f"{ROUTE_AUTH}{ROUTE_TOKEN}"
