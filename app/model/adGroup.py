from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional, List


class BidTypeEnum(Enum):
    CPC = 2
    OCPM = 10
    MCB = 12


class ShowModeEnum(Enum):
    CAROUSEL = 1
    PREFERRED = 2


class OCPXActionTypeEnum(Enum):
    ACTION_BAR_CLICK = 2
    ACTIVATION = 180
    FORM_SUBMISSION = 53
    PHONE_ACTIVATION = 109
    ROOM_MEASUREMENT = 137
    PAYMENT = 190
    FIRST_DAY_ROI = 191
    APP_INSTALLATION = 324
    EFFECTIVE_LEADS = 348
    CREDIT = 383
    COMPLETED_ITEM = 384
    ORDER_SUBMISSION = 394
    REGISTRATION = 396
    WECHAT_COPY = 715
    MULTI_CONVERSION_EVENT = 716
    AD_WATCH_TIMES = 717
    AD_WATCH_5_TIMES = 731
    AD_WATCH_10_TIMES = 732
    AD_WATCH_20_TIMES = 733
    KEY_ACTION = 773
    SEVEN_DAY_ROI = 774
    INCREASE_FANS = 72
    SEVEN_DAY_PAYMENT_TIMES = 739
    PRODUCT_VISIT = 392
    ORDER_PAYMENT = 395
    LIVE_WATCH = 62
    LIVE_ROI = 192
    APPOINTMENT_FORM = 634
    APPOINTMENT_CLICK = 635
    ACTIVATION_PAYMENT = 810
    NATURAL_RETENTION = 346


class Target(BaseModel):
    region: Optional[List[int]] = None
    age: Optional[dict] = None
    gender: Optional[int] = None


class AdUnit(BaseModel):
    advertiser_id: int  # 广告主 ID
    campaign_id: int  # 广告计划 ID
    unit_name: str = Field(min_length=1, max_length=100)  # 广告组名称
    put_status: Optional[int] = Field(ge=1, le=2)
    bid_type: BidTypeEnum
    bid: Optional[int] = Field(ge=0.2, le=100)
    cpa_bid: Optional[int] = Field()
    ocpx_action_type: OCPXActionTypeEnum = None
    show_mode: ShowModeEnum
    scene_id: List[int]
    unit_type: int
    begin_time: str
    app_id: str
    roi_ratio: float = None
    target: Target

    class Config:
        allow_population_by_field_name = True


class DeepConversionType(str, Enum):
    PAYMENT = '3'
    NEXT_DAY_RETENTION = '7'
    COMPLETED_ITEM = '10'
    CREDIT = '11'
    ADD_TO_CART = '13'
    SUBMIT_ORDER = '14'
    PURCHASE = '15'
    EFFECTIVE_LEADS = '44'
    PAYMENT_ROI = '92'
    NEXT_DAY_RETENTION_24H = '181'

