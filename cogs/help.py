import math
import discord


from discord.ext import commands
from discord.ui import View, Button

PAGE_COMMANDS = 4


class HelpButtons(View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current = 0

        self.l_button.disabled = True

        if len(embeds) == 1:
            self.r_button.disabled = True

    @discord.ui.button(label="🡸", style=discord.ButtonStyle.success)
    async def l_button(self, interaction: discord.Interaction, button: Button):
        self.current -= 1
        if self.current == 0:
            button.disabled = True
        self.r_button.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label="🡺", style=discord.ButtonStyle.success)
    async def r_button(self, interaction: discord.Interaction, button: Button):
        self.current += 1
        if self.current == len(self.embeds) - 1:
            button.disabled = True
        self.l_button.disabled = False
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_cmd(self, ctx):

        isExec = any(role.name == "Executive Board" for role in ctx.author.roles)

        if isExec:
            visibleCommands = [cmd for cmd in self.bot.commands if not cmd.hidden]
        else:
            visibleCommands = [cmd for cmd in self.bot.commands if not getattr(cmd, "adminOnly", False)]
        
        totalPages = math.ceil(len(visibleCommands) / PAGE_COMMANDS)
        pages = []

        for i in range(totalPages):
            embed = discord.Embed(title=f"Welcome to the {'Executive' if isExec else 'Member'} Help Page -- Page {i + 1}/{totalPages}", color=discord.Color.dark_magenta())
            
            for cmd in visibleCommands[i*PAGE_COMMANDS:(i+1)*PAGE_COMMANDS]:
                cmdInfo = f"{ctx.prefix}{cmd.name} {cmd.signature}".strip()
                embed.add_field(name=cmdInfo, value=cmd.help or "No description provided.", inline=False)
            
            embed.set_footer(text="Use 🡸 and 🡺 to navigate")
            pages.append(embed)

        view = HelpButtons(pages)
        await ctx.send(embed=pages[0], view=view)

async def setup(bot):
    await bot.add_cog(Help(bot))