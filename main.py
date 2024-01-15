import asyncio
import os

import discord
import psycopg2
import psycopg2.pool
from discord.ext import commands
from dotenv import load_dotenv

from messages import get_message

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
# コネクションプールの設定
DB_CONNECTION_POOL = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

# 設定を保持する辞書
channel_settings = {}
language_settings = {}


# チャンネル設定を読み込む
def load_channel_settings(guild_id):
    conn = DB_CONNECTION_POOL.getconn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT channel_id, remove_minute FROM channel_settings WHERE guild_id = %s",
            (guild_id,),
        )
        result = {}
        for channel_id, remove_minute in cur.fetchall():
            result[channel_id] = remove_minute
        return result
    except Exception as e:
        print(f"Error loading channel settings: {e}")
        return {}
    finally:
        cur.close()
        DB_CONNECTION_POOL.putconn(conn)


# チャンネル設定を取得する
def get_channel_settings(channel_id):
    conn = DB_CONNECTION_POOL.getconn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT remove_minute FROM channel_settings WHERE channel_id = %s",
            (channel_id,),
        )
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error getting channel settings for channel {channel_id}: {e}")
        return None
    finally:
        cur.close()
        DB_CONNECTION_POOL.putconn(conn)


# チャンネル設定を保存する
def set_channel_settings(guild_id, channel_id, remove_minute):
    conn = DB_CONNECTION_POOL.getconn()
    try:
        cur = conn.cursor()
        # 既存のレコードが存在するか確認
        cur.execute(
            "SELECT 1 FROM channel_settings WHERE guild_id = %s AND channel_id = %s",
            (guild_id, channel_id),
        )
        exists = cur.fetchone()

        # 既存のレコードがある場合は更新、なければ挿入
        if exists:
            cur.execute(
                "UPDATE channel_settings SET remove_minute = %s WHERE guild_id = %s AND channel_id = %s",
                (remove_minute, guild_id, channel_id),
            )
        else:
            cur.execute(
                "INSERT INTO channel_settings (guild_id, channel_id, remove_minute) VALUES (%s, %s, %s)",
                (guild_id, channel_id, remove_minute),
            )
        conn.commit()
    except Exception as e:
        print(f"Error setting channel settings: {e}")
        conn.rollback()
    finally:
        cur.close()
        DB_CONNECTION_POOL.putconn(conn)


# チャンネル設定を削除する
def remove_channel_settings(guild_id, channel_id):
    conn = DB_CONNECTION_POOL.getconn()
    try:
        cur = conn.cursor()
        cur.execute
        (
            "DELETE FROM channel_settings WHERE guild_id = %s AND channel_id = %s",
            (guild_id, channel_id),
        )
        conn.commit()
    except Exception as e:
        print(f"Error removing channel settings: {e}")
    finally:
        cur.close()
        DB_CONNECTION_POOL.putconn(conn)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.group(invoke_without_command=True)
async def adm(ctx):
    lang = language_settings.get(ctx.guild.id, "ja")
    if ctx.invoked_subcommand is None:
        await ctx.send(get_message(ctx.guild.id, "help_message", lang))


@adm.command(name="help")
async def adm_help(ctx):
    lang = language_settings.get(ctx.guild.id, "ja")
    await ctx.send(get_message(ctx.guild.id, "help_message", lang))


@adm.command(name="set")
@commands.has_permissions(manage_messages=True)
async def adm_set(ctx, channel_name: str, remove_minute: str):
    lang = language_settings.get(ctx.guild.id, "ja")
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        if remove_minute.isdigit() and 1 <= int(remove_minute) <= 1440:
            set_channel_settings(ctx.guild.id, channel.id, int(remove_minute))
            await ctx.send(
                get_message(ctx.guild.id, "message_set", lang).format(
                    channel_name, remove_minute
                )
            )
        elif remove_minute.lower() == "stop":
            remove_channel_settings(channel.id)
            await ctx.send(
                get_message(
                    ctx.guild.id, "message_deletion_stopped", lang
                ).format(channel_name)
            )
        else:
            await ctx.send(
                get_message(ctx.guild.id, "invalid_time_setting", lang)
            )
    else:
        await ctx.send(
            get_message(ctx.guild.id, "channel_not_found", lang).format(
                channel_name
            )
        )

# TODO: プライベートチャンネルを表示させない
@adm.command(name="info")
async def adm_info(ctx):
    lang = language_settings.get(ctx.guild.id, "ja")
    channel_settings = load_channel_settings(ctx.guild.id)
    info_lines = []
    for cid, remove_minute in channel_settings.items():
        channel = ctx.guild.get_channel(cid)
        channel_name = channel.name if channel else "Unknown Channel"
        info_line = get_message(ctx.guild.id, "channel_info", lang).format(
            channel_name, remove_minute
        )
        info_lines.append(info_line)

    info = "\n".join(info_lines)
    if info:
        await ctx.send(info)
    else:
        await ctx.send(get_message(ctx.guild.id, "no_channel_settings", lang))


@adm.command(name="lang")
@commands.has_permissions(manage_messages=True)
async def adm_lang(ctx, lang_code: str):
    if lang_code in ["en", "ja"]:
        language_settings[ctx.guild.id] = lang_code
        await ctx.send(get_message(ctx.guild.id, "language_set", lang_code))
    else:
        await ctx.send(
            get_message(ctx.guild.id, "unsupported_language", lang_code)
        )


@adm.command(name="shutdown")
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    """シャットダウンコマンド"""
    lang = language_settings.get(ctx.guild.id, "ja")
    await ctx.send(get_message(ctx.guild.id, "shutdown_message", lang))
    await bot.close()
    DB_CONNECTION_POOL.closeall()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot or message.content.startswith(bot.command_prefix):
        return

    guild_id = message.guild.id
    channel_settings = load_channel_settings(guild_id)

    if message.channel.id in channel_settings:
        lang = language_settings.get(guild_id, "ja")
        remove_minute = channel_settings[message.channel.id]

        # 添付ファイルをダウンロード
        attachments = message.attachments
        files = [await attachment.to_file() for attachment in attachments]

        # ユーザー名とメッセージの内容を組み合わせて再投稿
        copied_message_content = (
            f"**{message.author.display_name}:**\n{message.content}"
        )

        # 再投稿する
        copied_message = await message.channel.send(
            content=copied_message_content, files=files
        )

        # オリジナルメッセージは削除
        await message.delete()

        # メッセージを削除するタスクを作成
        async def delete_copied_message():
            try:
                await asyncio.sleep(remove_minute * 60)
                # メッセージを編集して添付ファイルや画像を削除
                await copied_message.edit(
                    content=get_message(
                        message.guild.id, "message_replaced", lang
                    ).format(message.author.display_name),
                    attachments=[],  # 添付ファイルを削除
                    embeds=[],  # 埋め込みを削除
                )
            except Exception as e:
                print(f"Error in delete_copied_message: {e}")

        asyncio.create_task(delete_copied_message())


@bot.event
async def on_command_error(ctx, error):
    lang = language_settings.get(ctx.guild.id, "ja")
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send(get_message(ctx.guild.id, "missing_permissions", lang))
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(get_message(ctx.guild.id, "command_not_found", lang))
    else:
        error_message = get_message(
            ctx.guild.id, "unexpected_error", lang
        ).format(error)
        await ctx.send(error_message)


bot.run(DISCORD_BOT_TOKEN)
