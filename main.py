
from fastapi import FastAPI

from app.utils import producer
from app.api.router import api_router

app = FastAPI(title="chatgpt-web")
app.include_router(api_router)


@app.on_event("startup")
async def startup():
    producer.start()


@app.on_event("shutdown")
async def shutdown():
    producer.shutdown()


if __name__ == '__main__':
    import uvicorn

    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8150 --reload
    uvicorn.run(
        app=app,
        host="localhost",
        port=60001,
    )
