import os
from discord import Intents, app_commands, Interaction, Message, Embed
from discord.ui import Select, View
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from menu import MenuView
from client_requests import sync_all_tags, fetch_subscriptions

load_dotenv()

server_name = os.environ["DISCORD_SERVER_NAME"]
channel_name = os.environ["DISCORD_CHANNEL_NAME"]

token = os.environ["DISCORD_TOKEN"]

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=("?",), intents=intents)


def get_thread_tags(ctx, channel_name):
    """
    Given the discord forum channel name, gets the tags applied to a forum thread

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        An object that represents the context in which the discord command is invoked
    channel_name: str
        The name for the respective forum channel
    """
    if ctx.parent.name == channel_name:
        channel_tags = ctx.applied_tags
        return channel_tags


def get_forum_tags(client, guild_name, channel_name):
    """
    Given the discord server name AND forum channel name, gets all of the
    tags available to that forum

    Parameters
    ----------
    client : discord.ext.commands.Bot
        A discord bot object
    guild_name : str
        The name for the respective server(known as guilds in Discord API)
    channel_name: str
        The name for the respective forum channel
    """
    client_guilds = client.guilds
    client_channels = get(client_guilds, name=guild_name).channels
    forum_tags = get(client_channels, name=channel_name).available_tags
    return forum_tags


def create_message_string(iter_tags):
    """
    Creates a comma separated string from an iterable of forum tags

    Parameters
    ----------
    iter_tags : Sequence[ForumTag]
        An iterable of Discord Forum Tags
    """
    tags = [tag.name for tag in iter_tags]
    return ", ".join(tags)


@bot.command()
async def boba(ctx):
    """
    Creates a boba-ascii art and outputs to respective channel

    Parameters
    ----------
    ctx : Discord Context
        Includes information on who executed the command (namely channel)
    """
    ascii_art = "\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣤⣴⣶⣶⣦⣤⣤⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠉⣉⠉⠉⠹⣿⠀⠀⠀⠀⠀⠈⠉⠉⣉⠉⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⢸⡿⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡆⠘⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⠀⢻⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⡄⠸⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣧⠀⢿⣿⣿⡟⢻⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⣿⠉⢻⡀⢸⡏⢉⡗⢺⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣄⣼⠛⢻⣇⣀⡟⢉⣷⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⣼⣷⣾⣅⣹⣿⣿⣤⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    await ctx.send(ascii_art)


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.tree.command()
async def list_tags(interaction):
    """
    Lists all of the available tags.

    Parameters
    ----------
    interaction: discord.Interaction
        The action implemented by the user that needs to be notified.
        In the context of the bot, the action is a slash command
    """
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    message_string = create_message_string(forum_tags)
    await interaction.response.send_message(f"The available tags are {message_string}")


@bot.tree.command(name="mention")
async def mention_me(interaction):
    """
    Sends a message mentioning the user who called this function.

    Parameters
    ----------
    interaction: discord.Interaction
        The action implemented by the user that needs to be notified.
        In the context of the bot, the action is a slash command
    """
    caller = interaction.user.id
    await interaction.response.send_message(f"Hello <@{caller}>, here is your mention")


@bot.tree.command(name="subscribe")
async def subscribe(interaction):
    """
    Presents a selectable menu of tags for reviewers to subscribe to.

    Parameters
    ----------
    interaction: discord.Interaction
        The action implemented by the user that needs to be notified.
        In the context of the bot, the action is a slash command
    """
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    view = MenuView(True)
    view.add_menu(forum_tags)
    await interaction.response.send_message(view=view, ephemeral=True)


@bot.tree.command(name="unsubscribe")
async def unsubscribe(interaction):
    """
    Present a selectable menu of tags for reviewers to unsubscribe from.

    Parameters:
    -----------
    interaction: discord.Interaction
        The action implemented by the user that needs to be notified.
        In the context of the bot, the action is a slash command
    """
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    subscribed_tags = fetch_subscriptions(interaction.user.id)
    # Filtering from forum_tags to retain important channel information (for Menu)
    forum_tags = [tag for tag in forum_tags if tag.name in subscribed_tags]
    view = MenuView(False)
    view.add_menu(forum_tags)
    await interaction.response.send_message(view=view, ephemeral=True)


@bot.event
async def on_thread_create(ctx):
    """
    On creation of a thread, sends a message listing all of the applied tags.

    Parameters
    ----------
    ctx : discord.ext.commands.Context
        An object that represents the context in which the discord command is invoked
    """
    channel_tags = get_thread_tags(ctx, channel_name)
    message_string = create_message_string(channel_tags)
    await ctx.send(f"The applied tags are: {message_string}")


@bot.command()
async def sync(interaction):
    """
    Syncs the bot tree commands if any changes have been made. Additionally
    syncs the forum tags with the database.

    Parameters
    ----------
    interaction: discord.Interaction
        The action implemented by the user that needs to be notified.
        In the context of the bot, the action is a slash command
    """
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    sync_all_tags(forum_tags)
    await bot.tree.sync()


bot.run(token)
