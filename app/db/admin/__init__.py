from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from app import get_settings

from .example import ExampleAdmin


views = [
    ExampleAdmin,
]


class AdminAuth(AuthenticationBackend):
    def __init__(self) -> None:
        super().__init__(get_settings().USER_MANAGER_SECRET)
        self._admin_username = get_settings().ADMIN_USERNAME
        self._admin_password_hash = get_settings().ADMIN_PASSWORD_HASH

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = str(form.get("username"))
        password = str(form.get("password"))
        if (
            username == self._admin_username
            and hash(password) == self._admin_password_hash
        ):
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("authenticated", False))
