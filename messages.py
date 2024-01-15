messages = {
    "en": {
        "help_message": (
            "Commands for General Users:\n"
            "/adm help: Display this help message\n"
            "/adm info: Display deletion times for all configured channels\n"
            "\n"
            "Configuration Commands (requires 'Manage Messages' permission):\n"
            "/adm set [channel_name] [remove_minute]: Set a timer to automatically delete messages in a specified channel\n"
            "/adm set [channel_name] stop: Stop the automatic message deletion timer for a specified channel\n"
            "/adm lang [language_code]: Set the bot's response language\n"
            "\n"
            "Admin Commands (requires 'Administrator' permissions):\n"
            "/adm shutdown: Shut down the bot\n"
        ),
        "channel_not_found": "Channel '{}' not found.",
        "message_set": "Messages in '{}' will be replaced after {} minutes.",
        "message_deletion_stopped": "Message deletion stopped for '{}'.",
        "no_channel_settings": "No channels have been configured.",
        "message_replaced": "{}'s message has been deleted.",
        "language_set": "Language set to English.",
        "missing_permissions": "You do not have the required permissions to use this command.",
        "channel_info": "{} channel: Messages will be deleted after {} minutes",
        "unsupported_language": "Unsupported language code or no change in language setting.",
        "invalid_time_setting": "Invalid time setting.",
        "command_not_found": "Command not found.",
        "unexpected_error": "An unexpected error occurred: {}",
        "shutdown_message": "Shutting down the bot.",
    },
    "ja": {
        "help_message": (
            "一般ユーザー向けコマンド:\n"
            "/adm help: このヘルプメッセージを表示\n"
            "/adm info: 設定された全チャンネルの削除時間を表示\n"
            "\n"
            "設定コマンド (「メッセージの管理」権限が必要です):\n"
            "/adm set [channel_name] [remove_minute]: 指定チャンネルでメッセージを自動削除するためのタイマーを設定\n"
            "/adm set [channel_name] stop: 指定チャンネルの自動削除タイマーを停止\n"
            "/adm lang [language_code]: ボットの応答言語を設定\n"
            "\n"
            "管理者向けコマンド (「管理者」権限が必要です):\n"
            "/adm shutdown: ボットをシャットダウンする\n"
        ),
        "channel_not_found": "チャンネル'{}'が見つかりません。",
        "message_set": "{} チャンネルのメッセージは投稿後{}分で削除されます。",
        "message_deletion_stopped": "{}でのメッセージ削除を停止しました。",
        "no_channel_settings": "設定されているチャンネルはありません。",
        "message_replaced": "{}のメッセージは削除されました。",
        "language_set": "言語を日本語に設定しました。",
        "missing_permissions": "このコマンドを使用するための必要な権限がありません。",
        "channel_info": "{} チャンネル: {}分後に削除",
        "unsupported_language": "サポートされていない言語コード、または言語設定の変更がありません。",
        "invalid_time_setting": "無効な時間設定です。",
        "command_not_found": "コマンドが見つかりません。",
        "unexpected_error": "予期せぬエラーが発生しました: {}",
        "shutdown_message": "ボットをシャットダウンします。",
    },
}


def get_message(guild_id, key, lang="ja"):
    # 優先言語でメッセージを試みる
    message = messages.get(lang, {}).get(key)

    # メッセージが見つからない場合、英語で試みる
    if message is None:
        message = messages.get("en", {}).get(key)

    # それでも見つからない場合は空文字列を返す
    return message if message is not None else ""
