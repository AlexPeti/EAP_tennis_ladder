import os
from db_utils.DBUtils import DBUtils

# We need the Match and Player imports, otherwise the db schema will not create the matches and players tables
from entity.Match import Match
from entity.Player import Player
from entity.LeagueRound import LeagueRound

class DBInit:
    def __init__(self):
        project_root = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(project_root, 'tennis_ladder.db')
        self.db_url = f"sqlite:///{db_path}"
        self.engine, self.session = DBUtils.create_engine_and_session(self.db_url)

    def create_db(self):
        DBUtils.create_tables(self.engine)
        print("Database and tables created successfully")

    def insert_initial_players(self):
        players = [
            "Novak Djokovic", "Margaret Court", "Rafael Nadal", "Serena Williams",
            "Steffi Graf", "Roger Federer", "Helen Wills", "Martina Navratilova", "Chris Evert", "Billie Jean King",
            "Roy Emerson", "Rod Laver", "Bill Tilden", "Suzanne Lenglen", "Ken Rosewall", "Maria Sakkari",
            "Naomi Osaka", "Andre Agassi", "Bjorn Borg", "Pete Sampras"
        ]

        player_objects = [Player(name=player_name, rank=i + 1)
                          for i, player_name in enumerate(players)]

        self.session.add_all(player_objects)
        self.session.commit()

    def initialize_db(self):
        self.create_db()
        self.insert_initial_players()

if __name__ == "__main__":
    db_init = DBInit()
    db_init.initialize_db()

