from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from app.config import settings
from app.repository import UserRepository
from app.erros import DadosInvalidosError, CredenciaisInvalidasError


def _verify_password(password: str, hashed: str) -> bool:
    pwd_bytes = password.encode("utf-8")[:72]
    return bcrypt.checkpw(pwd_bytes, hashed.encode("utf-8"))


def _generate_jwt(user: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    claims = {
        "sub": str(user["id"]),
        "email": user["email"],
        "name": user["name"],
        "exp": expire,
    }
    return jwt.encode(claims, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def executar_login(payload: dict, repo: UserRepository) -> dict:
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        raise DadosInvalidosError("Informe e-mail e senha.")

    user = repo.find_by_email(email)
    if not user or not _verify_password(password, user["password_hash"]):
        raise CredenciaisInvalidasError()

    token = _generate_jwt(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    }