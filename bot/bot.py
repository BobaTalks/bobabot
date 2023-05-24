import os
from discord import Intents, app_commands, Interaction, Message, Embed
from discord.ui import Select, View
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from menu import MenuView

load_dotenv()

server_name = os.environ["DISCORD_SERVER_NAME"]
channel_name = os.environ["DISCORD_CHANNEL_NAME"]

token = os.environ["DISCORD_TOKEN"]

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=("?",), intents=intents)


def get_thread_tags(ctx, channel_name):
    if ctx.parent.name == channel_name:
        channel_tags = ctx.applied_tags
        return channel_tags


def get_forum_tags(client, guild_name, channel_name):
    client_guilds = client.guilds
    client_channels = get(client_guilds, name=guild_name).channels
    forum_tags = get(client_channels, name=channel_name).available_tags
    return forum_tags


def create_message_string(iter_tags):
    tags = [tag.name for tag in iter_tags]
    return ", ".join(tags)


@bot.event
async def on_ready():
    print(f"{bot.user} is online")


@bot.tree.command()
async def list_tags(interaction):
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    message_string = create_message_string(forum_tags)
    await interaction.response.send_message(f"The available tags are {message_string}")


@bot.tree.command(name="mention")
async def mention_me(interaction):
    caller = interaction.user.id
    await interaction.response.send_message(f"Hello <@{caller}>, here is your mention")


@bot.tree.command(name="opt_in")
async def opt_in(interaction):
    forum_tags = get_forum_tags(bot, server_name, channel_name)
    view = MenuView()
    view.add_menu(forum_tags)
    await interaction.response.send_message(view=view, ephemeral=True)


@bot.event
async def on_thread_create(ctx):
    channel_tags = get_thread_tags(ctx, channel_name)
    message_string = create_message_string(channel_tags)
    await ctx.send(f"The applied tags are: {message_string}")


@bot.command()
async def sync(interaction):
    await bot.tree.sync()


bot.run(token)
