from pydantic import BaseModel


class RequestOptions(BaseModel):
    # lastContext: str
    # message: str
    # systemMessage: str
    parentMessageId: str = ""


class RequestBodyAdGroup(BaseModel):
    #requestId: str = ""
    advertiser_id: int  # 广告主 ID
    campaign_id: int  # 广告计划 ID
    unit_name: str  # 广告组名称
    bid_type: int  # 优化目标出价类型
    begin_time: str
    #day_budget: int
    #day_budget_schedule: int
    app_id: int


class RequestBodyAdPlan(BaseModel):
    #requestId: str = ""
    advertiser_id: int  # 广告主 ID
    campaign_name: str
    type: int

