import os
import json

import discord

from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_any_role

load_dotenv()

# Load variables
if os.getenv("TESTING"):
    # If we're on testing, read testing.json
    # This file is gitignored, so it can have channel IDs and stuff from testing servers
    data_file = "testing.json"
else:
    # Otherwise read data.json
    data_file = "data.json"


with open(data_file, "r") as f:
    data = json.loads(f.read())

bot = commands.Bot(command_prefix=commands.when_mentioned_or(data["prefix"]))


@bot.event
async def on_ready():
    print("Logged in as", bot.user)


@bot.command()
@has_any_role(*data["say_whitelist"])
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)


@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingAnyRole):
        await ctx.send("no u")


if not os.getenv("TESTING"):
    # Start webserver for uptime robot to ping
    import keep_alive
    keep_alive.keep_alive()

# Start the bot
bot.run(os.getenv("TOKEN"))
