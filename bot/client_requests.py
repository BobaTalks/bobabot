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


def add_subscriber(user_id, tag_id):
    """
    Makes a post request to the server's /tags/<:id>/subscribers endpoint
    appending the given user id to the given tag id

    Parameters
    ----------
    user_id : int
        An integer representing the corresponding user id

    tag_id : str
        The id of the tag being subscribed to by the respective user
    """

    payload = {"subscriber_id": user_id}
    requests.post(f"{server_url}/tags/{tag_id}/subscribers", json=payload)

    
def fetch_subscriptions(user_id):
    """
    Makes a get request to the server's /tags/<:id>/subscribers endpoint
    fetching the tag if the given user id is present

    Parameters
    ----------
    user_id : int
        An integer representing the corresponding user id
    """
    response = requests.get(f"{server_url}/tags/subscribers", params={"subscriber_id": user_id})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching subscribed tags: {response.text}")
        return None
    
