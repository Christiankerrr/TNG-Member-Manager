import discord
import DB_Manage
from time import time as time_now

signInTimes = {}

class SignInOutView(discord.ui.View):

    def __init__(self, eventName):

        super().__init__(timeout = None)
        self.eventName = eventName

    @discord.ui.button(label = "Sign In", style = discord.ButtonStyle.green)
    async def sign_in_member(self, interaction, button):
        memberID = interaction.user.id
        signInTimes[memberID] = time_now()
        await interaction.response.send_message("Signed in!", ephemeral = True)

    @discord.ui.button(label = "Sign Out", style = discord.ButtonStyle.red)
    async def sign_out_member(self, interaction, button):
        memberID = interaction.user.id
        if memberID in signInTimes:
            durSec = time_now() - signInTimes.pop(memberID)
            newHours = durSec / 3600

            memData = DB_Manage.get_attrs("members", memberID)
            evData = DB_Manage.get_attrs("events", self.eventName)
            attendees = evData.get("attendees", ())

            if isinstance(attendees, str):
                attendees = tuple(
                    map(int, filter(None, attendees.split(',')))  # filter out empty strings
                )

            updatedAttend = attendees + (memberID,)

            DB_Manage.edit_attr("members", memberID, "hours", newHours + memData["hours"])
            DB_Manage.edit_attr("events", self.eventName, "attendees", updatedAttend)

            await interaction.response.send_message(
                f"Signed out! You were signed in for {newHours:.2f} hours.",
                ephemeral=True)
        else:
            await interaction.response.send_message("You haven't signed in yet", ephemeral=True)

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

    await ctx.send(embed=embed, view=SignInOutView(eventName))
