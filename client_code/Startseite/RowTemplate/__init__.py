from ._anvil_designer import RowTemplateTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate(RowTemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("button_choose", "click")
  def button_choose_click(self, **event_args):
    open_form('Startseite.Trophylist', self.item["FID"])
