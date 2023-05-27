from pydantic import BaseModel


class RequestOptions(BaseModel):
    # lastContext: str
    # message: str
    # systemMessage: str
    parentMessageId: str = ""


class RequestBody(BaseModel):
    prompt: str
    requestId: str = ""
