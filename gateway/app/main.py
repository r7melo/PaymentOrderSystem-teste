from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.rpc_client import rpc_client
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rpc_client.connect()
    yield
    await rpc_client.close()


app = FastAPI(title="PaymentOrderSystem API Gateway", lifespan=lifespan)
app.include_router(router)