import gym
import numpy as np
import cv2
import os
import shutil
import pickle
import argparse

# 最大ステップ数
MAX_STEP = 200

# 目標ステップ数
TARGET_STEP = 180

# 離散値の数
BIN_NUMBER = 6

# Qテーブル
q_table = {}

# 学習率
alpha = 0.2

# 割引率
gamma = 0.9

# フレーム画像の保存
IMAGE_DIR = "images/"
rgb_arrays = []

# 履歴（ステップ数）
histories = []

# 引数の処理
parser = argparse.ArgumentParser(description="Balance Game on OpenAI Gym")
parser.add_argument("-r", "--reset", help="Reset Q-Table File", action="store_false")
parser.add_argument("-i", "--input", help="Input Q-Table File", default="qtable.dump")
parser.add_argument("-o", "--output", help="Output Q-Table File", default="qtable.dump")
parser.add_argument("-e", "--epsilon", help="Max Value of Epsilon", type=float, default=0.5)
parser.add_argument("-n", "--number", help="Max Number of Episodes", type=int, default=10)
args = parser.parse_args()

Q_FILE_INPUT = args.input # 入力用のQテーブル
Q_FILE_OUTPUT = args.output # 書込用のQテーブル
READ_Q_FILE = args.reset # Qテーブルの読込
MAX_EPSILON = args.epsilon # ランダム率の最大値
MAX_EPISODE = args.number # 最大エピソード数

# 離散値の範囲
bins = []
bins.append(np.linspace(-2.4, 2.4, BIN_NUMBER))
bins.append(np.linspace(-3.0, 3.0, BIN_NUMBER))
bins.append(np.linspace(-0.5, 0.5, BIN_NUMBER))
bins.append(np.linspace(-2.0, 2.0, BIN_NUMBER))

# 観測データを状態（離散値）に変換
def digitize(observation):

    state = []
    
    state.append(np.digitize(observation[0], bins[0]))
    state.append(np.digitize(observation[1], bins[1]))
    state.append(np.digitize(observation[2], bins[2]))
    state.append(np.digitize(observation[3], bins[3]))
    
    return tuple(state)

# 報酬の取得
def getReward(step, done):

    if done:
        if step >= TARGET_STEP:
            reward = 1 # 目標ステップに到達
        else:
            reward = -200 # ペナルティ
    else:
        reward = 1

    return reward

# Q値の更新
def updateQTable(state, action, next_state, reward):

    max_value = max(getQ(next_state, 0), getQ(next_state, 1))

    value = (1 - alpha) * getQ(state, action) + alpha * (reward + gamma * max_value)

    setQ(state, action, value)


# Q値の設定
def setQ(state, action, value):
    q_table[(state, action)] = value
                     
# Q値の取得
def getQ(state, action):

    if not(state, action) in q_table:
        q_table[(state, action)] = 0

    return q_table[(state, action)]

# εグリーディ手法で行動選択
def greedyAction(state, episode):

    epsilon = MAX_EPSILON - (MAX_EPSILON * (episode / MAX_EPISODE))
    
    if epsilon > np.random.rand():
        action = env.action_space.sample()
    else:
        action = np.argmax([getQ(state, 0), getQ(state, 1)])

    return action

# Qテーブルの読込
if READ_Q_FILE:
    with open(Q_FILE_INPUT, mode="rb") as f:
        q_table = pickle.load(f)

# 環境の初期化
env = gym.make('CartPole-v0')

# 環境の状態確認
print("Action Space: {}".format(env.action_space)) # 行動
print("Env Space: {}".format(env.observation_space)) # 観測データ
print("Env High: {}".format(env.observation_space.high)) # 観測データの最大値
print("Env Low: {}".format(env.observation_space.low)) # 観測データの最小値

for episode in range(MAX_EPISODE):

    print("Episode [{}]".format(episode))
    
    # 環境の初期化
    observation = env.reset()
    
    for step in range(MAX_STEP):

        rgb_array = env.render()

        # フレーム画像の記録
        if episode == (MAX_EPISODE - 1):
            rgb_arrays.append(rgb_array)

        cart_position = observation[0] # カートの位置
        cart_speed = observation[1] # カートの速度
        pole_angle = observation[2] # ポールの角度
        pole_speed = observation[3] # ポールの速度

        # 状態の取得
        state = digitize(observation)
        
        # εグリーディ手法で行動選択
        action = greedyAction(state, episode)

        # 次の状態に遷移
        observation, reward, done, info = env.step(action)

        # 次の状態
        next_state = digitize(observation)        
        
        # 報酬の取得
        reward = getReward(step, done)

        # Q値の更新
        updateQTable(state, action, next_state, reward)
        
        if done:
            histories.append(step + 1)
            print("Finished After {} Steps".format(step + 1))        
            break

# 平均ステップ数の出力
print("Avg. {}".format(np.mean(histories)))
print("Std. {}".format(np.std(histories)))

# Qテーブルの保存
with open(Q_FILE_OUTPUT, mode="wb") as f:
    pickle.dump(q_table, f)

# フレーム画像の保存
shutil.rmtree(IMAGE_DIR) #フォルダの削除
os.mkdir(IMAGE_DIR) #フォルダの作成

for step, rgb_array in enumerate(rgb_arrays):
    cv2.imwrite(IMAGE_DIR + str(step + 1).zfill(3) + ".jpg", rgb_array)

env.close()    
