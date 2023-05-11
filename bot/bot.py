import os
from discord import Intents
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()

token = os.environ["DISCORD_TOKEN"]
intents = Intents.default()
intents.message_content=True
bot = commands.Bot(command_prefix="?", intents=intents)

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
    forum_tags = get_forum_tags(bot, "BOT TESTING", "test-forum")
    print(f"{bot.user} is online")
    print(f"Available tags: {forum_tags}")

@bot.command()
async def list_tags(ctx):
    forum_tags = get_forum_tags(bot, "BOT TESTING", "test-forum")
    message_string = create_message_string(forum_tags)
    await ctx.send(f"The available tags are {message_string}")

@bot.command()
async def mention_me(ctx):
    caller = ctx.author.id
    await ctx.send(f"Hello <@{caller}>, here is your mention")

@bot.event
async def on_thread_create(ctx):
    channel_tags = get_thread_tags(ctx, "test-forum")
    message_string = create_message_string(channel_tags)
    await ctx.send(f"The applied tags are: {message_string}")
    

bot.run(token)