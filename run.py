from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from cfgs import config as cfg
from tortoise import Tortoise
from tortoise.contrib.fastapi import RegisterTortoise, tortoise_exception_handlers
from app.routes.v1 import router as v1_router
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 使用RegisterTortoise和Aerich管理的迁移，而不是生成模式
    async with RegisterTortoise(
        app,
        config=cfg.TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    ):
        yield

    await Tortoise.close_connections()

app = FastAPI(
    title="Remi Union Service",
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)

app.include_router(v1_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "run:app",
        host=cfg.FastapiHost,
        port=cfg.FastapiPort,
        reload=True,
    )
