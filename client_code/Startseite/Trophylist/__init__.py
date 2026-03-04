from ._anvil_designer import TrophylistTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Trophylist(TrophylistTemplate):
  def __init__(self, id, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
    res = anvil.server.call('query_database_dict_trophies', id)
    self.repeating_panel_trophies.items = res
    self.label_header.text = anvil.server.call('query_database_clubname', id)
    self.configure_plot(id)



  def configure_plot(self, id):
    jahre, anzahl = anvil.server.call('get_trophy_stats_by_club', id)

    self.plot_trophies_per_year.data = [
      {
        "x": jahre,
        "y": anzahl,
        "type": "bar",        # Balkendiagramm (oder "scatter" für eine Linie)
        "marker": {"color": "#2196F3"}
      }
    ]

    self.plot_trophies_per_year.layout = {
      "title": "Gewonnene Trophäen pro Jahr",
      "xaxis": {
        "type": "category",  # Zwingt Plotly, Jahre als einzelne Labels zu sehen
        "title": "Jahr",
        "categoryorder": "category ascending" # Sortiert sie chronologisch
      },
      "yaxis": {
        "title": "Anzahl Trophäen",
        "dtick": 1 # Verhindert halbe Trophäen (1.5, 2.5) auf der Y-Achse
      },
      "bargap": 0.5 # Steuert die Breite der Balken (0.5 = 50% Lücke)
    }