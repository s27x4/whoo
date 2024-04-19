# whoo

![](https://img.shields.io/github/stars/v1x4y/whoo.svg) ![](https://img.shields.io/github/forks/v1x4y/whoo.svg) ![](https://img.shields.io/github/tag/v1x4y/whoo.svg) ![](https://img.shields.io/github/release/v1x4y/whoo.svg) ![](https://img.shields.io/github/issues/v1x4y/whoo.svg) ![](https://img.shields.io/bower/v/whoo.svg)

[whoo](https://www.wh00.ooo)のアカウントを操作します。

- アカウントの基本操作
- 情報改竄

## Features

- web版

## Installation

```sh
pip install ...
```


## How to use

```py
import whoo
client = whoo.Client()

# login
data=client.email_login(
    email="example@example.com",
    password="password"
    )
print(data)
# >>> account data

# create account
data=client.create_account(
    email="example@example.com",
    password="password",
    name="example",
    username="example",
    profile_image="https://example.com/image.png",
    location={"latitude":35.681236,"longitude":139.767125} #option
    )
print(data)
# >>> account data
```
