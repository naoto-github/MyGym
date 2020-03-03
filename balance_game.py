import gym
import time
import math
import random
import numpy as np

MAX_REPEAT = 60
SLEEP_TIME = 0.1

# 環境の初期化
env = gym.make('CartPole-v1')

# 状態の価値
values = {}

# 学習率
alpha = 0.1

# 重み
weight = [2/10, 0, 2/10, 6/10]

# 状態の取得
def getState(observation, action):

    # 状態の符号で表現
    state = (np.sign(observation[0]), np.sign(observation[1]), np.sign(observation[2]), np.sign(observation[3]), action)
    
    return state

# 報酬の取得
def getReward(observation):
    
    reward = -1 * (weight[0] * math.fabs(observation[0]) +
                   weight[1] * math.fabs(observation[1]) +
                   weight[2] * math.fabs(observation[2]) +
                   weight[3] * math.fabs(observation[3]))

    return reward

# 状態の価値の更新
def updateValues(state, reward):

    if state in values:
        values[state] = (1 - alpha) * values[state] + alpha * reward
        #print("update")
    else:
        values[state] = alpha * reward
        #print("initialize")
        
    
# キーボード入力で行動選択
def keyAction():
    
    while True:
        print("Please input 0 or 1 > ", end="")
        action = int(input())
        if action == 0 or action == 1:
            break

    return action

# ランダムで行動選択
def randAction():
    action = env.action_space.sample()
    return action

# カートの角度で行動選択
def angleAction(pole_angle):
    if pole_angle >= 0:
        action = 1
    else:
        action = 0
    return action

# カートの速度で行動選択
def speedAction(pole_speed):
    if pole_speed >= 0:
        action = 1
    else:
        action = 0
    return action

# 状態の価値で行動選択
def greedyAction(observation):
    
    state0 = (np.sign(observation[0]), np.sign(observation[1]), np.sign(observation[2]), np.sign(observation[3]), 0)
    state1 = (np.sign(observation[0]), np.sign(observation[1]), np.sign(observation[2]), np.sign(observation[3]), 1)

    if (state0 in values) and (state1 in values):
        values0 = values[state0]
        values1 = values[state1]

        if(values0 > values1):
            action = 0
        else:
            action = 1        
    else:
        action = random.randint(0, 1)
        
    return action

# ルーレット選択で行動選択
def rouletteAction(observation):

    state0 = (np.sign(observation[0]), np.sign(observation[1]), np.sign(observation[2]), np.sign(observation[3]), 0)
    state1 = (np.sign(observation[0]), np.sign(observation[1]), np.sign(observation[2]), np.sign(observation[3]), 1)

    if (state0 in values) and (state1 in values):
        values0 = values[state0]
        values1 = values[state1]

        threshold = values0 / (values0 + values1)
        if(threshold > random.random()):
            action = 1
        else:
            action = 0
        
    else:
        action = random.randint(0, 1)
        
    return action



for i in range(MAX_REPEAT):

    # 環境の初期化
    observation = env.reset()
    
    for step in range(1000):
        env.render()

        cart_position = observation[0] #カートの位置
        cart_speed = observation[1] #カートの速度
        pole_angle = observation[2] #ポールの角度
        pole_speed = observation[3] #ポールの速度

        if(i >= (MAX_REPEAT - 10)):
            #print("CP:{:.2f} CV:{:.2f} PA:{:.2f} PV:{:.2f}".format(cart_position, cart_speed, pole_angle, pole_speed))    
            
            action = greedyAction(observation)
            #action = rouletteAction(observation)
            #print(action)

            observation, reward, done, info = env.step(action)

            #time.sleep(SLEEP_TIME)
        else:
            #action = keyAction()
            action = randAction()
            #action = angleAction(pole_angle)
            #action = speedAction(pole_speed)                        

            state = getState(observation, action)
            #print(state)

            observation, reward, done, info = env.step(action)
            
            reward = getReward(observation)
            #print(reward)

            updateValues(state, reward)
        
        if done:
            print("Finished After {} Steps".format(step + 1))        
            break

print(values)
env.close()    

