"""
client_requests contains all of the functionality for the bot client to
make requests to the server
"""
import os
import requests
from dotenv import load_dotenv
from exceptions import EnvironmentVariableNotFoundError

load_dotenv()
try:
    server_url = os.environ["SERVER_URL"]
except KeyError as e:
    raise EnvironmentVariableNotFoundError(e.args[0])


def sync_all_tags(forum_tags):
    """
    Makes a post request to the server's /tags endpoint sending all of
    the channel's available tags. This should only be called when syncing
    the bot's commands

    Parameters
    ----------
    forum_tags : Sequence[ForumTag]
        An iterable of all Discord Forum Tags for the specified channel
    """
    for tag in forum_tags:
        tag_dict = {}
        tag_dict["snowflake_id"] = tag.id
        tag_dict["name"] = tag.name
        tag_dict["subscribers"] = []
        requests.post(f"{server_url}/tags", json=tag_dict)
        requests.Response
