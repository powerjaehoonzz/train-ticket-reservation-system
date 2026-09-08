from pwdlib import PasswordHash


class PasswordHasher:
    def __init__(self) -> None:
        self._hasher = PasswordHash.recommended()
        self._dummy_hash = self._hasher.hash("dummy-password-for-timing-attack")

    def hash(self, plain_password: str) -> str:
        return self._hasher.hash(plain_password)

    def verify_and_update(
        self, plain_password: str, hashed_password: str
    ) -> tuple[bool, str | None]:
        return self._hasher.verify_and_update(plain_password, hashed_password)

    def verify_dummy(self, plain_password: str) -> None:
        try:
            self._hasher.verify(plain_password, self._dummy_hash)
        except Exception:
            pass


password_hasher = PasswordHasher()
