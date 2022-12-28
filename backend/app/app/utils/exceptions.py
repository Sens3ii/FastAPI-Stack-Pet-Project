from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse


def install_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request, exc: RequestValidationError
    ):
        data = dict()
        message = "Something went wrong"
        errors = dict()
        for pydantic_error in exc.errors():
            loc, msg = pydantic_error["loc"], pydantic_error["msg"]
            filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
            filtered_loc = [item for item in filtered_loc if isinstance(item, str)]
            field_string = ".".join(filtered_loc)  # nested fields with dot-notation
            errors[field_string] = msg
        data["message"] = message
        data["errors"] = errors
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(data),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )
