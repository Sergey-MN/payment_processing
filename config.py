from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=r".env",
                                      extra='ignore')


class RabbitSettings(BaseSettings):
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_QUEUE: str
    RABBITMQ_EXCHANGE: str
    RABBITMQ_ROUTING_KEY: str

    @property
    def RABBITMQ_URL(self) -> str:
        return f"pyamqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"

    model_config = SettingsConfigDict(env_file=r".env",
                                      extra='ignore')


class Settings(PostgresSettings, RabbitSettings):
    API_KEY: str


settings = Settings()
