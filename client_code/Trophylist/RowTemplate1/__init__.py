from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    

  @handle("button_choose", "click")
  def button_choose_click(self, **event_args):
    main_form = self.parent.parent.parent.parent
    trophy_id = anvil.server.call('query_database_trophy_id', self.item['Name'])
    id = anvil.server.call('query_database_trophy_club_id', trophy_id, main_form.cur_id)
    open_form('Squad', id)
    