"""

This file as an automatic program to solve the minesweeper board

"""

from game_engine import Game

from displays.terminal_display import Display

import numpy as np

from controllers.controller_base import ControllerBase
from response_codes import  *


class Controller(ControllerBase):
    def __init__(self, game):
        super().__init__(game)
        self.baord_width = game.board_width
        self.board_height = game.board_height
        self.bomb_probs = np.ones_like(game.get_board()) * game.bomb_density

    def get_input(self, board):
        super().get_input(board)

        index = np.argmin(self.bomb_probs)
        y, x = np.unravel_index(index, self.bomb_probs.shape)

        print(y, x)


        return "left_click_square", x, y

    def set_response(self, response):
        self.response = response
        if self.response == GAME_OVER:
            exit()

    def bomb_prob_update(self):
        for 



def random_click(game):
    return game.left_click_square(
        )


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

