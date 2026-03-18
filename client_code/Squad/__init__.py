from ._anvil_designer import SquadTemplate
from anvil import *
import plotly.graph_objects as go
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
    self.club_id, self.trophy = anvil.server.call('query_database_club_per_trophy', self.trophy_club_id)
    self.label_header.text = anvil.server.call('query_database_clubname', self.club_id)
    self.repeating_panel_squad.items = anvil.server.call('query_database_dict_squad', self.club_id)
    self.update_position_chart(self.club_id)

    print(self.trophy)

    
  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    open_form('Trophylist', self.club_id)

  def update_position_chart(self, mid):
    # Daten vom Server holen
    labels, values = anvil.server.call('query_database_positions_count', mid)

    # Kreisdiagramm konfigurieren
    self.plot_squad.data = [{
      "labels": labels,
      "values": values,
      "type": "pie",
      "hole": 0.4, # Macht ein Ring-Diagramm daraus (Donut-Chart), sieht moderner aus
      "marker": {"colors": ['#9374fe', '#223ca2', '#124172', '#67afe5']} 
    }]


  @handle("button_home", "click")
  def button_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
