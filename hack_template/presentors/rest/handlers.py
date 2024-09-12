from http import HTTPStatus

from litestar import Request, Response

from hack_template.application.common.exceptions import (
    DuplicateUsernameError,
    EntityNotFoundError,
)


def entity_not_found_handler(_: Request, exc: EntityNotFoundError) -> Response:
    return Response(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "status_code": HTTPStatus.NOT_FOUND,
            "message": exc.message,
        },
    )


def entity_conflict_handler(_: Request, exc: DuplicateUsernameError) -> Response:
    return Response(
        status_code=HTTPStatus.CONFLICT,
        content={
            "status_code": HTTPStatus.CONFLICT,
            "message": exc.message,
        },
    )
