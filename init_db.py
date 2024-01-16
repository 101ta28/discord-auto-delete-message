import os

import psycopg2

# 環境変数からデータベース接続情報を取得
DATABASE_URL = os.getenv("DATABASE_URL")

# データベースに接続
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# テーブルを作成
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS channel_settings (
        channel_id BIGINT PRIMARY KEY,
        guild_id BIGINT,
        remove_minute INT
    );
"""
)
conn.commit()
cur.close()
conn.close()
