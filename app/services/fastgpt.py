import re
import json
import requests
from pprint import pprint

from app.settings import settings


class GPTServices:
    headers = {
        'apikey': settings.FASTGPT_APIKEY,
        'Content-Type': 'application/json'
    }

    def pushData(self):
        pass

    @staticmethod
    def chat(prompts, apiname):
        url = "https://doc.script.red/api/openapi/chat/chat"
        print(f"收到请求：{apiname}, {prompts}")
        payload = json.dumps({
            "modelId": "6465c1d710e8b538917e8c36",
            "isStream": False,
            "prompts": [
                {
                    "obj": "System",
                    "value": "你是一个专业的快手广告运营人员"
                },
                {
                    "obj": "Human",
                    "value": f"根据快手api{apiname}文档，生成用于创建{apiname}的json请求体，要求必须符合文档中的规则，保证所有参数都是文档中定义的"
                },
                {
                    "obj": "Human",
                    "value": prompts
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
            ret = data.replace("\n")
            if ret:
                data_str = re.search(r"(\{.*\})", ret)
                if data_str:
                    print(data_str)
                    new_data = json.loads(data_str.group(0))
                    return {'code': 200, 'statusText': '', 'data': new_data}
        except Exception as e:
            print(e)
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
