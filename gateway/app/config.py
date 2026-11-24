import os


class Settings:
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-jwt-key-payment-system")
    JWT_ALGORITHM: str = "HS256"
    RPC_TIMEOUT: float = float(os.getenv("RPC_TIMEOUT", "8.0"))


settings = Settings()