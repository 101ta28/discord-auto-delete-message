import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from messages import get_message

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# 設定を保持する辞書
channel_settings = {}
language_settings = {}

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


def set_channel_settings(channel_id, remove_minute):
    channel_settings[channel_id] = remove_minute


def remove_channel_settings(channel_id):
    channel_settings.pop(channel_id, None)


def get_channel_settings(channel_id):
    return channel_settings.get(channel_id)


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
            set_channel_settings(channel.id, int(remove_minute))
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


@adm.command(name="info")
async def adm_info(ctx):
    lang = language_settings.get(ctx.guild.id, "ja")
    info_lines = []
    for cid in channel_settings:
        channel_name = (
            ctx.guild.get_channel(cid).name
            if ctx.guild.get_channel(cid)
            else "Unknown Channel"
        )
        remove_minute = get_channel_settings(cid)
        if remove_minute is not None:
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


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author.bot or message.content.startswith(bot.command_prefix):
        return
    if message.channel.id in channel_settings:
        lang = language_settings.get(message.guild.id, "ja")
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

        async def delete_copied_message():
            try:
                await asyncio.sleep(remove_minute * 60)
                await copied_message.edit(
                    content=get_message(
                        message.guild.id, "message_deletion_stopped", lang
                    ).format(message.channel.name)
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
