import importlib

from game_engine import Game
from utils import read_config

# initialise a game



cfg = read_config()

game = Game(cfg["board_width"], cfg["board_height"])

# setup display
display_module = importlib.import_module("displays." + cfg["display"])
display = display_module.Display(game)

# setup controller
controller_module = importlib.import_module("controllers." + cfg["controller"])
controller = controller_module.Controller(game)


while True:
    display.display(game.get_board())
    action, *args = controller.get_input(game.get_board())
    response = getattr(game, action)(*args)
    controller.set_response(response)
