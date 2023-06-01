
from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse
from uuid import uuid4

from app.model.models import *
from app.services.fastgpt import GPTServices
from app.utils import send_msg

router = APIRouter()


def chat_and_to_mq(item, api_name, mqtag):
    prompts = item.json()
    resp = GPTServices.chat(prompts, apiname=api_name)
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
async def ad_plan_create(item: RequestBodyAdPlan, background_tasks: BackgroundTasks):
    request_id = uuid4()
    item.requestId = request_id
    background_tasks.add_task(chat_and_to_mq, item, "创建广告计划", "ad-plan")
    # resp_str = ad_plan_gpt(prompt, item.requestId)

    return JSONResponse(content={
        "status": "success",
        "requestId": request_id
    })


@router.post("/ad-group")
async def ad_group_create(item: RequestBodyAdGroup, background_tasks: BackgroundTasks):
    request_id = uuid4()
    item.requestId = request_id
    background_tasks.add_task(chat_and_to_mq, item, "创建广告组", "ad-group")

    return JSONResponse(content={
        "status": "success",
        "requestId": request_id
    })
