import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every

from app import cli, config

from .routers.account_router import account_router
from .routers.extension_router import extension_router
from .routers.prize_router import prize_router
from .routers.proposal_router import proposal_router
from .routers.proposal_vote_router import proposal_vote_router
from .routers.timeline_router import timeline_router
from .routers.user_router import user_router
from .routers.web3_router import web3_router


def get_application() -> FastAPI:
    app = FastAPI(
        title="DAO Innovation Support",
        description="Innovation Support APIです",
        prefix="/api/v1"
        # version=env_settings.version,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.middleware("http")(ControllerLoggingMiddleware())
    app.include_router(account_router)
    app.include_router(user_router)
    app.include_router(proposal_router)
    app.include_router(proposal_vote_router)
    app.include_router(timeline_router)
    app.include_router(prize_router)
    app.include_router(extension_router)
    app.include_router(web3_router)
    return app


app: FastAPI = get_application()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.on_event("startup")
@repeat_every(seconds=60 * config.batch_interval_minute)  # 5 min
async def remove_expired_tokens_task() -> None:
    await cli.main()


if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
    )
