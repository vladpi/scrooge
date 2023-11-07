from passlib.context import CryptContext


class PasswordsService:
    def __init__(self) -> None:
        self._crypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._crypt_ctx.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        return self._crypt_ctx.verify(password, password_hash)
