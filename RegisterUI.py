import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def register(ctx):

    embed = discord.Embed(
        title="Registration For 'Add Variable for events here'",
        color=discord.Color.blue()
    )
    embed.add_field(name="**Meeting Area**", value="Blank", inline=False)
    embed.add_field(name="**Need help?**", value="[Message Blank](https://google.com)", inline=False)

    view = discord.ui.View()
    sign_in = discord.ui.Button(label="Sign in", style=discord.ButtonStyle.link, url="https://google.com")
    sign_out = discord.ui.Button(label="Sign Out", style=discord.ButtonStyle.link,
                                       url="https://google.com")

    view.add_item(sign_in)
    view.add_item(sign_out)

    await ctx.send(embed=embed, view=view)


bot.run(TOKEN)
