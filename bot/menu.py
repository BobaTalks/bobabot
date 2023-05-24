from discord import Interaction
from discord.ui import Select, View


class Menu(Select):
    def __init__(self, tags):
        max_values = len(tags)
        super().__init__(
            placeholder="The currently available tags", max_values=max_values
        )

    def add_items(self, tags):
        for tag in tags:
            self.add_option(label=tag.name, emoji=tag.emoji)

    async def callback(self, interaction: Interaction):
        selected_values = self.values
        await interaction.response.send_message(
            f"Thank you for selecting {selected_values}", ephemeral=True
        )


class MenuView(View):
    def __init(self):
        super().__init__()

    def add_menu(self, tags):
        menu = Menu(tags)
        menu.add_items(tags)
        # Adds a menu to the view object that can be displayed in discord
        self.add_item(menu)
