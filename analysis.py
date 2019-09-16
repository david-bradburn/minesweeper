import importlib

from game_engine import Game
from utils import read_config

from response_codes import *

# initialise a game
cfg = {
    "board_width": 10,
    "board_height": 10,
    "bomb_density": 0.1,
    "display": "pygame_display",
    "controller": "ai_player"
}
game = Game(cfg["board_width"], cfg["board_height"])

# setup display
display_module = importlib.import_module("displays." + cfg["display"])
display = display_module.Display(game)

# setup controller
controller_module = importlib.import_module("controllers." + cfg["controller"])
controller = controller_module.Controller(game)


while True:
    action, *args = controller.get_input(game.get_board())
    response = getattr(game, action)(*args)
    controller.set_response(response)
    display.set_response(response)
    display.display(game.get_board())

    if response in [VICTORY, GAME_OVER]:
        break
