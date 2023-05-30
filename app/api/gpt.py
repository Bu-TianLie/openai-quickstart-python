
from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse


from app.model.models import RequestBody
from app.services.fastgpt import GPTServices
from app.utils import send_msg

router = APIRouter()


def chat_and_to_mq(item: RequestBody, api_name, mqtag):
    resp = GPTServices.chat(item.prompt, apiname=api_name)
    if resp:
        send_msg(mqtag, resp, item.requestId)
    else:
        resp = {
            "code": 401,
            "statusText": "Failed",
            "data": ""
        }
        send_msg(mqtag, resp, item.requestId)


@router.post("/ad-plan")
async def ad_plan_create(item: RequestBody, background_tasks: BackgroundTasks):
    background_tasks.add_task(chat_and_to_mq, item, "创建广告计划", "ad-plan")
    # resp_str = ad_plan_gpt(prompt, item.requestId)
    return JSONResponse(content={
        "status": "success",
        "requestId": item.requestId
    })


@router.post("/ad-group")
async def ad_group_create(item: RequestBody, background_tasks: BackgroundTasks):

    background_tasks.add_task(chat_and_to_mq, item, "创建广告组", "ad-group")

    return JSONResponse(content={
        "status": "success",
        "requestId": item.requestId
    })
