import bcrypt


def hash_password(password: str) -> bytes:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def check_password(plain_password: str, db_password: bytes) -> bool:
    password_bytes = bytes(plain_password, "utf-8")
    return bcrypt.checkpw(password_bytes, db_password)
