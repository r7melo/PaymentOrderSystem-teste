import jwt
from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.config import settings
from app.rpc_client import rpc_client

router = APIRouter()


def get_current_user(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou inválido.")
    token = authorization.split(" ", 1)[1]
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido.")


class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str


@router.get("/health")
async def health():
    return {"status": "ok", "service": "gateway"}


@router.post("/auth/register", status_code=201)
async def register(body: RegisterSchema):
    res = await rpc_client.call("rpc.auth.requests", "register", body.model_dump())
    if res["status"] >= 400:
        raise HTTPException(status_code=res["status"], detail=res["error"])
    return res["data"]


@router.post("/auth/login")
async def login(body: LoginSchema):
    res = await rpc_client.call("rpc.auth.requests", "login", body.model_dump())
    if res["status"] >= 400:
        raise HTTPException(status_code=res["status"], detail=res["error"])
    return res["data"]


@router.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return {"user_id": user["sub"], "email": user["email"], "name": user["name"]}