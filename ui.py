import importlib
import json
import os

from game_engine import Game

from displays.terminal_display import Display


def input_int(variable_name):  # type is simply to print to thr user to tell them what coordinate to enter
    try:
        return int(input("Enter {}".format(variable_name)))
    except ValueError:
        print("Please enter an integer")
        return input_int(variable_name)


def read_config():
    with open(os.path.join(os.path.dirname(__file__), "config.json"), 'r') as f:
        config = json.load(f)
    return config


if __name__ == '__main__':
    cfg = read_config()

    game = Game(5, 5)

    # setup display
    display_module = importlib.import_module("displays." + cfg["display"])
    display = display_module.Display()
    while True:
        display.display(game.get_board())
        x = input_int("x")
        y = input_int("y")
        exit_code = game.click_square(x, y)
        if exit_code == 1:
            print("GAME OVER")
            break
        elif exit_code == 3:
            print("Well done, you've won the game!")
            break
