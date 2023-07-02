from discord import Interaction
from discord.ui import Select, View
from client_requests import add_subscriber


class Menu(Select):
    """
    A class used to represent a select menu in discord. This menu object
    holds the options available to a user but is not responsible for
    displaying the contents. Inherits from discord.ui.Select.

    Methods
    -------
    add_items(tags)
        Adds items to the Menu object
    async callback(interaction)
        Waits for a discord user to select option(s) from the menu and
        sends back a response message
    """

    def __init__(self, tags):
        """
        Parameters
        ----------
        tags : Sequence[ForumTag]
            The tags owned by the Forum channel
        """
        max_values = len(tags)
        super().__init__(
            placeholder="The currently available tags", max_values=max_values
        )

    def add_items(self, tags):
        """
        Parameters
        ----------
        tags : Sequence[ForumTag]
            The tags owned by the Forum channel
        """
        for tag in tags:
            self.add_option(label=tag.name, emoji=tag.emoji, value=tag.id)

    async def callback(self, interaction: Interaction):
        """
        Parameters
        ----------
        interaction: discord.Interaction
            The action implemented by the user that needs to be notified.
            In the context of the bot, the action is a slash command
        """
        for value in self.values:
            add_subscriber(interaction.user.id, value)

        await interaction.response.send_message(
            f"Thank you for selecting {self.values}", ephemeral=True
        )


class MenuView(View):
    """
    A class used to represent a select menu's view in discord. This is
    used to actually display the menu and its contents in discord.
    Inherits from discord.ui.View

    Methods
    -------
    add_menu(tags)
        Adds the Menu object to the view
    """

    def __init(self):
        super().__init__()

    def add_menu(self, tags):
        """
        Parameters
        ----------
        tags : Sequence[ForumTag]
            The tags owned by the Forum channel
        """
        menu = Menu(tags)
        menu.add_items(tags)
        # Adds a menu to the view object that can be displayed in discord
        self.add_item(menu)
