import os
import json

import discord

from Cogs import anilist_commands, spoiler

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
bot.remove_command("help")


@bot.event
async def on_ready():
    activity = discord.Game("Unital Ring")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Logged in as", bot.user)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Yuuki Asuna",
        description="Vice-commander of KoB, Lightning Flash, Queen Titania, Berserk Healer, "
                    + "Goddess Stacia, and Kirito's lover.",
         colour=discord.Color.red(),
         url="https://swordartonline.fandom.com/wiki/Yuuki_Asuna"
    )

    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)    
    
    embed.set_image(url="https://cdn.discordapp.com/attachments/694146811560198196/794956119251877898/364.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/694146811560198196/794955939559243816/98.png")
    
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name="help", value=f"My command prefix is `{data['prefix']}`", inline=False)
    embed.add_field(name="mod", value="Displays moderation commands", inline=False)
    embed.add_field(name="search", value="Displays search commands", inline=False)
    await ctx.send(embed=embed)


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

# Add the anilist cog
bot.add_cog(anilist_commands.AniList(bot))
# Add the spoiler cog
bot.add_cog(spoiler.Spoiler.spoiler(bot))
# Start the bot
bot.run(os.getenv("TOKEN"))
