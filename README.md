# DiscordAutoDeleteMessage

## 説明

DiscordAutoDeleteMessage は、Discord 用 Bot です。

指定したチャンネルに投稿されたメッセージを、指定した時間が経過したら自動的に削除します。

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

.env.sample から.env ファイルを作成します

### 4. Discord Bot を動かす

```bash
$ python main.py
```
