import requests


class GPTServices:
    headers = {
        "Content-Type": "application/json",
        "apikey": "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"
    }
    def __init__(self):

        pass

    def pushData(self):
        pass

    def chat(self):
        data = {
            "chatId": "可选，claude才有效",
            "modelId": "6465c1d710e8b538917e8c36",
            "isStream": false,
            "prompts": [
                {
                    "obj": "System",
                    "value": "你是一个开发工程师"
                },
                {
                    "obj": "Human",
                    "value": "生成一个快手广告计划"
                }

            ]
        }
        requests.get()
        pass
