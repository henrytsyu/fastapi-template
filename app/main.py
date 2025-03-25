from fastapi import FastAPI

from app.db import create_admin
from app.routers import include_routers


def main() -> None:
    app = FastAPI()
    create_admin(app)
    include_routers(app)


if __name__ == "__main__":
    main()
