import json
import logging
from rocketmq.client import Producer, Message

from app.settings import settings

# 创建一个 RocketMQ 消息生产者
producer = Producer(settings.RQ_PRODUCER_GROUP)

# 设置 Name Server 的地址
producer.set_namesrv_addr(settings.RQ_ADDR)


def send_msg(tag, msg_body, request_id):
    try:
        msg = Message(settings.RQ_TOPIC)
        print(f"msg_type:{type(msg_body)} msg: {msg_body}")
        msg.set_tags(tag)
        msg.set_keys(str(request_id))
        msg.set_body(json.dumps(msg_body).encode())
        ret = producer.send_sync(msg)
        print(f"send msg ret: {ret}")
    except Exception as e:
        print(repr(e))
        logging.exception(e)
        print(f"mq send msg fail! requestId: {request_id}")

