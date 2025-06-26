from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from database import db_helper
from settings.config import settings

from football import router as football_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)


main_app.include_router(football_router)

if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True)
