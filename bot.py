import json
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


@tree.command(name="backup", description="save this server's roles and channels")
async def backup(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("use this in a server")
        return

    data = {"name": guild.name, "roles": [], "categories": [], "channels": []}

    for role in guild.roles:
        if role.is_default() or role.managed:
            continue
        data["roles"].append({
            "name": role.name,
            "color": role.color.value,
            "hoist": role.hoist,
            "mentionable": role.mentionable,
            "position": role.position,
        })

    for cat in guild.categories:
        data["categories"].append({"name": cat.name, "position": cat.position})

    for ch in guild.channels:
        if isinstance(ch, discord.CategoryChannel):
            continue
        data["channels"].append({
            "name": ch.name,
            "type": str(ch.type),
            "category": ch.category.name if ch.category else None,
            "position": ch.position,
        })

    os.makedirs("backups", exist_ok=True)
    path = f"backups/{guild.id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    await interaction.response.send_message(
        f"saved {len(data['roles'])} roles, {len(data['channels'])} channels",
        file=discord.File(path),
    )


if not TOKEN:
    print("no DISCORD_TOKEN in .env")
else:
    client.run(TOKEN)
