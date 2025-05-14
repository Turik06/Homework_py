import sys
import requests_db
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableView, QLabel, QPushButton, QComboBox,
                             QHeaderView, QMessageBox, QGroupBox, QFormLayout, QLineEdit)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import Qt

class SportsLeagueApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sports League Database")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("sports_league.db")
        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Could not open database.")
            sys.exit(1)

        self.create_leagues_tab()
        self.create_teams_tab()
        self.create_players_tab()
        self.create_coaches_tab()
        self.create_matches_tab()
        self.create_goals_tab()
        self.create_queries_tab()

    def create_table_tab(self, title, table_name, headers):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel(title)
        label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(label)

        model = QSqlTableModel()
        model.setTable(table_name)
        model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        model.select()
        for i, header in enumerate(headers):
            model.setHeaderData(i, Qt.Horizontal, header)

        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.setEditTriggers(QTableView.NoEditTriggers)

        layout.addWidget(table_view)
        self.tabs.addTab(tab, title)

    def create_leagues_tab(self):
        headers = ["ID", "Name", "Country", "Founded Year"]
        self.create_table_tab("Leagues", "Leagues", headers)

    def create_teams_tab(self):
        headers = ["ID", "League ID", "Name", "City", "Founded Year"]
        self.create_table_tab("Teams", "Teams", headers)

    def create_players_tab(self):
        headers = ["ID", "Team ID", "First Name", "Last Name", "Birth Date",
                   "Nationality", "Jersey", "Height", "Weight",
                   "Joined", "Contract End", "Photo"]
        self.create_table_tab("Players", "Players", headers)

    def create_coaches_tab(self):
        headers = ["ID", "Team ID", "First Name", "Last Name", "Birth Date",
                   "Nationality", "Style", "Joined", "Contract End", "Photo"]
        self.create_table_tab("Coaches", "Coaches", headers)

    def create_matches_tab(self):
        headers = ["ID", "Season ID", "Home Team", "Away Team", "Date",
                   "Home Score", "Away Score", "Status", "Attendance", "Referee"]
        self.create_table_tab("Matches", "Matches", headers)

    def create_goals_tab(self):
        headers = ["ID", "Match ID", "Player ID", "Team ID", "Minute",
                   "Penalty", "Own Goal"]
        self.create_table_tab("Goals", "Goals", headers)

    def create_queries_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        label = QLabel("Запросы")
        label.setStyleSheet("font-size: 16pt; font-weight: bold;")
        layout.addWidget(label)

        params_group = QGroupBox("Параметры")
        params_layout = QFormLayout()

        self.query_combo = QComboBox()
        self.query_combo.addItems([
            "1. Все лиги с командами",
            "2. Топ-5 бомбардиров лиги",
            "3. Статистика команд",
            "4. Тренеры команд",
            "5. Игроки команды",
            "6. Последние матчи команды",
            "7. Контракты игроков",
            "8. Самые результативные матчи",
            "9. Топ команд по трофеям",
            "10. Игроки с истекающими контрактами",
            "11. Топ-10 лучших защит",
            "12. Игроки без клуба"
        ])

        self.league_combo = QComboBox()
        self.league_combo.setPlaceholderText("Выберите лигу")
        self.populate_leagues()
        self.league_combo.currentIndexChanged.connect(self.populate_teams)

        self.team_combo = QComboBox()
        self.team_combo.setPlaceholderText("Выберите команду")

        self.days_input = QLineEdit()
        self.days_input.setPlaceholderText("Дней до окончания контракта (по умолчанию 30)")

        params_layout.addRow("Запрос:", self.query_combo)
        params_layout.addRow("Лига:", self.league_combo)
        params_layout.addRow("Команда:", self.team_combo)
        params_layout.addRow("Диапазон дней:", self.days_input)
        params_group.setLayout(params_layout)

        execute_btn = QPushButton("Выполнить")
        execute_btn.clicked.connect(self.execute_query)
        self.result_view = QTableView()
        self.result_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(params_group)
        layout.addWidget(execute_btn)
        layout.addWidget(self.result_view)
        self.tabs.addTab(tab, "Requests")

    def populate_leagues(self):
        query = QSqlQuery(self.db)
        query.exec_("SELECT league_id, name FROM Leagues ORDER BY name")
        self.league_combo.clear()
        while query.next():
            lid = query.value(0)
            lname = query.value(1)
            self.league_combo.addItem(lname, lid)

    def populate_teams(self):
        lid = self.league_combo.currentData()
        query = QSqlQuery(self.db)
        query.prepare("SELECT team_id, name FROM Teams WHERE league_id = ? ORDER BY name")
        query.addBindValue(lid)
        query.exec_()
        self.team_combo.clear()
        while query.next():
            tid = query.value(0)
            tname = query.value(1)
            self.team_combo.addItem(tname, tid)

    def execute_query(self):
        idx = self.query_combo.currentIndex()
        league_id = self.league_combo.currentData() or 1
        team_id = self.team_combo.currentData() or 1
        days_range = int(self.days_input.text()) if self.days_input.text().isdigit() else 30

        model = QSqlQueryModel()
        try:
            if idx == 0:
                model.setQuery(requests_db.query_leagues_with_teams(), self.db)
            elif idx == 1:
                model.setQuery(requests_db.query_top_scorers(league_id), self.db)
            elif idx == 2:
                model.setQuery(requests_db.query_team_statistics(league_id), self.db)
            elif idx == 3:
                model.setQuery(requests_db.query_coaches_per_team(league_id), self.db)
            elif idx == 4:
                model.setQuery(requests_db.query_players_by_team(team_id), self.db)
            elif idx == 5:
                model.setQuery(requests_db.query_recent_matches(team_id), self.db)
            elif idx == 6:
                model.setQuery(requests_db.query_player_contracts(team_id), self.db)
            elif idx == 7:
                model.setQuery(requests_db.query_highest_scoring_matches(), self.db)
            elif idx == 8:
                model.setQuery(requests_db.query_top_teams_by_titles(), self.db)
            elif idx == 9:
                model.setQuery(requests_db.query_expiring_contracts(days_range), self.db)
            elif idx == 10:
                model.setQuery(requests_db.query_top_defensive_teams(), self.db)
            elif idx == 11:
                model.setQuery(requests_db.query_players_without_club(), self.db)

            self.result_view.setModel(model)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка запроса", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SportsLeagueApp()
    window.show()
    sys.exit(app.exec_())