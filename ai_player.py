"""

This file as an automatic program to solve the minesweeper board

"""

from game_engine import Game

from displays.terminal_display import Display

import numpy as np


def random_click(game):
    return game.click_square(np.random.randint(0, game.board_width +1), np.random.randint(0, game.board_height + 1))


def autosolve():
    game = Game(10, 10)
    display = Display(game)

    display.display(game.get_board())

    number_of_clicks = 0

    while True:
        assert number_of_clicks < (game.board_height + 1) * (game.board_width + 1) + 1

        print(game.get_board())
        if number_of_clicks == 0:
            exit_code = random_click(game)
        else:
            if np.any(game.get_board() == 0):
                print("Open patch found")
                break
            else:
                exit_code = random_click(game)
        number_of_clicks += 1



        print("No. of clicks {}".format(number_of_clicks))
        display.display(game.get_board())

        if exit_code == 1:
            print("GAME OVER")
            break
        elif exit_code == 3:
            print("Well done, you've won the game!")
            break


if __name__ == '__main__':

    autosolve()

