from ._anvil_designer import SquadTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Squad(SquadTemplate):
  def __init__(self, id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    self.trophy_club_id = id
    self.club_id = anvil.server.call('query_database_club_per_trophy', self.trophy_club_id)
    self.label_header.text = anvil.server.call('query_database_clubname', self.club_id)
    
  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    open_form('Trophylist', self.club_id)
