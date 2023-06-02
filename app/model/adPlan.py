from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class CampaignType(str, Enum):
    INSTALL_APP = '2'
    GET_ORDER = '3'
    PROMOTE_BRAND = '4'
    COLLECT_LEADS = '5'
    INCREASE_APP_ACTIVITY = '7'
    PROMOTE_PRODUCT_LIBRARY = '9'
    FAN_LIVE_PROMOTION = '16'
    MINI_PROGRAM_PROMOTION = '19'


class AutoBuildNameRule(BaseModel):
    unit_name_rule: str
    creative_name_rule: str


class AdPlan(BaseModel):
    advertiser_id: int  # 广告主 ID
    campaign_name: str = Field(min_length=1, max_length=100)
    type: int = Field(ge=1, le=2)
    day_budget: Optional[int] = 0
    day_budget_schedule: Optional[List[int]] = []
    ad_type: Optional[int] = Field(default=0, le=0, lt=1)
    bid_type: Optional[int] = Field(le=0, lt=1)
    auto_adjust: Optional[int] = Field(le=0, lt=1)
    auto_build: Optional[int] = Field(le=0, lt=1)
    auto_build_name_rule: Optional[AutoBuildNameRule] = None

    class Config:
        allow_population_by_field_name = True
