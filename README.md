# DiscordAutoDeleteMessage

## 説明

DiscordAutoDeleteMessage は、Discord 用 Bot です。

指定したチャンネルに投稿されたメッセージを、指定した時間(分)が経過したら自動的に削除します。

データベースを用いず、再起動すると設定がリセットされる `local.py` と、PostgresSQLを用いて設定を保存する `main.py` があります。

## 環境構築

### 1. リポジトリをクローン

```bash
$ git clone https://github.com/101ta28/discord-auto-delete-message.git
$ cd discord-auto-delete-message
```

### 2. パッケージをインストール

python-venv を使って仮想環境を作成することをおすすめします。

WSL2, Ubuntu の場合は、以下のコマンドで仮想環境を作成できます。

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### 3. .env ファイルを作成

.env.sample から.env ファイルを作成します。

DISCORD_BOT_TOKENは、Discord Developer Portal から取得してください。

データベースを用いない場合、手順5に進んでください。

### 4. データベースを用いる

PostgresSQL を用いています。

```sql
CREATE TABLE channel_settings (
    channel_id BIGINT PRIMARY KEY,
    remove_minute INT
);
```

### 5. Discord Bot を動かす

```bash
# データベースを用いない場合
$ python local.py

# データベースを用いる場合
$ python main.py
```
