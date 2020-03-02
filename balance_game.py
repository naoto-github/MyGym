import gym
import time
import numpy as np

env = gym.make('CartPole-v1')
observation = env.reset()

# 状態の変換
def getState(cart_position, cart_speed, pole_position, pole_speed, action):
    state = (np.sign(cart_position), np.sign(cart_speed), np.sign(pole_position), np.sign(pole_speed), action)
    return state
        
# キーボード入力(0:左 1:右)
def keyAction():
    
    while True:
        print("Please input 0 or 1 > ", end="")
        action = int(input())
        if action == 0 or action == 1:
            break

    return action

# ランダム入力
def randAction():
    action = env.action_space.sample()
    return action

# カートの角度
def angleAction(pole_angle):
    if pole_angle >= 0:
        action = 1
    else:
        action = 0
    return action

# カートの速度
def speedAction(pole_speed):
    if pole_speed >= 0:
        action = 1
    else:
        action = 0
    return action

for i in range(1000):
    env.render()

    cart_position = observation[0] #カートの位置
    cart_speed = observation[1] #カートの速度
    pole_angle = observation[2] #ポールの角度
    pole_speed = observation[3] #ポールの速度

    print("CP:{:.2f} CV:{:.2f} PA:{:.2f} PV:{:.2f}".format(cart_position, cart_speed, pole_angle, pole_speed))
    
    #action = keyAction()
    #action = randAction()
    #action = angleAction(pole_angle)
    action = speedAction(pole_speed)

    state = getState(cart_position, cart_speed, pole_angle, pole_speed, action)
    print(state)
    
    time.sleep(0.1)
    
    observation, reward, done, info = env.step(action)
    
    if done:
        print("Finished After {} Steps".format(i+1))        
        break

env.close()    

