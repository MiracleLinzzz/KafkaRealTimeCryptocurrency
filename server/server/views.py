import time 
import json
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
from django.shortcuts import render
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/kafka'))
from config import config, params
from kafkaHelper import produceRecord, consumeRecord, initConsumer, initProducer

@accept_websocket
def test(request):
    
    if request.is_websocket():
        print('websocket connection....')
        msg = request.websocket.wait()  # 接收前端发来的消息
        print(msg, type(msg), json.loads(msg))  # b'["1","2","3"]' <class 'bytes'> ['1', '2', '3']
        consumer_1 = initConsumer(config['topic_1'])
        consumer_2 = initConsumer(config['topic_2'])
        consumer_3 = initConsumer(config['topic_3'])
        # consumer_4 = initConsumer(config['topic_4'])
        # consumer_5 = initConsumer(config['topic_5'])
        # consumer_6 = initConsumer(config['topic_6'])
        while 1:
            if msg:
                records = {}
                records[config['topic_1']] = consumeRecord(consumer_1)[0]
                records[config['topic_2']] = consumeRecord(consumer_2)[0]
                records[config['topic_3']] = consumeRecord(consumer_3)[0]
                # records[config['topic_4']] = consumeRecord(consumer_4)[0]
                # records[config['topic_5']] = consumeRecord(consumer_5)[0]
                # records[config['topic_6']] = consumeRecord(consumer_6)[0]

                request.websocket.send(str(records).encode())  # 向客户端发送数据
                time.sleep(0.5)  # 每0.5秒发一次
        # request.websocket.close()
    else:  # 如果是普通的请求返回页面
        return render(request, 'template.html')