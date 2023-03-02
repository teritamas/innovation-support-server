import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.extension_router import extension_router
from .routers.proposal_router import proposal_router
from .routers.proposal_vote_router import proposal_vote_router
from .routers.timeline_router import timeline_router
from .routers.uer_router import user_router


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
    app.include_router(user_router)
    app.include_router(proposal_router)
    app.include_router(proposal_vote_router)
    app.include_router(timeline_router)
    app.include_router(extension_router)

    return app


app: FastAPI = get_application()


if __name__ == "__main__":
    uvicorn.run(
        "__main__:app",
    )
