import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from api.file_manager.minio_helper import minio_helper
from api.main_router import router as main_router
from core.config import settings
from core.elastic import es_helper
from core.kafka import consume


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume())
    minio_helper.ensure_bucket_exists()

    await es_helper.init_images_index()

    yield

    await es_helper.es_client.close()
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    docs_url=None if settings.run.disable_docs else "/docs",
    redoc_url=None if settings.run.disable_docs else "/redoc",
    openapi_url=None if settings.run.disable_docs else "/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.run.host, port=settings.run.port, reload=True)
