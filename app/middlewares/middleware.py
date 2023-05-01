import re

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from starlette import status

from app.constants.constants import DetailExceptionConstants


async def handle_error(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except IntegrityError as e:
        detail = str(e.orig) if hasattr(e, "orig") else str(e)
        pattern = r"Key \(([a-z_]+)\)"
        match = re.search(pattern, detail)

        if match:
            msg = ""
            field = match.group(1)

            if "unique constraint" in detail:
                msg = DetailExceptionConstants.FIELD_ALREADY_EXISTS.replace(
                    "{Field}", field.capitalize()
                )

            elif "foreign key constraint" in detail:
                msg = DetailExceptionConstants.FIELD_NOT_EXISTS.replace(
                    "{Field}", field.capitalize()
                )

            return JSONResponse(
                status_code=422,
                content={
                    "detail": [
                        {
                            "loc": ["body", match.group(1)],
                            "msg": msg,
                            "type": "constraint_violation",
                        }
                    ],
                },
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=DetailExceptionConstants.INTERNAL_SERVER_ERROR,
        )
