import os

from rocketmq.client import Producer

from app.settings import settings

# 创建一个 RocketMQ 消息生产者
producer = Producer(settings.RQ_PRODUCER_GROUP)

# 设置 Name Server 的地址
producer.set_name_server_address(settings.RQ_ADDR)

# # 启动生产者
# producer.start()
#
# # 创建一个消息对象
# message = Message('my_topic', 'Hello, RocketMQ!')
#
# # 发送消息到 RocketMQ
# producer.send_sync(message)
#
# # 关闭生产者
# producer.shutdown()
