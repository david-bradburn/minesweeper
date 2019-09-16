import importlib

from game_engine import Game
from utils import read_config

from response_codes import *

import matplotlib.pyplot as plt

import numpy as np

# initialise a game
bomb_densities = np.linspace(0.01, 0.25, 15)


print(bomb_densities)

results = []

cfg = {
    "board_width": 30,
    "board_height": 16,
    "display": "pygame_display",
    "controller": "ai_player"
}

display_module = importlib.import_module("displays." + cfg["display"])
display = None

controller_module = importlib.import_module("controllers." + cfg["controller"])

for bomb_density in bomb_densities:
    cfg["bomb_density"] = bomb_density

    run_no = 30
    win_no = 0

    for i in range(run_no):

        game = Game(cfg["board_width"], cfg["board_height"], cfg["bomb_density"])

        # setup display
        if display is None:
            display = display_module.Display(game)

        # setup controller
        controller = controller_module.Controller(game)
        print("Start")
        while True:
            action, *args = controller.get_input(game.get_board())
            response = getattr(game, action)(*args)
            controller.set_response(response)
            display.display(game.get_board())

            if response == VICTORY:
                win_no += 1
                print("Win")
                break
            elif response == GAME_OVER:
                break

    print(win_no/run_no)
    results += [win_no/run_no]

for i in range(len(results)):
    print(bomb_densities[i], results[i])
plt.plot(bomb_densities, results)
plt.ylim(0, 1)
plt.show()




