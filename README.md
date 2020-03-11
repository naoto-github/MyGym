# MyGym

[OpenAI Gym](https://gym.openai.com/)のバランスゲーム(CartPole-v0)をQ学習で解くサンプルプログラムです．

## バランスゲームとは

カートの上に立てたポールを落とさないようにバランスをとるゲームです．  
ユーザは，カートに対し，左右から力を加えるという操作しかできません．

失敗となる条件は下記です．

- ポールが15度以上傾く
- カートが画面から外れる（中央から2.4ユニット以上離れる）

また，失敗せず200ステップ以上が経過すれば **成功** となります．
このサンプルでは，Q学習を利用して，状態-行動の価値を学習しています．

<a href="https://gyazo.com/cd093e2a691a4fd3ecad3499b780bd20"><video alt="Video from Gyazo" width="594" autoplay muted loop playsinline controls><source src="https://i.gyazo.com/cd093e2a691a4fd3ecad3499b780bd20.mp4" type="video/mp4" /></video></a>

**【学習前】**

<a href="https://gyazo.com/629f06dfeb48264f2a876952b1f25546"><video alt="Video from Gyazo" width="598" autoplay muted loop playsinline controls><source src="https://i.gyazo.com/629f06dfeb48264f2a876952b1f25546.mp4" type="video/mp4" /></video></a>

**【学習後】**

## 実行方法

Pythonの3.8.0で実装しています．
最初にOpenAI Gymのライブラリを導入してください．

```
% pip install gym
```

プログラムを実行するには下記のコマンドを入力します．

```
% python balance_game.py
```

オプションを表示するには下記のコマンドを入力します．

```
% python balance_game.py -h
```

利用可能な引数は下記です．

- --reset Reset # Qテーブルの初期化
- --input INPUT # 入力用Qテーブル
- --output OUTPUT # 出力用Qテーブル
- --epsilon EPSILON # 最大ランダム率
- --number NUMBER # 最大エピソード数


