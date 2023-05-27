from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "openai-python"
    OPENAI_API_KEY: str
    OPENAI_API_MODEL: str = "gpt-3.5-turbo"
    RQ_TOPIC: str = ""
    RQ_PRODUCER_GROUP: str = ""
    RQ_ADDR: str = ""


settings = Settings()