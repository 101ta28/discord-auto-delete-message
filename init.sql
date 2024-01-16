CREATE TABLE channel_settings (
    channel_id BIGINT PRIMARY KEY,
    guild_id BIGINT,
    remove_minute INT
);
