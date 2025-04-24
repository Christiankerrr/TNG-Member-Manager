import discord
import DB_Manage
import time
from discord.ext import commands
from Member import Member

user_responses = {}


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Click Here!", style=discord.ButtonStyle.success)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(
                title="📝 Survey: Shirt Cut",
                description="Please select your preferred shirt cut:",
                color=discord.Color.blurple()
            )
            await interaction.user.send(embed=embed, view=ShirtCutView())
            await interaction.response.send_message("📬 Check your DMs!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("DM's are off for this user", ephemeral=True)



class ShirtCutView(discord.ui.View):
    @discord.ui.button(label="Women's", style=discord.ButtonStyle.primary)
    async def women(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)  # store as string
        user_responses[key] = {"cut": "Women's"}
        await interaction.response.send_message("You selected: Women's", ephemeral=True)
        await send_shirt_size(interaction)

    @discord.ui.button(label="Men's", style=discord.ButtonStyle.primary)
    async def mens(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses[key] = {"cut": "Men's"}
        await interaction.response.send_message("You selected: Men's", ephemeral=True)
        await send_shirt_size(interaction)

class ShirtSizeView(discord.ui.View):
    @discord.ui.button(label="XS", style=discord.ButtonStyle.secondary)
    async def size_xs(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "XS"
        await interaction.response.send_message("You selected: Size XS", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="S", style=discord.ButtonStyle.secondary)
    async def size_s(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "S"
        await interaction.response.send_message("You selected: Size S", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="M", style=discord.ButtonStyle.secondary)
    async def size_m(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "M"
        await interaction.response.send_message("You selected: Size M", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="L", style=discord.ButtonStyle.secondary)
    async def size_l(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "L"
        await interaction.response.send_message("You selected: Size L", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="XL", style=discord.ButtonStyle.secondary)
    async def size_xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "XL"
        await interaction.response.send_message("You selected: Size XL", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="2XL", style=discord.ButtonStyle.secondary)
    async def size_2xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "2XL"
        await interaction.response.send_message("You selected: Size 2XL", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="3XL", style=discord.ButtonStyle.secondary)
    async def size_3xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["size"] = "3XL"
        await interaction.response.send_message("You selected: Size 3XL", ephemeral=True)
        await send_diet(interaction)

class DietView(discord.ui.View):
    @discord.ui.button(label="Vegetarian", style=discord.ButtonStyle.success)
    async def vegetarian(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Vegetarian" not in diet_list:
            diet_list.append("Vegetarian")
            await interaction.response.send_message("✅ Added: Vegetarian", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Vegetarian.", ephemeral=True)

    @discord.ui.button(label="Vegan", style=discord.ButtonStyle.success)
    async def vegan(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Vegan" not in diet_list:
            diet_list.append("Vegan")
            await interaction.response.send_message("✅ Added: Vegan", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Vegan.", ephemeral=True)

    @discord.ui.button(label="Kosher", style=discord.ButtonStyle.success)
    async def kosher(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Kosher" not in diet_list:
            diet_list.append("Kosher")
            await interaction.response.send_message("✅ Added: Kosher", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Kosher.", ephemeral=True)

    @discord.ui.button(label="Gluten-Free", style=discord.ButtonStyle.success)
    async def gluten_free(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Gluten-Free" not in diet_list:
            diet_list.append("Gluten-Free")
            await interaction.response.send_message("✅ Added: Gluten-Free", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Gluten-Free.", ephemeral=True)

    @discord.ui.button(label="Dairy-Free", style=discord.ButtonStyle.success)
    async def dairy_free(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Dairy-Free" not in diet_list:
            diet_list.append("Dairy-Free")
            await interaction.response.send_message("✅ Added: Dairy-Free", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Dairy-Free.", ephemeral=True)

    @discord.ui.button(label="Allergies", style=discord.ButtonStyle.success)
    async def allergies(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Allergies" not in diet_list:
            diet_list.append("Allergies")
            await interaction.response.send_message("✅ Added: Allergies\n📩 Please contact a Mod.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Allergies.", ephemeral=True)

    @discord.ui.button(label="Other", style=discord.ButtonStyle.success)
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "Other" not in diet_list:
            diet_list.append("Other")
            await interaction.response.send_message("✅ Added: Other\n📩 Please contact a Mod.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Other.", ephemeral=True)

    @discord.ui.button(label="None", style=discord.ButtonStyle.danger)
    async def none(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet_list = user_responses.setdefault(key, {}).setdefault("diet", [])
        if "None" not in diet_list:
            diet_list.append("None")
            await interaction.response.send_message("✅ Added: None", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected None.", ephemeral=True)

    @discord.ui.button(label="🗑️ Clear All", style=discord.ButtonStyle.secondary)
    async def clear_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        user_responses.setdefault(key, {})["diet"] = []
        await interaction.response.send_message("Cleared all dietary selections.", ephemeral=True)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = str(interaction.user.id)
        diet = user_responses.get(key, {}).get("diet", [])
        if not diet:
            await interaction.response.send_message("⚠️ You haven't selected any dietary preferences yet.", ephemeral=True)
            return
        await interaction.response.send_message("Submitting your dietary preferences...", ephemeral=True)
        await finish_survey(interaction)


async def send_shirt_size(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👕 Shirt Size",
        description="Please select your shirt size:",
        color=discord.Color.blurple()
    )
    await interaction.channel.send(embed=embed, view=ShirtSizeView())


async def send_diet(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🥗 Dietary Preference",
        description="Do you have any dietary restrictions?",
        color=discord.Color.blurple()
    )
    await interaction.channel.send(embed=embed, view=DietView())


async def finish_survey(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    data = user_responses.get(user_id, {})
    print("user_responses for", user_id, ":", data)
    cut = data.get("cut", None)
    size = data.get("size", None)
    diet_list = data.get("diet", [])
    diet_display = ", ".join(diet_list) if isinstance(diet_list, list) else diet_list

    print("Survey values - Cut:", cut, "Size:", size, "Diet:", diet_display)

    if cut:
        DB_Manage.edit_attr("member", user_id, "cut", cut)
    if size:
        DB_Manage.edit_attr("member", user_id, "sze", size)
    if diet_display:
        DB_Manage.edit_attr("member", user_id, "diet", diet_display)

    summary = (
        f"🧾 **Survey Complete!**\n"
        f"• User ID: `{user_id}`\n"
        f"• Shirt Cut: `{cut or 'none'}`\n"
        f"• Shirt Size: `{size or 'none'}`\n"
        f"• Dietary: `{diet_display or 'none'}`"
    )
    await interaction.channel.send(summary)


sign_in_times = {}

class RegisterView(discord.ui.View):
    def __init__(self, event_name: str, timeout: float = 3600):
        super().__init__(timeout=timeout)
        self.event_name = event_name

    @discord.ui.button(label="Sign In", style=discord.ButtonStyle.success)
    async def sign_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        try:
            DB_Manage.add_attend(self.event_name, user_id)
            await interaction.response.send_message(
                f"You’ve signed into **{self.event_name}**",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"{e}", ephemeral=True)


    @discord.ui.button(label="Sign Out", style=discord.ButtonStyle.danger)
    async def sign_out(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        if user_id in sign_in_times:
            sign_in_time = sign_in_times.pop(user_id)
            sign_out_time = time.time()
            duration_seconds = sign_out_time - sign_in_time
            duration_minutes = int(duration_seconds / 60)
            DB_Manage.update_hours(user_id, duration_minutes)
            await interaction.response.send_message(
                f"You've signed out. Recorded duration: {duration_minutes} minute(s).",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You haven't signed in yet.", ephemeral=True
            )
class MemberView(discord.ui.View):
    def __init__(self, timeout: float = None):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Sign Up", style=discord.ButtonStyle.primary)
    async def become_member(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        discord_id = str(user.id)
        discord_tag = f"{user.name}#{user.discriminator}"
        display_name = user.display_name
        DB_Manage.write_member(discord_id, discord_tag, display_name)

        await interaction.response.send_message(
            f"You are now registered as a member!\nID: {discord_id}\nUsername: {discord_tag}\nDisplay Name: {display_name}",
            ephemeral=True
        )
class AttendView(discord.ui.View):
    def __init__(self, event_name: str, timeout: float = None):
        super().__init__(timeout=timeout)
        self.event_name = event_name

    @discord.ui.button(label="Attend", style=discord.ButtonStyle.success)
    async def attend(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        try:
            DB_Manage.add_attend(self.event_name, user_id)
            await interaction.response.send_message(
                f"You’re now registered for **{self.event_name}**",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"{e}", ephemeral=True)


