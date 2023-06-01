from rocketmq.client import Producer, Message

# 创建一个 RocketMQ 消息生产者
producer = Producer('con1')

# 设置 Name Server 的地址
producer.set_namesrv_addr('192.168.2.191:9876')

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
