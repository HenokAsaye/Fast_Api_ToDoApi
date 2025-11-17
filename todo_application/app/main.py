from fastapi import FastAPI
from todo_application.app.core.config import get_settings
from todo_application.app.api.v1.routes.todo import router as todo_router


settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
)

app.include_router(todo_router, prefix=settings.API_V1_STR)