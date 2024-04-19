# whoo

![](https://img.shields.io/github/stars/v1x4y/whoo.svg) ![](https://img.shields.io/github/forks/v1x4y/whoo.svg) ![](https://img.shields.io/github/tag/v1x4y/whoo.svg) ![](https://img.shields.io/github/release/v1x4y/whoo.svg) ![](https://img.shields.io/github/issues/v1x4y/whoo.svg) ![](https://img.shields.io/bower/v/whoo.svg)

[whoo](https://www.wh00.ooo)のアカウントを操作します。

[Web版(beta)はこちら](https://x-4.jp/tools/whoo)


## 一覧
> - 未認証
>   - アカウント作成
>   - ログイン
> - 認証
>   - 基本操作
>     - メッセージを送信
>     - スタンプを送信
>     - 位置情報を更新
>     - 友達申請
>       - 送信
>       - 取消
>   - 情報取得
>     - ログイン中のアカウント情報を取得
>     - ユーザー情報を取得
>     - 友達リストを取得
>     - 友達申請リストを取得
>     - 友達の位置情報を取得
>   - システム操作
>     - アカウント
>       - 更新
>       - 削除
>     - ステータスを変更
>       - オンライン
>       - オフライン
>     - ユーザーに位置情報を更新させる



## 使い方
### 未認証
```py
import whoo

client=whoo.Client()
# ログイン
data=client.email_login(
    email="example@example.com", # メールアドレス
    password="password" # パスワード
)

# アカウント作成
data=client.create_account(
    email="example@example.com", # メールアドレス
    password="password", # パスワード
    name="example", # 表示名
    username="example", # ユーザー名(ID)
    profile_image="https://example.com/image.png", # アイコンの画像URL
    location={"latitude":37.7877389,"longitude":136.3752183} # 位置情報を指定位置で偽造させる(option | type: dict | default: None)
)
```
### 認証(token)
```py
import whoo
client=whoo.Client(
    token="your token" # トークン
)
```
### 認証(email/password)
```py
import whoo
client=whoo.Client(
    email="example@example.com", # メールアドレス
    password="password" # パスワード
)
```

### 基本操作
```py
# client=whoo.Client(...)

# メッセージを送信
client.send_message(
    room_id="room id", # ルームID
    content="hello world" # 送信内容
)

# スタンプを送信
client.send_stamp(
    user_id="user id", # ユーザーID
    stamp_id="stamp id", # スタンプID
    quantity=1 # スタンプの送信数
)

# 位置情報を更新
client.update_location(
    location={ # 座標
        "latitude":37.7877389, # 緯度
        "longitude":136.3752183 # 経度
    },
    level=100, # バッテリー残量(%)(option | type: int | default: None)
    state=0, # 充電ステータス 通常: 0 充電: 1(option | type: int | default: None)
    speed=0.0, # 移動速度(km/h)(option | type: float | default: None)
    stayed_at="2024-04-1 00:00:00 +0900", # 滞在開始時間(option | type: datetime | default: None)
    horizontal_accuracy=1.0 # 高度(m)(option | type: float | default: None)
)

# 友達申請を送る
client.request_friend(
    user_id="user id" # ユーザーID
)

# 友達申請を取り消す
client.delete_requested(
    user_id="user id" # ユーザーID
)
```
### 情報取得
```py
# client=whoo.Client(...)

# アカウント情報を取得
data=client.info()

# ユーザー情報を取得
data=client.get_user(
    user_id="user id", # ユーザーID
    friends=True # 対象ユーザーの友達リストを同時に取得するかどうか(option | type: bool | default: False)
)

# 友達リストを取得
data=client.get_friends()

# 友達申請リストを取得
data=client.get_requested()

# 友達の位置情報を取得
data=client.get_locations(
    user_id="user id" # ユーザーを指定しない場合は友達全員の位置情報を返す(option | type: str | default: None)
)
```
### システム操作
```py
# client=whoo.Client(...)

# アカウント情報を更新
data=client.update_account(
    name="example", # 表示名
    profile_image="https://example.com/image.png", # アイコンの画像URL
    username="example" # ユーザー名(ID)
)

# アカウントを削除
client.delete_account(
    alert=True # 確認アラートを出すかどうか(option | type: bool | default: True)
)

# ステータスをオンラインに変更
client.online()

# ステータスをオフラインに変更 
client.offline()

# ユーザーに位置情報を更新させる(不安定)
client.reacquire_location(
    user_id="user id" # ユーザーID
)
```
