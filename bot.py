import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"logged in as {client.user}")


@tree.command(name="ping", description="check if seed is alive")
async def ping(interaction: discord.Interaction):
    ms = round(client.latency * 1000)
    await interaction.response.send_message(f"pong {ms}ms")


if not TOKEN:
    print("no DISCORD_TOKEN in .env")
else:
    client.run(TOKEN)
