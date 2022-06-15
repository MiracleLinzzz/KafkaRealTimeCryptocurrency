
import atexit
import logging
import os
from kafka.errors import KafkaError, KafkaTimeoutError
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from config import config
import json
import ast
# logger_format = '%(asctime)s - %(message)s'
# logging.basicConfig(format=logger_format)
# logger = logging.getLogger('stream-processing')
# logger.setLevel(logging.INFO)

java8_location = 'F:\Program Files\Java\jdk1.8.0_331' 
os.environ['JAVA_HOME'] = java8_location

os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars spark-streaming-kafka-0-8-assembly_2.11-2.1.1.jar pyspark-shell'
# def shutdown_hook(producer):
# 	"""
# 	a shutdown hook to be called before the shutdown
# 	"""
# 	try:
# 		logger.info('Flushing pending messages to kafka, timeout is set to 10s')
# 		producer.flush(10)
# 		logger.info('Finish flushing pending messages to kafka')
# 	except KafkaError as kafka_error:
# 		logger.warn('Failed to flush pending messages to kafka, caused by: %s', kafka_error.message)
# 	finally:
# 		try:
# 			logger.info('Closing kafka connection')
# 			producer.close(10)
# 		except Exception as e:
# 			logger.warn('Failed to close kafka connection, caused by: %s', e.message)



if __name__ == '__main__':
    # Setup command line arguments.
    # parser = argparse.ArgumentParser()
    # parser.add_argument('source_topic')
    # parser.add_argument('target_topic')
    # parser.add_argument('kafka_broker')
    # parser.add_argument('batch_duration', help='the batch duration in secs') # spark mini-batch streaming

    # # Parse arguments.
    # args = parser.parse_args()
    # source_topic = args.source_topic
    # target_topic = args.target_topic
    # kafka_broker = args.kafka_broker
    # batch_duration = int(args.batch_duration)

    # Create SparkContext and SteamingContext.
    # https://spark.apache.org/docs/2.2.0/api/python/index.html
    sc = SparkContext() # 2 threads
    # sc.setLogLevel('INFO')
    ssc = StreamingContext(sc, 2)
    print()
    # Instantiate a kafka stream for processing.
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [config['topic_1']], {'metadata.broker.list':config['kafka_broker']})
    # directKafkaStream.pprint()
    # line1 = ssc.socketTextStream('192.168.10.11', 9999)
    # out1 = line1.map(lambda x: (len(x), x)).groupByKey()    # value 没有进行任何操作
    # out1.pprint()
    # directKafkaStream.pprint()
    # Extract value from directKafkaStream (key, value) pair.
    stream = directKafkaStream.map(lambda msg: msg[1])
    # counts = stream.pprint()
    # if counts:
        # counts = ast.literal_eval(counts)
        # stream.pprint()
    # time_stream = stream.transform(lambda amount, time, rdd: ast.literal_eval(rdd.first()))
    
    # print(type(counts), counts)
    # print(stream)
    # if time_stream:
    #     print(time_stream)
        # time_stream.pprint()
    # amount_stream = stream.map(lambda x: x["amount"])
    # amount_stream.pprint()
    # print(time_tream.foreachRDD(lambda x: x.collect()))
    # print(amount_stream.foreachRDD(lambda x: x.collect()))



    winlogs = stream.window(30,2)
    winlogs.pprint()
    # atexit.register(shutdown_hook, kafka_producer)
    ssc.start()
    # print(type(counts), counts)
    ssc.awaitTermination()
    # print(type(counts), counts)