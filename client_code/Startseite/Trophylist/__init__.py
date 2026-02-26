from ._anvil_designer import TrophylistTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Trophylist(TrophylistTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    query = '''
    SELECT t.name, ft.jahr, m.kategorie 
    FROM Fussballverein_Trophaeen ft
    JOIN Trophaeen t ON t.TrID = ft.TrID
    JOIN Mannschaft m ON m.FID = ft.FID
    WHERE 
    
    '''