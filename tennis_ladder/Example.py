from DBInit import DBInit
from repository.PlayerRepository import PlayerRepository
from service.PlayerService import PlayerService
from controller.PlayerController import PlayerController

db_init = DBInit()
session = db_init.session

player_repository = PlayerRepository(session)
player_service = PlayerService(player_repository)
player_controller = PlayerController(player_service)

if __name__ == "__main__":
    player_controller.create_player("Novak Djokovic", 1)
#giannis test
#deytero test