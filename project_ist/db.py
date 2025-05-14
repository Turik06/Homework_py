import sqlite3

conn = sqlite3.connect("sports_league.db")
cursor = conn.cursor()

# Leagues Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Leagues (
    league_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT NOT NULL,
    founded_year INTEGER
)
""")
    
# Teams Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    founded_year INTEGER,
    FOREIGN KEY (league_id) REFERENCES Leagues (league_id)
)
""")

# Players Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date DATE,
    nationality TEXT,
    jersey_number INTEGER,
    height REAL,
    weight REAL,
    joining_date DATE,
    contract_end_date DATE,
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
)
""")

# Coaches Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Coaches (
    coach_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date DATE,
    nationality TEXT,
    coaching_style TEXT,
    joining_date DATE,
    contract_end_date DATE,
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
)
""")

# Trophies Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Trophies (
    trophy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    name TEXT NOT NULL,
    competition TEXT NOT NULL,
    year INTEGER NOT NULL,
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
)
""")

# Seasons Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Seasons (
    season_id INTEGER PRIMARY KEY AUTOINCREMENT,
    league_id INTEGER,
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    status TEXT CHECK(status IN ('upcoming', 'ongoing', 'completed')),
    FOREIGN KEY (league_id) REFERENCES Leagues (league_id)
)
""")

# Matches Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    season_id INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    match_date DATETIME,
    home_team_score INTEGER DEFAULT 0,
    away_team_score INTEGER DEFAULT 0,
    match_status TEXT CHECK(match_status IN ('scheduled', 'ongoing', 'completed', 'postponed')),
    attendance INTEGER,
    referee TEXT,
    FOREIGN KEY (season_id) REFERENCES Seasons (season_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams (team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams (team_id)
)
""")

# Goals Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER,
    player_id INTEGER,
    team_id INTEGER,
    minute INTEGER,
    is_penalty BOOLEAN DEFAULT 0,
    is_own_goal BOOLEAN DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES Matches (match_id),
    FOREIGN KEY (player_id) REFERENCES Players (player_id),
    FOREIGN KEY (team_id) REFERENCES Teams (team_id)
)
""")

conn.commit()
conn.close()

print("База данных успешно создана/обновлена")