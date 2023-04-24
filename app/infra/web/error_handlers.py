import fastapi
from starlette.responses import RedirectResponse

from .security import LOGIN_PATH, NotAuthenticatedError


def not_authenticated_exception_handler(
    request: fastapi.Request,
    exc: NotAuthenticatedError,
) -> RedirectResponse:
    return RedirectResponse(url=LOGIN_PATH)


def register_error_handlers(app: fastapi.FastAPI) -> None:
    app.add_exception_handler(NotAuthenticatedError, not_authenticated_exception_handler)
