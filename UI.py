import discord
from time import time as time_now

import DB_Manage
import Functions

class SignInOutView(discord.ui.View):

    class VerifySignIn(discord.ui.View):

        def __init__(self, parentUI, memberObj):

            super().__init__(timeout = None)

            self.parentUI = parentUI
            self.memberObj = memberObj

        @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
        async def confirm_sign_in(self, interaction, button):

            signInTime = self.parentUI.pendingApproval[self.memberObj.id]
            del self.parentUI.pendingApproval[self.memberObj.id]

            self.parentUI.signedInMembers[self.memberObj.id] = signInTime

            await self.memberObj.send(f"Your sign in request to \"{self.parentUI.eventName}\" was confirmed!")

            await interaction.message.delete()

        @discord.ui.button(label = "Deny", style = discord.ButtonStyle.red)
        async def deny_sign_in(self, interaction, button):

            del self.parentUI.pendingApproval[self.memberObj.id]

            await self.memberObj.send(f"Your sign in request to \"{self.parentUI.eventName}\" was denied. If you believe this was a mistake, DM an executive board member and sign in again.")

            await interaction.message.delete()

    def __init__(self, botClient, eventName, startTime):

        super().__init__(timeout = None)

        self.botClient = botClient

        tngServer = botClient.get_guild(botClient.tngServerID)
        self.verifyChannel = discord.utils.get(tngServer.text_channels, name = "sign-in-verify")

        self.eventName = eventName
        self.startTime = startTime

        self.pendingApproval = {}
        self.signedInMembers = {}
        self.signedOutMembers = []

    async def close_event(self):

        msg = self.botClient.activeEvents[self.eventName]

        await msg.delete()

    @discord.ui.button(label = "Sign In", style = discord.ButtonStyle.green)
    async def sign_in_member(self, interaction, button):

        memberObj = interaction.user

        if memberObj.id in self.pendingApproval.keys():

            await interaction.response.send_message(
                "We've already recorded your sign-in request! Please DM an executive board member to handle your sign-in request.",
                ephemeral = True
            )

            return

        if memberObj.id in self.signedInMembers.keys():

            await interaction.response.send_message(
                "You're already signed in! Please sign out before signing in again.",
                ephemeral = True
            )

            return

        self.pendingApproval[memberObj.id] = time_now()

        embed = discord.Embed(
            title = f"{memberObj.display_name} is trying to sign in to the event \"{self.eventName}\"!",
            color = discord.Color.blue()
        )

        await self.verifyChannel.send(embed = embed, view = self.VerifySignIn(self, memberObj))

        await interaction.response.send_message(
            "We've recorded your sign-in request! You'll get a DM if it gets confirmed or denied.",
            ephemeral = True
        )

    @discord.ui.button(label = "Sign Out", style = discord.ButtonStyle.red)
    async def sign_out_member(self, interaction, button):

        memberObj = interaction.user

        if memberObj.id in self.pendingApproval.keys():

            await interaction.response.send_message(
                "Your sign-in request has not been approved yet! Please DM an executive board member to handle your sign-in request before signing out.",
                ephemeral = True
            )

            return

        if memberObj.id not in self.signedInMembers.keys():

            await interaction.response.send_message(
                "You are not signed in! Please sign in before signing out.",
                ephemeral = True
            )

            return

        signInTime = self.signedInMembers[memberObj.id]
        del self.signedInMembers[memberObj.id]

        durSecs = time_now() - signInTime
        durHours = durSecs/(60 * 60)

        self.signedOutMembers.append((memberObj.id, durHours))

        print(str(self.signedOutMembers))

        await interaction.response.send_message(
            f"You have been signed out! You were at \"{self.eventName}\" for {durHours:.2f} hours.",
            ephemeral = True
        )

        # memberID = interaction.user.id
        # if memberID in signInTimes:
        #     durSec = time_now() - signInTimes.pop(memberID)
        #     newHours = durSec / 3600
        #
        #     memData = DB_Manage.get_attrs("members", memberID)
        #     evData = DB_Manage.get_attrs("events", self.eventName)
        #     attendees = evData.get("attendees", ())
        #
        #     if isinstance(attendees, str):
        #         attendees = tuple(
        #             map(int, filter(None, attendees.split(',')))  # filter out empty strings
        #         )
        #
        #     updatedAttend = attendees + (memberID,)
        #
        #     DB_Manage.edit_attr("members", memberID, "hours", newHours + memData["hours"])
        #     DB_Manage.edit_attr("events", self.eventName, "attendees", updatedAttend)
        #
        #     await interaction.response.send_message(
        #         f"Signed out! You were signed in for {newHours:.2f} hours.",
        #         ephemeral=True)
        # else:
        #     await interaction.response.send_message("You haven't signed in yet", ephemeral=True)

async def event_card(ctx, botClient, eventName, startTime):

    embed = discord.Embed(
        title = f"{eventName} Has Started!",
        color = discord.Color.blue()
    )
    embed.add_field(
        name = "**Event Start Time:**",
        value = Functions.secs_to_str(startTime),
        inline = False
    )
    embed.add_field(
        name = "**Need help?**",
        value = "DM the Organizational Director",
        inline = False
    )

    return await ctx.send(embed = embed, view = SignInOutView(botClient, eventName, startTime))
