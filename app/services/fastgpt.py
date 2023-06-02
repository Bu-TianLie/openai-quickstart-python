import re
import json
import logging
# import demjson
# import simplejson as json
import requests
from pprint import pprint

from app.settings import settings


class GPTServices:
    headers = {
        'apikey': settings.FASTGPT_APIKEY,
        'Content-Type': 'application/json'
    }

    ad_plan_doc = """好的，以下是创建快手广告计划接口的请求参数：

            请求接口： https://ad.e.kuaishou.com/rest/openapi/gw/dsp/campaign/create
            请求方式：POST
            数据格式：JSON
            
            请求参数：
            字段 类型 是否必填 说明 备注
            advertiser_id long 必填 广告主 ID 账号ID，在获取 access_token 的时候返回
            campaign_name string 必填 广告计划名称 长度为 1-100 个字符，同一个账号下面计划名称不能重复
            type int 必填 计划类型 2：提升应用安装；3：获取电商下单；4：推广品牌活动；5：收集销售线索；7：提高应用活跃；9：商品库推广（此营销目标下创建的默认为DPA广告）；16：粉丝/直播推广；19：小程序推广
            day_budget long 选填 单日预算金额 单位：厘，指定 0 表示预算不限，默认为 0；不小于 500 元，不超过 100000000 元，仅支持输入数字；修改预算不得低于该计划当日花费的 120%，与 day_budget_schedule 不能同时传，不能低于该计划下任一广告组出价。当 bid_type = 1时，day_budget 或者 budget_schedule 二选一必填
            day_budget_schedule long[] 选填 分日预算 单位：厘，指定 0 表示预算不限，默认为 0；每天不小于 500 元，不超过 100000000 元，仅支持输入数字；修改预算不得低于该计划当日花费的 120%，与 day_budget 不能同时传，均不能低于该计划下任一广告组出价。事例：时间周期为周一到周日，样例："day_budget_schedule":[11110000,22220000,0,0,0,0,0]，优先级高于day_budget。当 bid_type = 1时，day_budget 或者 budget_schedule 二选一必填
            ad_type int 选填 广告计划类型 0:信息流，1:搜索；不填默认信息流
            bid_type int 选填 出价类型 0:默认1:最大转化（添加后不可修改）
            auto_adjust int 选填 自动调控开关 0：关闭，1：开启【注：此字段设置为关闭时， auto_build 字段也必须为关闭，白名单功能】
            auto_build int 选填 自动基建开关 0：关闭，1：开启【注：此字段设置为开启时， auto_adjust 字段也必须为开启，白名单功能】
            auto_build_name_rule struct 自动基建命名规则 【注：白名单功能】
            auto_build_name_rule.unit_name_rule string 必填 广告组名称命名规则 必须同时包含[日期]和[序号]宏变量，eg: 系统自动搭建_[日期][序号]
            auto_build_name_rule.creative_name_rule string 必填 广告创意名称命名规则 必须同时包含[日期]和[序号]宏变量，eg: 系统自动搭建_[日期][序号]"""
    ad_plan_prompts_list = [
        {
            "obj": "Human",
            "value": f"创建快手广告计划接口请求参数;"
        },
        {
            "obj": "AI",
            "value": ad_plan_doc
        },
        {
            "obj": "Human",
            "value": f"根据上述文档生成一个请求用例;day_budget与day_budget_schedule参数只能二选一;格式为json代码"
        },
    ]
    ad_group_doc = """好的，以下是创建快手广告组接口的请求参数：
        请求接口： https://ad.e.kuaishou.com/rest/openapi/gw/dsp/ad_unit/create
        请求方式：POST
        数据格式：JSON
        请求参数：
        字段 类型 是否必填 说明 备注
        advertiser_id long 必填 广告主 ID 账号ID，在获取 access_token 的时候返回
        campaign_id long 必填 广告计划 ID
        unit_name string 必填 广告组名称 长度为 1-100 个字符，同一个广告计划下面广告组名称不能重复
        put_status int 选填 广告组的投放状态 0：暂停，1：投放，默认为投放状态
        bid_type int 必填 优化目标出价类型 0:默认出价，1:最大转化出价，2:手动CPC出价，3:手动CPM出价，4:手动oCPC出价
        bid long 选填 出价 单位：厘，默认为0；当 bid_type =2/3/4时必传；当 bid_type =1时不支持传入 bid 字段；
        cpa_bid long 选填 出价 单位：厘，默认为0；当 bid_type =1时必传；
        ocpx_action_type int 选填 优化目标 当 bid_type =1时必传；取值范围[1,3]，对应的行动是[安装、注册、购买]
        deep_conversion_type int 选填 深度转化目标 当 ocpx_action_type = 3 时必传；取值范围[1,5]，对应的行动是[加购、提交订单、支付订单、收藏、加购并支付]
        enhance_conversion_type int 选填 增强目标 当 ocpx_action_type = 2/3 时必传；取值范围[1,2]，对应的行动是[加购、提交订单]
        roi_ratio double 选填 付费 ROI 系数 取值范围 [0.1,10.0]，默认为0，当 bid_type =1时必传；
        deep_conversion_bid long 选填 深度转化目标出价 单位：厘，默认为0；当 deep_conversion_type 不为空时必传；
        scene_id int[] 必填 资源位置 至少要有一个资源位
        unit_type int 必填 创意制作方式 取值范围：1：手动创意；2：程序化创意；3：模板创意；4: 程序化创意2.0
        begin_time string 必填 投放开始时间 格式为 "yyyy-MM-dd HH:mm:ss"，如："2022-01-01 00:00:00"
        end_time string 选填 投放结束时间 格式为 "yyyy-MM-dd HH:mm:ss"，如："2022-01-01 00:00:00"（不传表示不限）
        schedule_time string 选填 投放时间段 投放时间段格式："HH:mm-HH:mm"，多个时间段用逗号隔开（不传表示全天投放），最多支持 6 个时间段，且时间段不能重复，且时间段总和不得超过 24 小时
        day_budget long 选填 单日预算金额 单位：厘，指定 0 表示预算不限，默认为 0；不小于 500 元，不超过 100000000 元，仅支持输入数字；修改预算不得低于该广告组当日花费的 120%，与 day_budget_schedule 不能同时传，不能低于该广告组下任一创意出价。当 bid_type =1时，day_budget 或者 budget_schedule 二选一必填
        day_budget_schedule long[] 必填 分日预算 单位：厘，指定 0 表示预算不限，默认为 0；每天不小于 500 元，不超过 100000000 元，仅支持输入数字；修改预算不得低于该广告组当日花费的 120%，与 day_budget 不能同时传，均不能低于该广告组下任一创意出价。事例：时间周期为周一到周日，样例："day_budget_schedule":[11110000,22220000,0,0,0,0,0]，优先级高于day_budget。当 bid_type =1时，day_budget 或者 budget_schedule 二选一必填
        convert_id int 选填 转化目标 ID 取值范围：1、2、3、4、5、6、7、8、9、10
        url_type int 选填 url 类型 0：普通链接，1：落地页链接，默认为 0
        web_uri_type int 选填 url 类型 取值范围：1：普通链接；2：落地页链接；3：小程序链接；4: 淘口令；5: 商品ID
        url string 选填 投放链接 当 url_type =0 或者 web_uri_type=1时必须传入
        site_id long 选填 建站ID/下载中间页ID 当 web_uri_type=2时必须传入
        group_id long 选填 程序化落地页ID 当 web_uri_type=3时必须传入
        schema_uri string 必填 调起链接 当 web_uri_type=3时必须传入，支持的协议有https、http、kuaishou、alipays等
        schema_id String 选填 微信小程序ID 当 web_uri_type =3并且 schema_uri 是小程序地址时，需要传该参数
        app_id long 必填 应用 ID
        app_download_type int 选填 应用下载方式 取值范围：0:系统默认下载方式;1:自定义下载方式;不传默认为系统默认下载方式
        use_app_market int 选填 优先从系统应用商店下载 取值范围：0:不优先从系统应用商店下载;1:优先从系统应用商店下载;不传默认为不优先从系统应用商店下载。当 app_download_type =1时，该参数生效。
        app_store string[] 选填 应用商店列表 取值范围：huawei、xiaomi、oppo、vivo、baidu、yingyongbao、qq，多个用逗号分隔。当 app_download_type =1时，该参数生效。
        show_mode int 必填 创意展现方式 取值范围：0：横版；1：竖版
        site_type int 加白 预约广告 取值范围：0:非预约广告；1:预约广告
        smart_cover boolean unit_type=7 选填 程序化创意 2.0 智能抽帧 当 unit_type=7时必填
        asset_mining boolean unit_type=7 选填 程序化创意 2.0 素材挖掘 当 unit_type=7时必填
        consult_id long 选填:从工具-获取可选咨询组件 咨询组件 id
        adv_card_option int 选填 高级创意开关 取值范围：0:关闭；1:开启
        adv_card_list long[] 选填 绑定卡片 id 当 adv_card_option =1时必传，最多支持绑定两个卡片
        playable_id Long 选填 试玩 ID 当 unit_type=3时必传，支持的试玩类型有[1,2,3,4]
        play_button String 选填 试玩按钮文字内容 当 playable_id 不为空时必传，长度不超过10个字符
        dpa_unit_param struct 选填 DPA 相关商品信息 当 unit_type=1时必填
        dpa_unit_param.product_id String 必填 商品 ID
        dpa_unit_param.product_name String 必填 商品名称
        dpa_unit_param.product_price long 必填 商品价格，单位：分
        dpa_unit_param.product_url String 必填 商品链接
        jingle_bell_id long 选填"""
    ad_group_prompts_list = [
        {
            "obj": "Human",
            "value": f"创建快手广告组接口请求参数;"
        },
        {
            "obj": "AI",
            "value": ad_plan_doc
        },
        {
            "obj": "Human",
            "value": f"根据上述文档生成一个请求用例;day_budget与day_budget_schedule参数只能二选一;格式为json代码"
        },
    ]

    def chat(self, prompt, api_name):
        url = "https://doc.script.red/api/openapi/chat/chat"
        print(f"收到请求：{api_name}, {prompt}")
        if api_name == "ad-plan":
            prompts = self.ad_plan_prompts_list
        else:
            prompts = self.ad_group_prompts_list
        data = {
            "modelId": "6465c1d710e8b538917e8c36",
            "isStream": False,
            "prompts": prompts
        }
        payload = json.dumps(data)
        pprint(f"payload: {json.loads(payload)}")
        try:
            response = requests.request("POST", url, headers=self.headers, data=payload)
            print(f"response: {response.json()}")
            data = response.json().get('data')
            return self.parse_data(data)

        except Exception as e:
            logging.exception(e)
            return

    def parse_data(self, data):
        try:
            ret = data.replace("\n", "").replace(" ", "").replace("'", '"')

            data_str = re.search(r"(\{.*\})", ret)
            if data_str:
                new_data = data_str.group(0)
                logging.info(f"new_data type : {type(new_data)};new_data: {new_data}")
                if new_data.endswith(",}"):
                    new_data.replace(",}", "}")
                new_data = json.loads(new_data)
                return {"code": 200, "statusText": "", "data": new_data}
        except Exception as e:
            logging.exception(e)
            return


if __name__ == '__main__':
    params = {
        "advertiser_id": 312312,
        "campaign_name": "ai创建计划测试22",
        "type": 2
    }
    GPTServices.chat(params, "广告计划", model_str="")
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
