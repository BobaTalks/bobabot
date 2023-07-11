from client_requests import get_subscribers_by_tag

def create_mention_string(tag_ids):
    """
    Accepts tag ids and creates a string to mention all respective subscribers.

    Parameters
    ----------
    tag_ids : List[ForumTag]
    """
    total_subscribers = []
    mention_string = ""
    for tag in tag_ids:
        total_subscribers.extend(get_subscribers_by_tag(tag.id))
    for subscriber in set(total_subscribers):
        mention_string += f"<@{subscriber}>"
    return mention_string