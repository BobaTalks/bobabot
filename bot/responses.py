import random
import bot


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"

    if p_message == "!help":
        return "Here is the list of available commands: "

    return 'I didn\'t understand what you wrote. Try typing "!help".'
