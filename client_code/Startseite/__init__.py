from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.res = anvil.server.call('query_database_dict_clubs')
    self.repeating_panel_vereine.items = self.res
    teams = [i["Name"] for i in self.res]
    self.drop_down_club.items = teams
    self.drop_down_club_change()


  @handle("drop_down_club", "change")
  def drop_down_club_change(self, **event_args):
    """This method is called when an item is selected"""
    self.id = [i["FID"] for i in self.res if i["Name"] == self.drop_down_club.selected_value][0]
    # Picks the id based on the chosen name 

  @handle("outlined_button_trophylist", "click")
  def outlined_button_trophylist_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Trophylist', self.id)
