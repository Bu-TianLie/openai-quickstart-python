
from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse
from uuid import uuid4

from app.model.models import *
from app.services.fastgpt import GPTServices
from app.utils import send_msg
from app.settings import settings
router = APIRouter()


def chat_and_to_mq(item, api_name, mqtag,request_id):
    prompts = item.json()
    model_path = None
    if mqtag == "ad-group":
        model_path = settings.PRODUCT_DIR +"/app/model/adGroup.py"
    #elif mqtag == 'ad-plan': 
        #model_path = settings.PRODUCT_DIR +"/app/model/adPlan.py"
    if model_path:
        with open(model_path, "r") as f:
            model_str = f.read()
    else:
        model_str = ""
    resp = GPTServices.chat(prompts, apiname=api_name, model_str=model_str)
    if resp:
        send_msg(mqtag, resp,request_id)
    else:
        resp = {
            "code": 401,
            "statusText": "Failed",
            "data": ""
        }
        print("fail")
        send_msg(mqtag, resp,request_id)


@router.post("/ad-plan")
async def ad_plan_create(item: RequestBodyAdPlan, background_tasks: BackgroundTasks):
    request_id = uuid4()
    #item.requestId = request_id
    background_tasks.add_task(chat_and_to_mq, item, "创建广告计划", "ad-plan",request_id)
    # resp_str = ad_plan_gpt(prompt, item.requestId)

    return JSONResponse(content={
        "status": "success",
        "requestId": str(request_id)
    })


@router.post("/ad-group")
async def ad_group_create(item: RequestBodyAdGroup, background_tasks: BackgroundTasks):
    request_id = uuid4()
    #item.requestId = request_id
    background_tasks.add_task(chat_and_to_mq, item, "创建广告组", "ad-group",request_id)

    return JSONResponse(content={
        "status": "success",
        "requestId": str(request_id)
    })
