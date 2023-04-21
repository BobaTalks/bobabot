import discord
import responses
import os
from dotenv import load_dotenv

load_dotenv()


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    token = os.environ["DISCORD_TOKEN"]
    # please input your own token here
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is online")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" {{channel}}')

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    @client.event
    async def on_raw_reaction_add(payload):
        emoji_id = payload.emoji.name
        print(emoji_id)
        # this event detects all reactions, seems to be an issue with the default set of emojis, seems custom emojis have more options

    @client.event
    async def on_raw_reaction_remove(payload):
        print("removal noted")

    client.run(TOKEN)
