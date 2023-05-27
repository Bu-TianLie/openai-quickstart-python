import asyncio
import os
import openai

from fastapi import APIRouter
# from rocketmq.client import Message
from starlette.responses import JSONResponse

from app.settings import settings
# from app.utils import producer
from app.model.models import RequestBody

router = APIRouter()

openai.api_key = "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"


@router.post("/ad-plan")
async def ad_plan_create(item: RequestBody):
    # timeout
    """
            api_key=None,
        api_base=None,
        api_type=None,
        request_id=None,
        api_version=None,
        organization=None,
                engine = params.pop("engine", None)
        timeout = params.pop("timeout", None)
        stream = params.get("stream", False)
        headers = params.pop("headers", None)
    """
    prompt = item.prompt

    def itercompletions(completions):
        for message in completions:
            # a = json.dumps(i.choices[0].text).encode("utf-8")
            # print(i.choices[0].text,end="")
            data = message.choices[0].delta.get('content')
            if data:
                yield data

    # await asyncio.to_thread(ad_plan_gpt,prompt, item.requestId)
    resp_str = ad_plan_gpt(prompt, item.requestId)
    return JSONResponse(content={
        "data": resp_str
    })


@router.post("/ad-group")
async def ad_group_create(item: RequestBody):
    prompt = item.prompt
    # await asyncio.to_thread(ad_group_gpt, prompt, item.requestId)
    resp_str =  ad_group_gpt(prompt, item.requestId)

    return JSONResponse(content={
        "data": resp_str
    })


def ad_plan_gpt(prompt, requestId):
    messages = [
        {"role": "system", "content": "python工程师"},
        {"role": "user", "content": "根据示例生成快手广告投放计划api请求参数,要求只输出json数据"},
        {"role": "assistant",
         "content": "输出格式示例：{'advertiser_id': 0, 'ad_type': 0, 'type': 2, 'bid_type': 0, 'auto_build_name_rule': {'creative_name_rule': None, 'unit_name_rule': None}, 'auto_build': 0, 'campaign_name': '525增长实验', 'auto_adjust': 0, 'day_budget': 500000, 'day_budget_schedule': []}"},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_API_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.7,
        stream=True,
        n=1
    )
    resp_list = []

    for message in response:
        if message.choices[0].delta.get('content'):
            # print(message.choices[0].delta.get('content'), end="")
            resp_list.append(message.choices[0].delta.get('content'))
    resp_str = "".join(resp_list)
    return resp_str
    # await send_msg("ad-plan", resp_str, requestId)


def ad_group_gpt(prompt, requestId):
    eg = {'advertiser_id': 17031121, 'campaign_id': 1513462152, 'scene_ids': [6], 'scene_type': 1, 'app_id': 14262443,
          'schema_uri': '', 'schema_url': '', 'appStore': [], 'use_app_market': False, 'convert_id': 0,
          'download_page_type': 0, 'site_id': '0', 'download_page_url': '', 'playable_id': 0, 'play_button': '',
          'app_download_type': 0, 'pec_coin_switch': False, 'dpa_sub_type': 0, 'dpa_library_id': 0,
          'dpa_product_id': '', 'quick_search': 0, 'word_info_list': [], 'extend_search': 0, 'target_explore': 0,
          'related_template_id': 0, 'template_name': '',
          'ad_dsp_target': {'age': [], 'behavior_interest': {}, 'device_brand': [], 'device_price': [],
                            'exclude_population': [], 'filter_converted_level': 0, 'gender': '', 'id': 0,
                            'interest': [], 'network': [], 'package_name': [], 'paid_audience': [],
                            'platform': {'android': {'min': 3}}, 'population': [], 'region_category_names': [],
                            'region_category_ids': [], 'user_type': 0, 'celebrity': {}, 'intelli_extendOption': 0,
                            'target_source': 1, 'seed_population': [], 'region_type': 0, 'app_interest_ids': [],
                            'appinterest_id_names': [], 'ip_type': 0, 'filter_time_range': 0, 'behavior_type': 0,
                            'device_brand_ids': [], 'media_source_type': 0, 'media': [], 'exclude_media': [],
                            'disable_installed_app_switch': 0}, 'day_budget': 100000, 'schedule': '[]',
          'budget_schedule': [], 'begin_time': 1684994272859, 'end_time': 0, 'constraint_action_type': 0,
          'constraint_cpa': 0, 'bid_type': 2, 'bid': 200, 'ocpx_action_type': 0, 'cpa_bid': 0, 'roi_ratio': 0,
          'deep_conversion_type': 0, 'deep_conversion_bid': 0, 'twin_bid_priority': 1, 'enhance_conversion_type': 0,
          'name': 'test1'}

    messages = [
        {"role": "system", "content": "python工程师"},
        {"role": "user", "content": "根据示例生成快手创建广告组api请求参数,要求只输出请求体，请求体为json格式"},
        {"role": "assistant",
         "content": f"输出格式示例：{eg}"},
        {"role": "user", "content": prompt},
    ]
    response = openai.ChatCompletion.create(
        model=settings.OPENAI_API_MODEL,
        messages=messages,
        max_tokens=200,
        temperature=0.7,
        stream=True,
        n=1
    )
    resp_list = []

    for message in response:
        if message.choices[0].delta.get('content'):
            # print(message.choices[0].delta.get('content'), end="")
            resp_list.append(message.choices[0].delta.get('content'))
    resp_str = "".join(resp_list)
    return resp_str
    # await send_msg("ad-group", resp_str, requestId)


#def send_msg(tag, msg_body, request_id):
#     try:
#         msg = Message(settings.RQ_TOPIC)
#         msg.set_tags(tag)
#         msg.set_keys(request_id)
#         msg.set_body(msg_body)
#         producer.send_sync(msg)
#     except Exception as e:
#         print(e)
