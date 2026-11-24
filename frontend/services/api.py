import os
import httpx

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://gateway:8000")


def extract_error_message(exc: httpx.HTTPStatusError) -> str:
    try:
        data = exc.response.json()
        return data.get("detail", f"Erro HTTP {exc.response.status_code}")
    except Exception:
        return f"Erro HTTP {exc.response.status_code}"


class GatewayClient:
    def __init__(self, token: str | None = None):
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}

    async def login(self, email: str, password: str) -> dict:
        async with httpx.AsyncClient(base_url=GATEWAY_URL, timeout=10.0) as client:
            resp = await client.post("/auth/login", json={"email": email, "password": password})
            resp.raise_for_status()
            return resp.json()

    async def register(self, name: str, email: str, password: str) -> dict:
        async with httpx.AsyncClient(base_url=GATEWAY_URL, timeout=10.0) as client:
            resp = await client.post(
                "/auth/register",
                json={"name": name, "email": email, "password": password},
            )
            resp.raise_for_status()
            return resp.json()

    async def get_me(self) -> dict:
        async with httpx.AsyncClient(base_url=GATEWAY_URL, headers=self.headers, timeout=10.0) as client:
            resp = await client.get("/auth/me")
            resp.raise_for_status()
            return resp.json()