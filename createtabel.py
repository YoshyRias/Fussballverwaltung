import sqlite3

def setup_database():
    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect('fussball_verwaltung.db')
    cursor = conn.cursor()

    # --- 1. TABELLEN LÖSCHEN ---
    tables = [
        "Fussballverein_Trophaeen", "Spieler", "Trainer",
        "Mannschaft", "Trophaeen", "Fussballverein"
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table};")

    # --- 2. TABELLEN ERSTELLEN (Ohne Foreign Keys & Ohne Autoincrement) ---
    cursor.execute('''
        CREATE TABLE Fussballverein (
            FID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Gruendungsjahr INTEGER
        );
    ''')

    cursor.execute('''
        CREATE TABLE Mannschaft (
            MID INTEGER PRIMARY KEY,
            Kategorie TEXT NOT NULL,
            FID INTEGER
        );
    ''')

    cursor.execute('''
        CREATE TABLE Trainer (
            TID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            "Alter" INTEGER,
            Gehalt INTEGER,
            MID INTEGER
        );
    ''')

    cursor.execute('''
        CREATE TABLE Spieler (
            SID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            "Alter" INTEGER,
            Position TEXT,
            MID INTEGER
        );
    ''')

    cursor.execute('''
        CREATE TABLE Trophaeen (
            TrID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL
        );
    ''')

    cursor.execute('''
        CREATE TABLE Fussballverein_Trophaeen (
            ID INTEGER PRIMARY KEY,
            Jahr INTEGER,
            FID INTEGER,
            TrID INTEGER
        );
    ''')

    # --- 3. DATEN BEFÜLLEN ---

    # --- ALTE VEREINE ---
    cursor.execute("INSERT INTO Fussballverein VALUES (1, 'FC Bayern München', 1900)")
    cursor.execute("INSERT INTO Fussballverein VALUES (2, 'Borussia Dortmund', 1909)")
    cursor.execute("INSERT INTO Fussballverein VALUES (3, 'Bayer 04 Leverkusen', 1904)")
    cursor.execute("INSERT INTO Fussballverein VALUES (4, 'Real Madrid', 1902)")
    cursor.execute("INSERT INTO Fussballverein VALUES (5, 'Manchester City', 1880)")

    bayern_id, bvb_id, bayer_id, real_id, city_id = 1, 2, 3, 4, 5

    # MANNSCHAFTEN
    cursor.execute("INSERT INTO Mannschaft VALUES (1, '1. Herren', 1)")  # Bayern
    cursor.execute("INSERT INTO Mannschaft VALUES (2, '1. Herren', 2)")  # BVB
    cursor.execute("INSERT INTO Mannschaft VALUES (3, '1. Herren', 3)")  # Bayer
    cursor.execute("INSERT INTO Mannschaft VALUES (4, '1. Herren', 4)")  # Real
    cursor.execute("INSERT INTO Mannschaft VALUES (5, '1. Herren', 5)")  # City

    m_bayern, m_bvb, m_bayer, m_real, m_city = 1, 2, 3, 4, 5

    # TRAINER
    trainer = [
        (1, 'Vincent Kompany', 38, 8000000, m_bayern),
        (2, 'Nuri Şahin', 35, 3000000, m_bvb),
        (3, 'Xabi Alonso', 42, 6000000, m_bayer),
        (4, 'Carlo Ancelotti', 64, 11000000, m_real),
        (5, 'Pep Guardiola', 53, 23000000, m_city)
    ]
    cursor.executemany("INSERT INTO Trainer VALUES (?, ?, ?, ?, ?)", trainer)

    # SPIELER (Deine alten + viele neue für die 5-Spieler-Regel pro Erfolg)
    spieler = [
        # FC Bayern (Kader 2024 & Legenden für Trophäen-Historie)
        (1, 'Jamal Musiala', 21, 'Mittelfeld', m_bayern),
        (2, 'Harry Kane', 30, 'Sturm', m_bayern),
        (3, 'Manuel Neuer', 38, 'Tor', m_bayern),
        (4, 'Thomas Müller', 34, 'Sturm', m_bayern),
        (5, 'Joshua Kimmich', 29, 'Mittelfeld', m_bayern),
        (6, 'Alphonso Davies', 23, 'Abwehr', m_bayern),
        (7, 'Leroy Sané', 28, 'Sturm', m_bayern),
        (8, 'Kingsley Coman', 27, 'Sturm', m_bayern),
        (9, 'Leon Goretzka', 29, 'Mittelfeld', m_bayern),
        (10, 'Dayot Upamecano', 25, 'Abwehr', m_bayern),

        # BVB
        (11, 'Julian Brandt', 27, 'Mittelfeld', m_bvb),
        (12, 'Nico Schlotterbeck', 24, 'Abwehr', m_bvb),
        (13, 'Gregor Kobel', 26, 'Tor', m_bvb),
        (14, 'Emre Can', 30, 'Mittelfeld', m_bvb),
        (15, 'Karim Adeyemi', 22, 'Sturm', m_bvb),

        # Bayer Leverkusen (Meisterkader 2024)
        (16, 'Florian Wirtz', 21, 'Mittelfeld', m_bayer),
        (17, 'Granit Xhaka', 31, 'Mittelfeld', m_bayer),
        (18, 'Victor Boniface', 23, 'Sturm', m_bayer),
        (19, 'Jonathan Tah', 28, 'Abwehr', m_bayer),
        (20, 'Lukas Hradecky', 34, 'Tor', m_bayer),
        (21, 'Jeremie Frimpong', 23, 'Abwehr', m_bayer),
        (22, 'Alejandro Grimaldo', 28, 'Abwehr', m_bayer),
        (23, 'Robert Andrich', 29, 'Mittelfeld', m_bayer),

        # Real Madrid
        (24, 'Jude Bellingham', 20, 'Mittelfeld', m_real),
        (25, 'Vinícius Júnior', 23, 'Sturm', m_real),
        (26, 'Luka Modric', 38, 'Mittelfeld', m_real),
        (27, 'Thibaut Courtois', 32, 'Tor', m_real),
        (28, 'Antonio Rüdiger', 31, 'Abwehr', m_real),
        (29, 'Rodrygo', 23, 'Sturm', m_real),

        # Man City
        (30, 'Erling Haaland', 23, 'Sturm', m_city),
        (31, 'Kevin De Bruyne', 32, 'Mittelfeld', m_city),
        (32, 'Rodri', 27, 'Mittelfeld', m_city),
        (33, 'Ruben Dias', 27, 'Abwehr', m_city),
        (34, 'Phil Foden', 24, 'Sturm', m_city),
        (35, 'Ederson', 30, 'Tor', m_city)
    ]
    cursor.executemany("INSERT INTO Spieler VALUES (?, ?, ?, ?, ?)", spieler)

    # TROPHÄEN
    cursor.execute("INSERT INTO Trophaeen VALUES (1, 'Bundesliga Meisterschale')")
    cursor.execute("INSERT INTO Trophaeen VALUES (2, 'Champions League')")
    cursor.execute("INSERT INTO Trophaeen VALUES (3, 'DFB-Pokal')")
    cursor.execute("INSERT INTO Trophaeen VALUES (4, 'Premier League')")
    cursor.execute("INSERT INTO Trophaeen VALUES (5, 'La Liga')")

    bl_id, cl_id, pokal_id, pl_id, laliga_id = 1, 2, 3, 4, 5

    # SIEGE (Historische Daten)
    siege = [
        # Bayern
        (2023, bayern_id, bl_id),
        (2020, bayern_id, cl_id), (2020, bayern_id, bl_id), (2020, bayern_id, pokal_id),  # Triple
        (2013, bayern_id, cl_id),
        # BVB
        (2012, bvb_id, bl_id), (2021, bvb_id, pokal_id),
        # Leverkusen
        (2024, bayer_id, bl_id), (2024, bayer_id, pokal_id),
        # Real
        (2024, real_id, cl_id), (2024, real_id, laliga_id),
        # City
        (2023, city_id, cl_id), (2024, city_id, pl_id)
    ]
    cursor.executemany("INSERT INTO Fussballverein_Trophaeen (Jahr, FID, TrID) VALUES (?, ?, ?)", siege)

    conn.commit()
    conn.close()
    print("Datenbank erfolgreich mit realistischen Profi-Daten befüllt!")


if __name__ == '__main__':
    setup_database()