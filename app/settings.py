from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "openai-python"
    OPENAI_API_KEY: str = ""
    OPENAI_API_MODEL: str = "gpt-3.5-turbo"
    RQ_TOPIC: str = "kuaishou"
    RQ_PRODUCER_GROUP: str = ""
    RQ_ADDR: str = "127.0.0.1:9876"
    FASTGPT_ADDR: str = "https://doc.script.red/api/openapi/chat/chat"


settings = Settings()