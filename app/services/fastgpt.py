import re
import json
#import demjson
#import simplejson as json
import requests
from pprint import pprint
from datetime import datetime
from app.settings import settings
from app.model.adGroup import AdUnit

class GPTServices:
    headers = {
        'apikey': settings.FASTGPT_APIKEY,
        'Content-Type': 'application/json'
    }

    def pushData(self):
        pass

    @staticmethod
    def chat(prompts, apiname, model_str):
        url = "https://doc.script.red/api/openapi/chat/chat"
        print(f"收到请求：{apiname}, {prompts}")
        payload = json.dumps({
            "modelId": "6465c1d710e8b538917e8c36",
            "isStream": False,
            "prompts": [
                {
                    "obj": "System",
                    "value": "你是一个专业的python开发工程师"
                },
                {
                    "obj": "Human",
                    "value": f"创建快手{apiname}接口请求参数\n当前时间：{datetime.now()}\n要求：结合下文给定的部分参数，模拟生成一个接口请求用例，(要求必须符合下文中的pydantic model规则,如果有),除了给定的参数外，其他参数模拟生成,value不能为null；每次生成的结果不能重复；输出格式为json代码,注意要生成合法标准的json数据格式;"},
                {
                    "obj": "Human",
                    "value": model_str
                },
                {
                    "obj": "Human",
                    "value": f"必填参数为:{prompts}"
                },
                {
                    "obj": "Human",
                    "value": "只需要生成json，不需要解释"
                }

            ]
        })
        pprint(f"payload: {json.loads(payload)}")
        try:
            # pass
            response = requests.request("POST", url, headers=GPTServices.headers, data=payload)
            print(f"response: {response.json()}")
            data = response.json().get('data')
            # ret = re.sub(r"{\n|\n\n}", "", data)
            ret = data.replace("\n","").replace(" ", "").replace("'",'"').replace('null','')
            if ret:
                data_str = re.search(r"(\{.*\})", ret)
                if data_str:
                    print(data_str.group(0))
                    print(type(data_str.group(0)))
                    new_data = json.loads(json.dumps(eval(data_str.group(0))))
                    return {"code": 200, "statusText": "", "data": new_data}
        except Exception as e:
            print(e)
            print("service fastgpt")
            return


if __name__ == '__main__':
    GPTServices.chat("广告目标：提升应用下载量", "广告计划")
    # data = {'code': 200, 'statusText': '',
    #  'data': '好的，以下是符合文档规则的创建广告计划请求体JSON示例，用于提升应用下载量的广告目标：\n\n```json\n{\n    "campaign_type": "APP_DOWNLOAD",\n    "campaign_name": "My Campaign",\n    "budget_mode": "BUDGET_MODE_INFINITE",\n    "landing_type": "APP_DOWNLOAD",\n    "bid_amount": 100,\n    "targeting": {\n        "age": {\n            "include": [18, 19, 20],\n            "exclude": [15, 16, 17]\n        },\n        "gender": {\n            "include": ["GENDER_MALE"]\n        },\n        "region_code": {\n            "include": ["CN-HL"]\n        }\n    },\n    "promoted_object_type":"PROMOTED_OBJECT_TYPE_APP_IOS",\n    "promoted_object_spec":{\n        "app_ios_spec":{\n            "app_id":"1234567890"\n        }\n    }\n}\n```'}
    # ret = re.sub(r"[\n|\n\n]", "", data.get('data'))
    # if ret:
    #     print(repr(ret))
    #     data_str = re.search(r"(\{.*\})", ret)
    #     if data_str:
    #         print(repr(data_str.group(0)))
    #         new_data = json.loads(data_str.group(0))
    #         print(new_data)
