import time, asyncio
import cryptocompare
# from datetime import datetime



from kafkaHelper import initProducer, produceRecord
from config import config, params

# real time data collector
async def async_getCryptoRealTimeData(producer, topic, crypto, time_inverval):
    while True:
        t_0 = time.time()
        # call API
        raw_data = {}
        raw_data["name"] =  crypto
        raw_data["currency"] = params['ref_currency']
        raw_data["amount"] = cryptocompare.get_price(crypto, currency=params['ref_currency'])[crypto][params['ref_currency']]
        raw_data["time"] = time.time()

        if raw_data["amount"]:
            print('API request at time {0}'.format(time.time()))
            # produce record to kafka
            produceRecord(raw_data, producer, topic)
            # debug \ message in prompt
            # print('Produce record to topic \'{0}\' at time {1}'.format(topic, datetime.now()))
            
            print('Record: {}'.format(raw_data))

        else:
            # debug / print message
            print('Failed API request at time {0}'.format(time.time()))
        # wait
        await asyncio.sleep(time_inverval - (time.time() - t_0))

# initialize kafka producer
producer = initProducer()
# define async routine
async def main():
    await asyncio.gather(
    async_getCryptoRealTimeData(producer, config['topic_1'], params['currency_1'], params['api_call_period']),
    async_getCryptoRealTimeData(producer, config['topic_2'], params['currency_2'], params['api_call_period']),
    async_getCryptoRealTimeData(producer, config['topic_3'], params['currency_3'], params['api_call_period']),
    # async_getCryptoRealTimeData(producer, config['topic_4'], params['currency_4'], params['api_call_period']),
    # async_getCryptoRealTimeData(producer, config['topic_5'], params['currency_5'], params['api_call_period']),
    # async_getCryptoRealTimeData(producer, config['topic_6'], params['currency_6'], params['api_call_period']),
)
# run async routine
asyncio.get_event_loop().run_until_complete(main())