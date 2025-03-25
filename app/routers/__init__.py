from fastapi import FastAPI

from .example import router as example_router


def include_routers(app: FastAPI) -> None:
    """Include all routers in the app."""

    routers = [
        example_router,
    ]

    for router in routers:
        app.include_router(router)
