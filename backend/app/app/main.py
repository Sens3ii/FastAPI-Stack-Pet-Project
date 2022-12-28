from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.schemas.base import ErrorResponse
from app.utils.exceptions import install_handlers

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
    responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse}},

)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
install_handlers(app)

app.include_router(api_router, prefix=settings.API_V1_STR)
