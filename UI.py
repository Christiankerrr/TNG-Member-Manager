import discord
from time import time as time_now

import DB_Manage
import Functions

class VerifySignInView(discord.ui.View):

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

        await self.memberObj.send(
            f"Your sign in request to \"{self.parentUI.eventName}\" was denied. If you believe this was a mistake, DM an executive board member and sign in again.")

        await interaction.message.delete()

class SignInOutView(discord.ui.View):

    def __init__(self, botClient, eventName, startTime):

        super().__init__(timeout = None)

        self.botClient = botClient

        tngServer = botClient.get_guild(botClient.tngServerID)
        self.verifyChannel = discord.utils.get(tngServer.text_channels, name = "sign-in-verify")

        self.originalMsg = None

        self.eventName = eventName
        self.startTime = startTime

        self.pendingApproval = {}
        self.signedInMembers = {}
        self.signedOutMembers = []

    async def close_event(self):

        endTime = time_now()
        eventDur = endTime - self.startTime

        attendees = set()
        for memberID, duration in self.signedOutMembers:

            attendees.add(memberID)

            memberAttrs = DB_Manage.get_attrs("members", memberID)

            DB_Manage.edit_attr("members", memberID, "hours", memberAttrs["hours"] + duration)

        del self.botClient.activeEvents[self.eventName]

        DB_Manage.write_event(
            title = self.eventName,
            isMeeting = 0,
            start = self.startTime,
            end = endTime,
            duration = eventDur,
            attendees = ",".join(str(memberID) for memberID in attendees)
        )

        await self.originalMsg.delete()

    @discord.ui.button(label = "Sign In", style = discord.ButtonStyle.green)
    async def sign_in_member(self, interaction, button):

        memberObj = interaction.user

        if not DB_Manage.locate_member(memberObj.id):

            DB_Manage.write_member(memberObj.id, memberObj.name, memberObj.display_name)

        dietMissing, sizeMissing, cutMissing = DB_Manage.missing_data(memberObj.id)
        await get_info(interaction, dietMissing, sizeMissing, cutMissing)

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

        await self.verifyChannel.send(embed = embed, view = VerifySignInView(self, memberObj))

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

        await interaction.response.send_message(
            f"You have been signed out! You were at \"{self.eventName}\" for {durHours:.2f} hours.",
            ephemeral = True
        )

class SignInView(discord.ui.View):

    def __init__(self, botClient, meetingName, startTime):

        super().__init__(timeout = None)

        self.botClient = botClient

        tngServer = botClient.get_guild(botClient.tngServerID)
        self.verifyChannel = discord.utils.get(tngServer.text_channels, name = "sign-in-verify")

        self.originalMsg = None

        self.meetingName = meetingName
        self.startTime = startTime

        self.pendingApproval = {}
        self.signedInMembers = {}

    async def close_event(self):

        endTime = self.startTime + 60 * 60
        meetingDur = endTime - self.startTime

        attendees = set()
        for memberID in self.signedInMembers.keys():

            attendees.add(memberID)

            memberAttrs = DB_Manage.get_attrs("members", memberID)

            DB_Manage.edit_attr("members", memberID, "meetings", memberAttrs["meetings"] + 1)

        del self.botClient.activeEvents[self.meetingName]

        DB_Manage.write_event(
            title = self.meetingName,
            isMeeting = 1,
            start = self.startTime,
            end = endTime,
            duration = meetingDur,
            attendees = ",".join(str(memberID) for memberID in attendees)
        )

        await self.originalMsg.delete()

    @discord.ui.button(label = "Sign In", style = discord.ButtonStyle.green)
    async def sign_in_member(self, interaction, button):

        memberObj = interaction.user

        if not DB_Manage.locate_member(memberObj.id):

            DB_Manage.write_member(memberObj.id, memberObj.name, memberObj.display_name)

        dietMissing, sizeMissing, cutMissing = DB_Manage.missing_data(memberObj.id)
        await get_info(interaction, dietMissing, sizeMissing, cutMissing)

        if memberObj.id in self.pendingApproval.keys():

            await interaction.response.send_message(
                "We've already recorded your sign-in request! Please DM an executive board member to handle your sign-in request.",
                ephemeral = True
            )

            return

        if memberObj.id in self.signedInMembers.keys():

            await interaction.response.send_message(
                "You're already signed in!",
                ephemeral = True
            )

            return

        self.pendingApproval[memberObj.id] = None

        embed = discord.Embed(
            title = f"{memberObj.display_name} is trying to sign in to the event \"{self.meetingName}\"!",
            color = discord.Color.blue()
        )

        await self.verifyChannel.send(embed = embed, view = VerifySignInView(self, memberObj))

        await interaction.response.send_message(
            "We've recorded your sign-in request! You'll get a DM if it gets confirmed or denied.",
            ephemeral = True
        )

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

    view = SignInOutView(botClient, eventName, startTime)
    view.originalMsg = await ctx.send(embed = embed, view = view)

    return view

async def meeting_card(ctx, botClient, meetingName, startTime):

    embed = discord.Embed(
        title = f"{meetingName} Has Started!",
        color = discord.Color.blue()
    )
    embed.add_field(
        name = "**Meeting Start Time:**",
        value = Functions.secs_to_str(startTime),
        inline = False
    )
    embed.add_field(
        name = "**Need help?**",
        value = "DM the Organizational Director",
        inline = False
    )

    view = SignInView(botClient, meetingName, startTime)
    view.originalMsg = await ctx.send(embed = embed, view = view)

    return view

async def get_info(interaction, dietMissing, sizeMissing, cutMissing):

    if dietMissing:

        pass

    if sizeMissing:

        pass

    if cutMissing:

        pass