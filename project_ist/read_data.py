import sqlite3


def read_txt_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
        if not lines:
            return []
        # Пропускаем заголовок, разбиваем по запятой, убираем кавычки
        return [
            tuple(field.strip().strip('"') for field in line.split(","))
            for line in lines[1:]
        ]


conn = sqlite3.connect("sports_league.db")
cursor = conn.cursor()

tables = {
    "Leagues": ("data/leagues.txt", ["league_id", "name", "country", "founded_year"]),
    "Teams": (
        "data/teams.txt",
        ["team_id", "league_id", "name", "city", "founded_year"],
    ),
    "Players": (
        "data/players.txt",
        [
            "player_id",
            "team_id",
            "first_name",
            "last_name",
            "birth_date",
            "nationality",
            "jersey_number",
            "height",
            "weight",
            "joining_date",
            "contract_end_date",
        ],
    ),
    "Coaches": (
        "data/coaches.txt",
        [
            "coach_id",
            "team_id",
            "first_name",
            "last_name",
            "birth_date",
            "nationality",
            "coaching_style",
            "joining_date",
            "contract_end_date",
        ],
    ),
    "Trophies": (
        "data/trophies.txt",
        ["trophy_id", "team_id", "name", "competition", "year"],
    ),
    "Seasons": (
        "data/seasons.txt",
        ["season_id", "league_id", "name", "start_date", "end_date", "status"],
    ),
    "Matches": (
        "data/matches.txt",
        [
            "match_id",
            "season_id",
            "home_team_id",
            "away_team_id",
            "match_date",
            "home_team_score",
            "away_team_score",
            "match_status",
            "attendance",
            "referee",
        ],
    ),
    "Goals": (
        "data/goals.txt",
        [
            "goal_id",
            "match_id",
            "player_id",
            "team_id",
            "minute",
            "is_penalty",
            "is_own_goal",
        ],
    ),
}

int_fields = {
    "league_id",
    "founded_year",
    "team_id",
    "player_id",
    "jersey_number",
    "coach_id",
    "trophy_id",
    "year",
    "season_id",
    "home_team_id",
    "away_team_id",
    "home_team_score",
    "away_team_score",
    "attendance",
    "minute",
    "is_penalty",
    "is_own_goal",
}
float_fields = {"height", "weight"}

for table, (file, columns) in tables.items():
    try:
        print(f"Загрузка данных из {file} в таблицу {table}...")
        data = read_txt_file(file)
        placeholders = ",".join(["?"] * len(columns))
        query = f"INSERT OR IGNORE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        for row in data:
            converted_row = []
            for value, column in zip(row, columns):
                value = value.strip() if value else None
                if value is None or value == "":
                    converted_row.append(None)
                elif column in int_fields:
                    try:
                        converted_row.append(int(value))
                    except (ValueError, TypeError):
                        converted_row.append(None)
                elif column in float_fields:
                    try:
                        converted_row.append(float(value))
                    except (ValueError, TypeError):
                        converted_row.append(None)
                else:
                    converted_row.append(value)
            try:
                cursor.execute(query, converted_row)
            except Exception as e:
                print(f"⚠️ Ошибка при обработке строки в {table}: {row}")
                print(f"  Детали: {str(e)}")
    except FileNotFoundError:
        print(f"❌ Файл не найден: {file}")
    except Exception as e:
        print(f"❌ Ошибка при обработке таблицы {table}: {str(e)}")

conn.commit()
conn.close()
print("✅ Импорт данных завершен")