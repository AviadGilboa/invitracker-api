import bcrypt

def verify(
    plain_password: str,
    hashed_password: str
) -> bool:
        return bcrypt.checkpw(
            password=plain_password.encode("utf-8"),
            hashed_password=hashed_password.encode("utf-8")
        )

def hash(
    password: str
) -> str:
        return bcrypt.hashpw(
            password=password.encode("utf-8"),
            salt=bcrypt.gensalt()
        ).decode("utf-8")
