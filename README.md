# whoo

![](https://img.shields.io/github/stars/v1x4y/whoo.svg) ![](https://img.shields.io/github/forks/v1x4y/whoo.svg) ![](https://img.shields.io/github/tag/v1x4y/whoo.svg) ![](https://img.shields.io/github/release/v1x4y/whoo.svg) ![](https://img.shields.io/github/issues/v1x4y/whoo.svg) ![](https://img.shields.io/bower/v/whoo.svg)

[whoo](https://www.wh00.ooo)のアカウントを操作します。

- アカウントの基本操作
- 情報改竄

## 使い方
### 未認証
```py
import whoo

client=whoo.Client()
# ログイン
data=client.email_login(
    email="example@example.com",
    password="password"
    )
print(data)
# >>> アカウントデータ

# アカウント作成
data=client.create_account(
    email="example@example.com",
    password="password",
    name="example",
    username="example",
    profile_image="https://example.com/image.png",
    location={"latitude":37.7877389,"longitude":136.3752183} #option
    )
print(data)
# >>> アカウントデータ
```
### 認証(token)
```py
import whoo
client=whoo.Client(
    token="your token"
    )
```
### 認証(email/password)
```py
import whoo
client=whoo.Client(
    email="example@example.com",
    password="password"
    )
```

### 基本操作
```py
# client=whoo.Client(...)

# メッセージを送信
client.send_message(
    room_id="room id",
    content="hello world"
)

# スタンプを送信
client.send_stamp(
    user_id="user id",
    stamp_id="stamp id",
    quantity=1
)

# 友達申請を送る
client.request_friend(
    id="user id"
)

# 友達申請を取り消す
client.delete_requested(
    id="user id"
)
```
```py
# client=whoo.Client(...)

# アカウントデータの更新
data=client.update_account(
    name="example",
    profile_image="https://example.com/image.png",
    username="example"
    )
print(data)
# >>> アカウントデータ

# アカウントを削除
client.delete_account(
    alert=True #確認アラートを出すかどうか(option | type: bool | default: True)
)

# アカウント情報
data=client.account_info()
print(data)
# >>> アカウント情報

# ステータスをオンラインに変更
client.online()

# ステータスをオフラインに変更 
client.offline()
```

