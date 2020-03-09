import gym

MAX_EPISODE = 3

# 環境の初期化
env = gym.make('CartPole-v1')

for i in range(MAX_EPISODE):

    print("Episode {}".format(i))
    
    # 環境の初期化
    observation = env.reset()
    
    for step in range(1000):
        env.render()

        cart_position = observation[0] #カートの位置
        cart_speed = observation[1] #カートの速度
        pole_angle = observation[2] #ポールの角度
        pole_speed = observation[3] #ポールの速度

        action = env.action_space.sample()
        
        observation, reward, done, info = env.step(action)
        
        if done:
            print("Finished After {} Steps".format(step + 1))        
            break


env.close()    
