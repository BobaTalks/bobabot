"""
client_requests contains all of the functionality for the bot client to
make requests to the server
"""
import os
import requests
from bson.json_util import dumps
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

      
def get_subscribers_by_tag(tag_id):
    """
    Gets the subscriber ids for the given tag id

    Parameters
    ----------
    tag_id : str
        The id of an applied forum tag
    """
    r = requests.get(f"{server_url}/tags/{tag_id}/subscribers")
    return r.json()
  
  
def remove_subscriber(user_id, tag_id):
    """
    Makes a delete request to the server's /tags/<:id>/subscribers endpoint
    removing the given user id if present

    Parameters
    ----------
    user_id : int
        An integer representing the corresponding user id

    tag_id : str
        The id of the tag being subscribed to by the respective user
    """
    requests.delete(f"{server_url}/tags/{tag_id}/subscribers/{user_id}")


def fetch_subscriptions_by_user_id(user_id):
    """
    Makes a get request to the server's /tags endpoint
    fetching the tags in which the user id is present

    Parameters
    ----------
    user_id : int
        An integer representing the corresponding user id
    """
    response = requests.get(f"{server_url}/tags")
    if response.status_code == 200:
        filtered_tags = []
        for tag in response.json():
            if user_id in tag["subscribers"]:
                filtered_tags.append(tag["name"])
        return filtered_tags
    else:
        print(f"Error fetching subscribed tags: {response.text}")
        return None
      