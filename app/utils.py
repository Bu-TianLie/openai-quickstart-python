import os

from rocketmq.client import Producer, Message

from app.settings import settings

# 创建一个 RocketMQ 消息生产者
producer = Producer("kuaishou")

# 设置 Name Server 的地址
producer.set_namesrv_addr("http://host.docker.internal:9876")


# 启动生产者
producer.start()

# 创建一个消息对象
message = Message('my_topic', )
message.set_keys("654321")
message.set_tags("123456")
message.set_body('Hello, RocketMQ!')
# 发送消息到 RocketMQ
producer.send_sync(message)

# 关闭生产者
producer.shutdown()
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
