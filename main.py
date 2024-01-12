import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.none()
# MESSAGE CONTENT INTENTを有効化
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# 設定を保持する辞書
channel_settings = {}
language_settings = {}

# メッセージのテンプレート
messages = {
    "en": {
        "help_message": "/adm set [channel_name] [remove_minute]: Replace messages in the specified channel after a certain number of minutes\n/adm help: Display this help message\n/adm info: Display the deletion times for all configured channels",
        "channel_not_found": "Channel '{}' not found.",
        "message_set": "Messages in '{}' will be replaced after {} minutes.",
        "message_deletion_stopped": "Message deletion stopped for '{}'.",
        "no_channel_settings": "No channels have been configured.",
        "message_replaced": "{}'s message has been deleted.",
        "language_set": "Language set to English.",
        "missing_permissions": "You do not have the required permissions to use this command.",
        "channel_info": "{}: Messages will be deleted after {} minutes",
        "unsupported_language": "Unsupported language code or no change in language setting."
    },
    "ja": {
        "help_message": "/adm set [channel_name] [remove_minute]: 指定チャンネルのメッセージを指定分後に置き換える\n/adm help: このヘルプメッセージを表示\n/adm info: 設定された全チャンネルの削除時間を表示",
        "channel_not_found": "チャンネル'{}'が見つかりません。",
        "message_set": "{}のメッセージは投稿後{}分で置き換えられます。",
        "message_deletion_stopped": "{}でのメッセージ削除を停止しました。",
        "no_channel_settings": "設定されているチャンネルはありません。",
        "message_replaced": "{}のメッセージは削除されました。",
        "language_set": "言語を日本語に設定しました。",
        "missing_permissions": "このコマンドを使用するための必要な権限がありません。",
        "channel_info": "{}: {}分後に削除",
        "unsupported_language": "サポートされていない言語コード、または言語設定の変更がありません。"
    }
}

def get_message(guild_id, key):
    lang = language_settings.get(guild_id, "ja")
    return messages[lang][key]

@bot.group(invoke_without_command=True)
async def adm(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.respond(get_message(ctx.guild.id, "help_message"))

@adm.command(name="help")
async def adm_help(ctx):
    await ctx.respond(get_message(ctx.guild.id, "help_message"))

@adm.command(name="set")
@commands.has_permissions(manage_messages=True)
async def adm_set(ctx, channel_name: str, remove_minute: str):
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    if channel:
        if remove_minute.isdigit():
            channel_settings[channel.id] = int(remove_minute)
            await ctx.respond(get_message(ctx.guild.id, "message_set").format(channel_name, remove_minute))
        elif remove_minute.lower() == "stop":
            channel_settings.pop(channel.id, None)
            await ctx.respond(get_message(ctx.guild.id, "message_deletion_stopped").format(channel_name))
    else:
        await ctx.respond(get_message(ctx.guild.id, "channel_not_found").format(channel_name))

@adm.command(name="info")
async def adm_info(ctx):
    if channel_settings:
        info = "\n".join([f"{ctx.guild.get_channel(cid).name}: {min}分後に削除" for cid, min in channel_settings.items()])
        await ctx.respond(get_message(ctx.guild.id, "info").format(info))
    else:
        await ctx.respond(get_message(ctx.guild.id, "no_channel_settings"))

@adm.command(name="lang")
async def adm_lang(ctx, lang_code: str):
    if lang_code in messages and language_settings.get(ctx.guild.id) != lang_code:
        language_settings[ctx.guild.id] = lang_code
        await ctx.respond(get_message(ctx.guild.id, "language_set"))
    else:
        await ctx.respond("Unsupported language code or no change in language setting.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id in channel_settings:
        remove_minute = channel_settings[message.channel.id]

        async def replace_message():
            await asyncio.sleep(remove_minute * 60)
            await message.edit(content=get_message(message.guild.id, "message_replaced").format(message.author.display_name))

        asyncio.create_task(replace_message())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send(get_message(ctx.guild.id, "missing_permissions"))
    else:
        # 他のエラーの処理
        pass

bot.run(DISCORD_BOT_TOKEN)
