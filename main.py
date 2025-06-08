import discord
import asyncio
import pytz
from datetime import datetime
import os

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_NAMES = {
    "WIB": None,
    "WITA": None,
    "WIT": None
}

timezones = {
    "WIB": pytz.timezone("Asia/Jakarta"),
    "WITA": pytz.timezone("Asia/Makassar"),
    "WIT": pytz.timezone("Asia/Jayapura")
}

async def update_channels():
    await client.wait_until_ready()
    guild = client.get_guild(GUILD_ID)

    for zone in CHANNEL_NAMES:
        if CHANNEL_NAMES[zone] is None:
            channel = await guild.create_voice_channel(name=f"{zone}: Loading...")
            CHANNEL_NAMES[zone] = channel.id

    while not client.is_closed():
        for zone, tz in timezones.items():
            now = datetime.now(tz)
            formatted = now.strftime("%H:%M")
            channel = guild.get_channel(CHANNEL_NAMES[zone])
            await channel.edit(name=f"{zone}: {formatted}")
        await asyncio.sleep(60)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    client.loop.create_task(update_channels())

client.run(TOKEN)
