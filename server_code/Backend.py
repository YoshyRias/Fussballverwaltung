import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

@anvil.server.callable
def query_database():
  query = ""
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_database_positions_count(id:int):
  query = f"""SELECT Position, COUNT(SID) as Anzahl
  FROM Spieler
  WHERE MID = {id}
  GROUP BY Position;"""
  
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    res = cur.execute(query).fetchall()
  
  labels = [row[0] for row in res]
  values = [row[1] for row in res]

  return labels, values

@anvil.server.callable
def query_database_trophy_id(name:str):
  query = f"SELECT trid FROM Trophaeen WHERE name='{name}'"
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result[0][0]

@anvil.server.callable
def query_database_club_per_trophy(id:int):
  query = f"SELECT fid FROM Fussballverein_Trophaeen ft WHERE ft.id = {id}"
  sql = f""" SELECT Trophaeen.Name AS Name, Fussballverein_Trophaeen.Jahr AS Jahr FROM Fussballverein_Trophaeen 
  JOIN Trophaeen
  ON Fussballverein_Trophaeen.TrID = Trophaeen.TrID
  WHERE Fussballverein_Trophaeen.ID = '{id}'
  """

  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    trophy = cur.execute(sql).fetchall()
  return result[0][0],trophy[0][0]

@anvil.server.callable
def query_database_trophy_club_id(trophy_id:int, club_id):
  query = f"SELECT id FROM Fussballverein_Trophaeen ft WHERE ft.trid = {trophy_id} AND ft.fid = {club_id}"
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result[0][0]
  
@anvil.server.callable
def query_database_clubname(id:int):
  query = f"SELECT name FROM Fussballverein WHERE FID={id}"
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result[0][0]
 
@anvil.server.callable
def query_database_dict_clubs():
  query = "SELECT fid, name, gruendungsjahr FROM Fussballverein"
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def query_database_dict_trophies(id:int):
  query = f"""SELECT t.name, ft.jahr, m.kategorie, ft.trid, ft.fid 
    FROM Fussballverein_Trophaeen ft
    JOIN Trophaeen t ON t.TrID = ft.TrID
    JOIN Mannschaft m ON m.FID = ft.FID
    WHERE ft.FID = {id};"""
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def query_database_dict_squad(id:int):
  query = f"""SELECT Name, "Alter", Position 
    FROM Spieler s
    WHERE s.MID = {id};"""
  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def get_trophy_stats_by_club(id:int):
  query = f"""
    SELECT Jahr, COUNT(TrID) as Anzahl
    FROM Fussballverein_Trophaeen
    WHERE FID = {id}
    GROUP BY Jahr
    ORDER BY Jahr ASC
    """

  with sqlite3.connect(data_files["fussball_verwaltung.db"]) as conn:
    cur = conn.cursor()
    res = dict(cur.execute(query).fetchall())

  start_jahr = 2010
  end_jahr = 2025
  jahre = []
  anzahl = []

  for i in range(start_jahr, end_jahr + 1):
    jahre.append(str(i))
    anzahl.append(res.get(i, 0))

  return jahre, anzahl