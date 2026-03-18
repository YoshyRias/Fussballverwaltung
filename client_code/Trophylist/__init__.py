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
    self.cur_id = id
    self.res = anvil.server.call('query_database_dict_trophies', id)
    self.repeating_panel_trophies.items = self.res
    self.label_header.text = anvil.server.call('query_database_clubname', id)
    self.configure_plot(id)
    self.drop_down_squad.items = [f"{i['Name']} ({i['Jahr']})" for i in self.res]
    self.drop_down_squad_change()


  def configure_plot(self, id):
    jahre, anzahl = anvil.server.call('get_trophy_stats_by_club', id)

    balken = go.Bar(
      x = jahre,
      y = anzahl,
      marker=dict(color="#17ecda")
    )
    
    self.plot_trophies_per_year.data = [balken]

    self.plot_trophies_per_year.layout.yaxis.dtick = 1
    self.plot_trophies_per_year.layout.xaxis.type = "category"
    self.plot_trophies_per_year.layout.bargap = 0.5
    self.plot_trophies_per_year.layout.title = "SigmaLigma"

  @handle("button_back", "click")
  def button_back_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("button_home", "click")
  def button_home_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

  @handle("outlined_button_squad", "click")
  def outlined_button_squad_click(self, **event_args):
    id = anvil.server.call('query_database_trophy_club_id', self.cur_trid, self.cur_fid)
    open_form('Squad', id)

  @handle("drop_down_squad", "change")
  def drop_down_squad_change(self, **event_args):
    """This method is called when an item is selected"""
    selected = self.drop_down_squad.selected_value
  
    match = next(i for i in self.res if f"{i['Name']} ({i['Jahr']})" == selected)
  
    self.cur_trid = match['TrID']
    self.cur_fid = match['FID']
