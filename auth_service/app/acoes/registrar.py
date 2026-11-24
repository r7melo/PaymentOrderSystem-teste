import bcrypt
from app.repository import UserRepository
from app.publisher import EventPublisher
from app.erros import DadosInvalidosError, EmailJaCadastradoError


def _hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pwd_bytes, bcrypt.gensalt()).decode("utf-8")


def executar_registro(payload: dict, repo: UserRepository, publisher: EventPublisher) -> dict:
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not name or not email or len(password) < 4:
        raise DadosInvalidosError("Nome, e-mail e senha (mínimo 4 caracteres) são obrigatórios.")

    if repo.find_by_email(email):
        raise EmailJaCadastradoError()

    password_hash = _hash_password(password)
    user = repo.create(name=name, email=email, password_hash=password_hash)

    # Dispara evento assíncrono no broker para criação de conta e auditoria
    publisher.publish_domain_event(
        routing_key="user.registered",
        payload={
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
        },
    )

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
    }