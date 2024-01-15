# DiscordAutoDeleteMessage

## Description

DiscordAutoDeleteMessage is a bot for Discord.

It automatically deletes messages posted in a specified channel after a set amount of time (in minutes).

There are two versions: `local.py`, which does not use a database and resets settings upon restart, and `main.py`, which uses PostgreSQL to save settings.

If you want to run it on Railway, you can use the following template:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/QJbiIN?referralCode=wih4oH)

## Environment Setup

### 1. Clone the Repository

```bash
$ git clone https://github.com/101ta28/discord-auto-delete-message.git
$ cd discord-auto-delete-message
```

### 2. Install Packages

It is recommended to create a virtual environment using python-venv.

For WSL2, Ubuntu, you can create a virtual environment with the following commands:

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### 3. Create a .env File

Create a .env file from .env.sample.

Get your DISCORD_BOT_TOKEN from the Discord Developer Portal.

If you are not using a database, proceed to step 5.

### 4. Using a Database

We use PostgreSQL.

```sql
CREATE TABLE channel_settings (
    channel_id BIGINT PRIMARY KEY,
    remove_minute INT
);
```

### 5. Run the Discord Bot

```bash
# If not using a database
$ python local.py

# If using a database
$ python main.py
```
