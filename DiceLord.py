# region startup
# Imports and other stuffs like bot token
import discord
from discord import app_commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the private key and guild
private_key = os.getenv('DiceLord_KEY')
guildid = os.getenv('DiceLord_GUILD')
# endregion

# region Variables
Oneshot = int(os.getenv("ONESHOT_ROLE_ID"))  # Ensure it's an integer
Campaign = int(os.getenv("CAMPAIGN_ROLE_ID"))  # Ensure it's an integer

Channel = os.getenv('Roller_Channel_ID')  # Load the channel ID
# endregion

# region add things like on_message here
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await tree.sync(guild=discord.Object(id=guildid))
        print("Commands synced and ready!")

                # Get the channel where the bot should perform cleanup
        channel = self.get_channel(int(Channel))
        if channel:
            # Run the /cleanup command
            cleanup_command = tree.get_command("cleanup", guild=discord.Object(id=guildid))
            if cleanup_command:
                await cleanup_command.callback(interaction=await self.fake_interaction(channel))

            # Run the /sendroles command
            sendroles_command = tree.get_command("sendroles", guild=discord.Object(id=guildid))
            if sendroles_command:
                await sendroles_command.callback(interaction=await self.fake_interaction(channel))
        else:
            print("Channel not found. Make sure the Channel ID is correct.")

    async def fake_interaction(self, channel):
        """Create a fake interaction to use in place of a user invoking a command"""
        class FakeResponse:
            async def send_message(self, content, ephemeral=False, view=None):
                await channel.send(content, view=view)

            async def defer(self):
                pass  # Placeholder if deferring responses is needed

        class FakeInteraction:
            def __init__(self, client, channel):
                self.client = client
                self.channel = channel
                self.guild = channel.guild
                self.user = client.user
                self.response = FakeResponse()  # Use a proper response object

        return FakeInteraction(self, channel)
        

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('test'):
            await message.channel.send('test complete')
    
    # region Funny stuff

        if 'Aphireon' in message.content:
            await message.channel.send('Yooooo das my creator')
    
        if 'aphireon' in message.content:
            await message.channel.send('Yooooo das my creator')

        if 'Albert' in message.content:
            await message.channel.send('𓁹‿𓁹 HEH.')
    
        if 'albert' in message.content:
            await message.channel.send('𓁹‿𓁹 HEH.')
    # endregion
# endregion


# region Intents and client
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Required to manage roles

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)
# endregion


# region Role buttons
class RoleButton(discord.ui.Button):
    def __init__(self, label, role_id, style, emoji=None):
        super().__init__(label=label, style=style, emoji=emoji)
        self.role_id = role_id

    async def callback(self, interaction: discord.Interaction):
        print(f"Button clicked: {self.label} with role ID: {self.role_id}")  # Debug statement

        # Ensure role_id is an integer
        print(f"Role ID type: {type(self.role_id)}")  # Debug statement

        role = interaction.guild.get_role(self.role_id)
    
        if not role:
            await interaction.response.send_message("Role not found!", ephemeral=True)
            print(f"Role with ID {self.role_id} not found in guild {interaction.guild.name}.")  # Debug statement
            return
    
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"Removed {role.name} from you.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Granted {role.name} to you.", ephemeral=True)

#Button text and emoji
class RoleView(discord.ui.View):
    def __init__(self, role1_id, role2_id):
        super().__init__()
        # Add a button with a custom emoji
        custom_emoji1 = discord.PartialEmoji(name="customemoji1", id=1295071923067158609)  # Replace with your emoji's name and ID
        custom_emoji2 = discord.PartialEmoji(name="customemoji2", id=1295071901609103391)  # Replace with your emoji's name and ID

        self.add_item(RoleButton("Oneshots", role1_id, style=discord.ButtonStyle.primary, emoji=custom_emoji1))
        self.add_item(RoleButton("Campaign", role2_id, style=discord.ButtonStyle.secondary, emoji=custom_emoji2))

#Role change
@tree.command(
    name="sendroles",
    description="Send a message with role buttons.",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def send_roles(interaction):
    role1_id = Oneshot  # Replace with your first role ID
    role2_id = Campaign  # Replace with your second role ID
    view = RoleView(role1_id, role2_id)

    await interaction.response.send_message(
        "Click a button to receive or remove a role. Remember Campaign role is for Jonathan's campaign and should be agreed with him to recieve:", view=view)
# endregion

# region Cleanup
@tree.command(
    name="cleanup",
    description="Deletes the bot's messages in the specified channel.",
    guild=discord.Object(id=guildid)  # Your guild ID
)
async def cleanup(interaction: discord.Interaction):
    global Channel  # Declare Channel as global

    # Ensure the channel ID is valid
    try:
        CHANNEL_ID = int(Channel)  # Convert to int
    except ValueError:
        await interaction.response.send_message("Invalid channel ID. Please check your environment variables.", ephemeral=True)
        return

    # Get the channel using the channel ID
    channel = interaction.guild.get_channel(CHANNEL_ID)

    if channel is None:
        await interaction.response.send_message("Channel not found. Please check your configuration.", ephemeral=True)
        return

    # Attempt to delete the bot's messages
    deleted_count = 0
    try:
        async for message in channel.history(limit=100):  # Adjust limit as needed
            if message.author.id == interaction.client.user.id:  # Check if the message is from the bot
                await message.delete()
                deleted_count += 1

    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to delete messages in that channel.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

# endregion


# region Dice commands
@tree.command(
    name="roll2",
    description="Roll a 2-sided dice",
    guild=discord.Object(id=guildid)
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 2)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll4",
    description="Roll a 4-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 4)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll6",
    description="Roll a 6-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 6)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll8",
    description="Roll a 8-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 8)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll10",
    description="Roll a 10-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 10)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll12",
    description="Roll a 12-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 12)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll20",
    description="Roll a 20-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 20)
    await interaction.response.send_message(f"You rolled a {result}!")

@tree.command(
    name="roll100",
    description="Roll a 100-sided dice",
    guild=discord.Object(id=guildid)  # Replace with your guild ID
)
async def roll_dice(interaction: discord.Interaction):
    import random
    result = random.randint(1, 100)
    await interaction.response.send_message(f"You rolled a {result}!")
# endregion


#region Fireballllllll
@tree.command(
    name="fireball",
    description="Cast a fireball",
    guild=discord.Object(id=1284153149220720692)  # Replace with your guild ID
)
async def custom_emoji_command(interaction: discord.Interaction):
    Fireball_emoji = "<:fireball:1295100878667255850>"  # Replace with your emoji name and ID
    await interaction.response.send_message(Fireball_emoji)
# endregion


# region Running the bot
client.run(private_key) # Dice lord token.
# endregion
