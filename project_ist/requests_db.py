# 1. Все лиги с командами и городами
def query_leagues_with_teams():
    return """
        SELECT l.name AS "Лига", t.name AS "Команда", t.city AS "Город"
        FROM Teams t
        JOIN Leagues l ON t.league_id = l.league_id
        ORDER BY l.name, t.name
    """

# 2. Топ-5 бомбардиров лиги
def query_top_scorers(league_id):
    return f"""
        SELECT p.first_name || ' ' || p.last_name AS "Игрок", COUNT(g.goal_id) AS "Голов"
        FROM Goals g
        JOIN Players p ON g.player_id = p.player_id
        JOIN Teams t ON p.team_id = t.team_id
        WHERE t.league_id = {league_id} AND g.is_own_goal = 0
        GROUP BY p.player_id
        ORDER BY "Голов" DESC
        LIMIT 5
    """

# 3. Статистика команд
def query_team_statistics(league_id):
    return f"""
        SELECT t.name AS "Команда",
            SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score > m.away_team_score)
                      OR (m.away_team_id = t.team_id AND m.away_team_score > m.home_team_score) THEN 1 ELSE 0 END) AS "Побед",
            SUM(CASE WHEN (m.home_team_id = t.team_id AND m.home_team_score < m.away_team_score)
                      OR (m.away_team_id = t.team_id AND m.away_team_score < m.home_team_score) THEN 1 ELSE 0 END) AS "Поражений",
            SUM(CASE WHEN m.home_team_score = m.away_team_score THEN 1 ELSE 0 END) AS "Ничьих"
        FROM Teams t
        LEFT JOIN Matches m ON t.team_id = m.home_team_id OR t.team_id = m.away_team_id
        WHERE m.match_status = 'completed' AND t.league_id = {league_id}
        GROUP BY t.team_id
        ORDER BY "Побед" DESC
    """

# 4. Тренеры команд
def query_coaches_per_team(league_id):
    return f"""
        SELECT c.first_name || ' ' || c.last_name AS "Тренер", t.name AS "Команда", c.nationality AS "Национальность"
        FROM Coaches c
        LEFT JOIN Teams t ON c.team_id = t.team_id
        WHERE t.league_id = {league_id}
        ORDER BY t.name
    """

# 5. Игроки команды
# def query_players_by_team(team_id):
#     return f"""
#         SELECT p.first_name || ' ' || p.last_name AS "Игрок", p.position_id AS "Позиция", p.jersey_number AS "Номер"
#         FROM Players p
#         WHERE p.team_id = {team_id}
#         ORDER BY p.jersey_number
#     """
def query_players_by_team(team_id):
    return f"""
        SELECT p.first_name || ' ' || p.last_name AS "Игрок",
               p.jersey_number AS "Номер"
        FROM Players p
        WHERE p.team_id = {team_id}
        ORDER BY p.jersey_number
    """

# 6. Последние матчи команды
def query_recent_matches(team_id):
    return f"""
        SELECT m.match_date AS "Дата",
               ht.name || ' ' || m.home_team_score || '-' || m.away_team_score || ' ' || at.name AS "Матч",
               m.match_status AS "Статус"
        FROM Matches m
        JOIN Teams ht ON m.home_team_id = ht.team_id
        JOIN Teams at ON m.away_team_id = at.team_id
        WHERE m.home_team_id = {team_id} OR m.away_team_id = {team_id}
        ORDER BY m.match_date DESC
        LIMIT 5
    """

# 7. Контракты игроков
def query_player_contracts(team_id):
    return f"""
        SELECT p.first_name || ' ' || p.last_name AS "Игрок", t.name AS "Команда", p.contract_end_date AS "Окончание контракта"
        FROM Players p
        JOIN Teams t ON p.team_id = t.team_id
        WHERE t.team_id = {team_id}
        ORDER BY p.contract_end_date DESC
    """

# 8. Самые результативные матчи
def query_highest_scoring_matches():
    return """
        SELECT m.match_date AS "Дата",
               ht.name || ' - ' || at.name AS "Матч",
               m.home_team_score || ':' || m.away_team_score AS "Счет",
               (m.home_team_score + m.away_team_score) AS "Всего голов"
        FROM Matches m
        JOIN Teams ht ON m.home_team_id = ht.team_id
        JOIN Teams at ON m.away_team_id = at.team_id
        ORDER BY "Всего голов" DESC
        LIMIT 10
    """

# 9. Топ команд по трофеям
def query_top_teams_by_titles():
    return """
        SELECT t.name AS "Команда", COUNT(tr.trophy_id) as "Трофеев"
        FROM Teams t
        LEFT JOIN Trophies tr ON t.team_id = tr.team_id
        GROUP BY t.team_id
        ORDER BY "Трофеев" DESC
        LIMIT 10
    """

# 10. Игроки с истекающими контрактами
def query_expiring_contracts(days_range):
    from datetime import datetime, timedelta
    end_date = (datetime.now() + timedelta(days=days_range)).strftime("%Y-%m-%d")
    return f"""
        SELECT p.first_name || ' ' || p.last_name AS "Игрок", t.name AS "Команда", p.contract_end_date AS "Окончание контракта"
        FROM Players p
        JOIN Teams t ON p.team_id = t.team_id
        WHERE p.contract_end_date BETWEEN date('now') AND '{end_date}'
        ORDER BY p.contract_end_date
    """

# 11. Топ-10 лучших защит (по наименьшему количеству пропущенных голов)
def query_top_defensive_teams():
    return """
        SELECT t.name AS "Команда",
               SUM(CASE WHEN m.home_team_id = t.team_id THEN m.away_team_score ELSE m.home_team_score END) AS "Пропущено"
        FROM Matches m
        JOIN Teams t ON t.team_id IN (m.home_team_id, m.away_team_id)
        GROUP BY t.team_id
        ORDER BY "Пропущено" ASC
        LIMIT 10
    """

# 12. Игроки без клуба
def query_players_without_club():
    return """
        SELECT first_name || ' ' || last_name AS "Игрок",
               contract_end_date AS "Окончание контракта"
        FROM Players
        WHERE team_id IS NULL
        ORDER BY contract_end_date
    """