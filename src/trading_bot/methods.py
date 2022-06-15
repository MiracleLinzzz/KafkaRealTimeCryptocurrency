import os
import logging
import time
import numpy as np

from tqdm import tqdm

from .utils import (
    format_currency,
    format_position
)
from .ops import (
    get_state
)
import numpy as np
import matplotlib.pyplot as plt


import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../kafka'))
from config import config, params
from kafkaHelper import produceRecord, consumeRecord, initConsumer, initProducer



def train_model(agent, episode, data, ep_count=100, batch_size=32, window_size=10):
    total_profit = 0
    data_length = len(data) - 1

    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0, window_size + 1)

    for t in tqdm(range(data_length), total=data_length, leave=True, desc='Episode {}/{}'.format(episode, ep_count)):

        reward = 0
        next_state = get_state(data, t + 1, window_size + 1)

        # select an action
        action = agent.act(state)

        # BUY
        if action == 1:
            agent.inventory.append(data[t])

        # SELL
        elif action == 2 and len(agent.inventory) > 0:
            bought_price = agent.inventory.pop(0)
            delta = data[t] - bought_price
            reward = delta #max(delta, 0)
            total_profit += delta

        # HOLD
        else:
            pass

        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)

        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            avg_loss.append(loss)

        state = next_state

    if episode % 10 == 0:
        agent.save(episode)

    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))


def evaluate_model(agent, data, window_size, debug,time_get):

    consumer_1 = initConsumer(config['topic_1'])

    total_profit = 0
    data_length = len(data) - 1

    history = []
    agent.inventory = []
    buy = False
    state = get_state(data, 0, 11)
    get = True
    t = 0
    while(get==True):
        records_1 = consumeRecord(consumer_1)
        # time.sleep(1)
        if not records_1:
            continue
        records_1 = records_1[0]
        data.append(records_1["amount"])
        strings = time.strftime("%Y,%m,%d,%H,%M,%S", time.localtime(records_1["time"]))
        h= strings.split(',')
        numbers = [h[4], h[5]]
        time_get.append(str(numbers[0]) + '-' + str(numbers[1]))

        if (t > 20):
            plt.title('BTCUSD Model Prediction Graph')
            plt.xlabel('Price')
            plt.ylabel('Minute-Second')
            plt.plot(time_get[t - 20: t+1],data[t - 20: t+1])
            plt.xticks(rotation=70)
            plt.text(time_get[t], data[t], str(data[t]),fontsize=10)

        reward = 0
        next_state = get_state(data, t + 1, 11)

        # select an action
        action = agent.act(state, is_eval=True)

        # BUY
        if action == 1 and buy == False:
            if (t > 20):
                plt.plot(time_get[t], data[t], 'r^')

            agent.inventory.append(data[t])

            history.append((data[t], "BUY"))
            buy = True
            if debug:
                logging.debug("Buy at: {}".format(format_currency(data[t])))

        # SELL
        elif action == 2 and len(agent.inventory) > 0:
            buy = False
            if (t > 20):
                plt.plot(time_get[t], data[t], 'gv')

            bought_price = agent.inventory.pop(0)
            delta = data[t] - bought_price
            reward = delta #max(delta, 0)
            total_profit += delta

            history.append((data[t], "SELL"))
            if debug:
                logging.debug("Sell at: {} | Position: {}".format(
                    format_currency(data[t]), format_position(data[t] - bought_price)))
        # HOLD
        else:
            history.append((data[t], 'HOLD'))


        if (t > 45):
            plt.savefig('./server/static/img/1.png')
            plt.savefig('./src/Picture/1.png')
            plt.clf()
        t = t+1
        done = False
        agent.memory.append((state, action, reward, next_state, done))

        state = next_state
        if done:
            return total_profit, history
