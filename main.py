# Import necessary libraries
import discord
from discord.ext import commands
import random
import string
import json
import os

# Define your intents
intents = discord.Intents.all()

# Set up the bot prefix and create a bot instance with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Remove the default /help command
bot.remove_command('help')

# Global variable to store bot name
bot_name = None

# Function to generate a random license key
def generate_license_key():
    characters = string.ascii_uppercase + string.digits
    license_key = ''.join(random.choice(characters) for _ in range(16))
    return license_key

# Function to save license data to keys.json
def save_license_data(user_id, license_key, duration, activated=False):
    if not os.path.exists('keys.json') or os.path.getsize('keys.json') == 0:
        with open('keys.json', 'w') as file:
            json.dump({}, file, indent=4)

    with open('keys.json', 'r') as file:
        data = json.load(file)

    data[str(user_id)] = {'license_key': license_key, 'duration': duration, 'activated': activated}

    with open('keys.json', 'w') as file:
        json.dump(data, file, indent=4)

# Placeholder for storing active licenses
active_licenses = {}

# Load license data from keys.json
if os.path.exists('keys.json') and os.path.getsize('keys.json') > 0:
    with open('keys.json', 'r') as file:
        active_licenses = json.load(file)

# Function to create an embed with a purple color theme and emojis
def create_embed(title, description, color):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    embed.set_footer(text=f"Thank you for choosing {bot_name}! 🌟")
    return embed

# Event: Bot is ready
@bot.event
async def on_ready():
    global bot_name
    bot_name = bot.user.name
    print("Welcome To The ExiKeys Owner Console!")
    print("Bot Successfully Running")

# Command: /create
@bot.command(name='create', aliases=['generate'])
async def create_license(ctx):
    # Ask for license duration
    duration_embed = discord.Embed(
        title="License Duration",
        description="Please choose the duration for your license:",
        color=discord.Color.purple()
    )
    duration_embed.add_field(name="1️⃣ 1 Day", value="React with 1️⃣ for a 1-day license", inline=False)
    duration_embed.add_field(name="2️⃣ 1 Week", value="React with 2️⃣ for a 1-week license", inline=False)
    duration_embed.add_field(name="3️⃣ 1 Month", value="React with 3️⃣ for a 1-month license", inline=False)
    duration_embed.add_field(name="4️⃣ Lifetime", value="React with 4️⃣ for a lifetime license", inline=False)

    duration_message = await ctx.send(embed=duration_embed)
    await duration_message.add_reaction("1️⃣")
    await duration_message.add_reaction("2️⃣")
    await duration_message.add_reaction("3️⃣")
    await duration_message.add_reaction("4️⃣")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except TimeoutError:
        await ctx.send("Time is up. Please run the command again.")
        return

    duration_mapping = {"1️⃣": "1 day", "2️⃣": "1 week", "3️⃣": "1 month", "4️⃣": "lifetime"}
    selected_duration = duration_mapping[str(reaction.emoji)]

    # Generate a license key
    license_key = generate_license_key()

    # Save license data with activated status set to False
    save_license_data(ctx.author.id, license_key, selected_duration, activated=False)

    # Update active licenses (in-memory storage)
    active_licenses[ctx.author.id] = {'license_key': license_key, 'duration': selected_duration, 'activated': False}

    # Create a formatted embed with purple color theme and emojis
    embed = create_embed(
        title="License Information",
        description=f"Your license has been successfully created!\n\n"
                    f"**License Key:** `{license_key}`\n"
                    f"**Duration:** {selected_duration}",
        color=discord.Color.purple()
    )

    # Send the embed as a message
    await ctx.send(embed=embed)

# Command: /activate
@bot.command(name='activate', aliases=['use'])
async def activate_license(ctx, license_key: str):
    # Check if the license key is valid and not already activated
    user_id = str(ctx.author.id)

    # Reload license data in case it has changed
    if os.path.exists('keys.json') and os.path.getsize('keys.json') > 0:
        with open('keys.json', 'r') as file:
            active_licenses = json.load(file)

    if user_id in active_licenses and active_licenses[user_id]['license_key'] == license_key:
        if not active_licenses[user_id]['activated']:
            # Update the activated status to True
            active_licenses[user_id]['activated'] = True

            # Save updated license data
            with open('keys.json', 'w') as file:
                json.dump(active_licenses, file, indent=4)

            # Create a formatted embed with purple color theme and emojis
            embed = create_embed(
                title="License Activated",
                description="Your license has been successfully activated!",
                color=discord.Color.purple()
            )

            # Send the embed as a message
            await ctx.send(embed=embed)
        else:
            # Create an embed for already activated license key
            embed = create_embed(
                title="Already Activated",
                description="The provided license key has already been activated.",
                color=discord.Color.red()
            )

            # Send the embed as a message
            await ctx.send(embed=embed)
    else:
        # Print debug information
        print(f"DEBUG: User ID: {user_id}, License Key: {license_key}")
        print("DEBUG: Active Licenses:", active_licenses)

        # Create an embed for invalid license key
        embed = create_embed(
            title="Invalid License Key",
            description="The provided license key is not valid. Please double-check.",
            color=discord.Color.red()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)

# Command: /deactivate
@bot.command(name='deactivate', aliases=['stop'])
async def deactivate_license(ctx):
    # Check if the user has an active license
    user_id = str(ctx.author.id)

    # Reload license data in case it has changed
    if os.path.exists('keys.json') and os.path.getsize('keys.json') > 0:
        with open('keys.json', 'r') as file:
            active_licenses = json.load(file)

    if user_id in active_licenses:
        # Deactivate the license for the user
        del active_licenses[user_id]

        # Save updated license data
        with open('keys.json', 'w') as file:
            json.dump(active_licenses, file, indent=4)

        # Create a formatted embed with purple color theme and emojis
        embed = create_embed(
            title="License Deactivated",
            description="Your license has been successfully deactivated.",
            color=discord.Color.purple()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)
    else:
        # Create an embed for no active license
        embed = create_embed(
            title="No Active License",
            description="You don't have an active license to deactivate.",
            color=discord.Color.red()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)

# Command: /checklicense
@bot.command(name='checklicense', aliases=['status'])
async def check_license(ctx):
    # Check if the user has an active license
    user_id = str(ctx.author.id)

    # Reload license data in case it has changed
    if os.path.exists('keys.json') and os.path.getsize('keys.json') > 0:
        with open('keys.json', 'r') as file:
            active_licenses = json.load(file)

    if user_id in active_licenses:
        # Create a formatted embed with purple color theme and emojis
        embed = create_embed(
            title="Active License",
            description=f"You currently have an active license.\n\n"
                        f"**License Key:** `{active_licenses[user_id]['license_key']}`\n"
                        f"**Duration:** {active_licenses[user_id]['duration']}",
            color=discord.Color.purple()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)
    else:
        # Create an embed for no active license
        embed = create_embed(
            title="No Active License",
            description="You don't have an active license. Consider activating one with `/activate`.",
            color=discord.Color.red()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)

# Command: /owner
@bot.command(name='owner')
async def check_owner(ctx, license_key: str):
    # Reload license data in case it has changed
    if os.path.exists('keys.json') and os.path.getsize('keys.json') > 0:
        with open('keys.json', 'r') as file:
            active_licenses = json.load(file)

    # Search for the owner of the given license key
    owner_id = None
    for user_id, data in active_licenses.items():
        if data['license_key'] == license_key:
            owner_id = user_id
            break

    if owner_id:
        # Get the owner's username
        owner = await bot.fetch_user(owner_id)

        # Create an embed with information about the owner
        embed = create_embed(
            title="License Owner",
            description=f"The owner of the license key `{license_key}` is {owner.mention}.",
            color=discord.Color.purple()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)
    else:
        # Create an embed for an invalid license key
        embed = create_embed(
            title="Invalid License Key",
            description="The provided license key is not valid or has not been activated.",
            color=discord.Color.red()
        )

        # Send the embed as a message
        await ctx.send(embed=embed)

# Command: /helpsheet
@bot.command(name='helpsheet')
async def helpsheet(ctx):
    # Create a premium help embed with purple color theme and emojis
    embed = create_embed(
        title="Command Help Sheet",
        description="Welcome to the official ExiKeys Command Help Sheet. Below are the available commands and their usage:",
        color=discord.Color.purple()
    )
    embed.add_field(name="/create or /generate", value="Generate a new license key", inline=False)
    embed.add_field(name="/activate or /use <license_key>", value="Activate your license", inline=False)
    embed.add_field(name="/deactivate or /stop", value="Deactivate your active license", inline=False)
    embed.add_field(name="/checklicense or /status", value="Check the status of your active license", inline=False)
    embed.add_field(name="/owner <license_key>", value="Check the owner of a license key", inline=False)
    embed.set_footer(text=f"Thank you for choosing {bot_name}! For more details, visit our official server! 🌐")

    # Send the embed as a message
    await ctx.send(embed=embed)

# Command: /help
@bot.command(name='help')
async def help_command(ctx):
    # Use the same response as /helpsheet
    await helpsheet(ctx)

# Run the bot with your bot token
bot.run('')
