from fastapi import Request

from serve.exceptions import BaseAPIException


async def request_handler(request: Request, call_next):
    """
    TODO: add logging and individual request traceability
    """
    try:
        return await call_next(request)
    except Exception as ex:
        if isinstance(ex, BaseAPIException):
            return ex.response()
        # Re-raising other exceptions will return internal error 500 to the client
        raise ex
    