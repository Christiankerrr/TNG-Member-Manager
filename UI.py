import discord
from discord.ext import commands

from Commands import bot

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