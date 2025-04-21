import discord

class SignInOutView(discord.ui.View):

    def __init__(self):

        super().__init__(timeout = None)

    @discord.ui.button(label = "Sign In", style = discord.ButtonStyle.green)
    async def sign_in_member(self, interaction, button):

        await interaction.response.send_message("Signed in!", ephemeral = True)

    @discord.ui.button(label = "Sign Out", style = discord.ButtonStyle.red)
    async def sign_out_member(self, interaction, button):

        await interaction.response.send_message("Signed out!", ephemeral = True)

async def sign_in_out(ctx, eventName, startTimeStr):

    embed = discord.Embed(
        title = f"{eventName} Has Started!",
        color = discord.Color.blue()
    )
    embed.add_field(
        name = "**Event Start Time:**",
        value = startTimeStr,
        inline = False
    )
    embed.add_field(
        name = "**Need help?**",
        value = "DM the Organizational Director",
        inline = False
    )

    await ctx.send(embed = embed, view = SignInOutView())
