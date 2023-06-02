import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "openai-python"
    PRODUCT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OPENAI_API_KEY: str = ""
    OPENAI_API_MODEL: str = "gpt-3.5-turbo"
    RQ_TOPIC: str = "yeeu-ad"
    RQ_PRODUCER_GROUP: str = "yeeu"
    RQ_ADDR: str = "127.0.0.1:9876"
    FASTGPT_ADDR: str = "https://doc.script.red/api/openapi/chat/chat"
    FASTGPT_APIKEY: str = "6465bfea10e8b538917e8c2f-9pbqk2yqyjlggob3qdzhb"


settings = Settings()
print(settings.PRODUCT_DIR)