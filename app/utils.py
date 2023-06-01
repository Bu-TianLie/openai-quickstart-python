
from rocketmq.client import Producer, Message

from app.settings import settings

# 创建一个 RocketMQ 消息生产者
producer = Producer(settings.RQ_PRODUCER_GROUP)

# 设置 Name Server 的地址
producer.set_namesrv_addr(settings.RQ_ADDR)


def send_msg(tag, msg_body, request_id):
    try:
        msg = Message(settings.RQ_TOPIC)
        msg.set_tags(tag)
        msg.set_keys(request_id)
        msg.set_body(msg_body)
        producer.send_sync(msg)
    except Exception as e:
        print(e)
        print(f"mq send msg fail! requestId: {request_id}")

