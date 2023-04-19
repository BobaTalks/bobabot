import random
import bot


def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hello":
        return "Hey there!"
    # testing to see if bot was responsive when online

    if message == "roll":
        return str(random.randint(1, 6))
    # silly test for seeing how pip packages worked in python

    if message == "assign":
        return bot.username
        # just testing to see if i can directly deal with assigning from messaging

    if p_message == "!help":
        return '`"Will put list of emojis to add here.`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'
