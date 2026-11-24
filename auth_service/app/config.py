import os


class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "auth_db")
    DB_NAME: str = os.getenv("DB_NAME", "auth")
    DB_USER: str = os.getenv("DB_USER", "auth")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "auth")

    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RPC_QUEUE: str = os.getenv("AUTH_RPC_QUEUE", "rpc.auth.requests")
    EVENTS_EXCHANGE: str = os.getenv("EVENTS_EXCHANGE", "domain.events")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-jwt-key-payment-system")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "12"))


settings = Settings()