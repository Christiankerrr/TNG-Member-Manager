import discord
#use this array to call information about what people select and the user ID that selected it
user_responses = {}

class ShirtCutView(discord.ui.View):
    @discord.ui.button(label="Women's", style=discord.ButtonStyle.primary)
    async def Women(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id] = {"cut": "Women's"}
        await interaction.response.send_message("You selected: Women's", ephemeral=True)
        await send_shirt_size(interaction)

    @discord.ui.button(label="Men's", style=discord.ButtonStyle.primary)
    async def Men(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id] = {"cut": "Men's"}
        await interaction.response.send_message("You selected: Men's", ephemeral=True)
        await send_shirt_size(interaction)

class ShirtSizeView(discord.ui.View):
    @discord.ui.button(label="XS", style=discord.ButtonStyle.secondary)
    async def size_xs(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "XS"
        await interaction.response.send_message("You selected: Size XS", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="S", style=discord.ButtonStyle.secondary)
    async def size_s(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "S"
        await interaction.response.send_message("You selected: Size S", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="M", style=discord.ButtonStyle.secondary)
    async def size_m(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "M"
        await interaction.response.send_message("You selected: Size M", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="L", style=discord.ButtonStyle.secondary)
    async def size_l(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "L"
        await interaction.response.send_message("You selected: Size L", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="XL", style=discord.ButtonStyle.secondary)
    async def size_xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "XL"
        await interaction.response.send_message("You selected: Size XL", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="2XL", style=discord.ButtonStyle.secondary)
    async def size_2xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "2XL"
        await interaction.response.send_message("You selected: Size 2XL", ephemeral=True)
        await send_diet(interaction)

    @discord.ui.button(label="3XL", style=discord.ButtonStyle.secondary)
    async def size_3xl(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_responses[interaction.user.id]["size"] = "3XL"
        await interaction.response.send_message("You selected: Size 3XL", ephemeral=True)
        await send_diet(interaction)

class DietView(discord.ui.View):
    @discord.ui.button(label="Vegetarian", style=discord.ButtonStyle.success)
    async def vegetarian(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Vegetarian" not in diet_list:
            diet_list.append("Vegetarian")
            await interaction.response.send_message("✅ Added: Vegetarian", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Vegetarian.", ephemeral=True)

    @discord.ui.button(label="Vegan", style=discord.ButtonStyle.success)
    async def vegan(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Vegan" not in diet_list:
            diet_list.append("Vegan")
            await interaction.response.send_message("✅ Added: Vegan", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Vegan.", ephemeral=True)

    @discord.ui.button(label="Kosher", style=discord.ButtonStyle.success)
    async def kosher(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Kosher" not in diet_list:
            diet_list.append("Kosher")
            await interaction.response.send_message("✅ Added: Kosher", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Kosher.", ephemeral=True)

    @discord.ui.button(label="Gluten-Free", style=discord.ButtonStyle.success)
    async def gluten_free(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Gluten-Free" not in diet_list:
            diet_list.append("Gluten-Free")
            await interaction.response.send_message("✅ Added: Gluten-Free", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Gluten-Free.", ephemeral=True)

    @discord.ui.button(label="Dairy-Free", style=discord.ButtonStyle.success)
    async def dairy_free(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Dairy-Free" not in diet_list:
            diet_list.append("Dairy-Free")
            await interaction.response.send_message("✅ Added: Dairy-Free", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Dairy-Free.", ephemeral=True)

    @discord.ui.button(label="Allergies", style=discord.ButtonStyle.success)
    async def allergies(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Allergies" not in diet_list:
            diet_list.append("Allergies")
            await interaction.response.send_message("✅ Added: Allergies\n📩 Please contact a Mod.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Allergies.", ephemeral=True)

    @discord.ui.button(label="Other", style=discord.ButtonStyle.success)
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "Other" not in diet_list:
            diet_list.append("Other")
            await interaction.response.send_message("✅ Added: Other\n📩 Please contact a Mod.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected Other.", ephemeral=True)

    @discord.ui.button(label="None", style=discord.ButtonStyle.danger)
    async def none(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet_list = user_responses.setdefault(user_id, {}).setdefault("diet", [])
        if "None" not in diet_list:
            diet_list.append("None")
            await interaction.response.send_message("✅ Added: None", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ You've already selected None.", ephemeral=True)

    @discord.ui.button(label="🗑️ Clear All", style=discord.ButtonStyle.secondary)
    async def clear_all(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        user_responses.setdefault(user_id, {})["diet"] = []
        await interaction.response.send_message("Cleared all dietary selections.", ephemeral=True)

    @discord.ui.button(label="Submit", style=discord.ButtonStyle.primary)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        diet = user_responses.get(user_id, {}).get("diet", [])
        if not diet:
            await interaction.response.send_message("⚠️ You haven't selected any dietary preferences yet.",
                                                        ephemeral=True)
            return
        await interaction.response.send_message("Submitting your dietary preferences...", ephemeral=True)
        await finish_survey(interaction)
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
            await interaction.response.send_message(
                "DM's are off for this user",
                ephemeral=True
            )
async def send_shirt_size(interaction):
    embed = discord.Embed(
        title="👕 Shirt Size",
        description="Please select your shirt size:",
        color=discord.Color.blurple()
    )
    await interaction.channel.send(embed=embed, view=ShirtSizeView())


async def send_diet(interaction):
    embed = discord.Embed(
        title="🥗 Dietary Preference",
        description="Do you have any dietary restrictions?",
        color=discord.Color.blurple()
    )
    await interaction.channel.send(embed=embed, view=DietView())


async def finish_survey(interaction):
    user_id = interaction.user.id
    data = user_responses.get(user_id, {})
    diet_list = data.get("diet", [])
    diet_display = ", ".join(diet_list) if isinstance(diet_list, list) else diet_list
    summary = (
        f"🧾 **Survey Complete!**\n"
        f"• User ID: `{user_id}`\n"
        f"• Shirt Cut: `{data.get('cut', 'none')}`\n"
        f"• Shirt Size: `{data.get('size', 'none')}`\n"
        f"• Dietary: `{diet_display or 'none'}`"
    )
    await interaction.channel.send(summary)


