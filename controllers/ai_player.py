"""

This file as an automatic program to solve the minesweeper board

"""

from game_engine import Game

from displays.terminal_display import Display

import numpy as np

from controllers.controller_base import ControllerBase
from response_codes import  *
import board_codes


class Controller(ControllerBase):
    def __init__(self, game):
        super().__init__(game)
        self.board_width = game.board_width
        self.board_height = game.board_height
        self.bomb_probs = np.ones_like(game.get_board()) * game.bomb_density
        self.bomb_probs_spliced = np.zeros((5,5))

    def get_input(self, board):
        super().get_input(board)

        # index = np.argmin(self.bomb_probs)
        # y, x = np.unravel_index(index, self.bomb_probs.shape)
        #
        # print(y, x)

        print(self.bomb_probs_spliced)
        for row in range(self.board_height):
            for col in range(self.board_width):

                self.bomb_prob_update(board, col, row)


        return "left_click_square", x, y

    def set_response(self, response):
        self.response = response
        if self.response == GAME_OVER:
            exit()

    def bomb_probs_array_splicer(self, board, x, y):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if self._x_is_in_bounds(x + dx) and self._y_is_in_bounds(y + dy):
                    self.bomb_probs_spliced[dy + 2, dx + 2] = board[y + dy, x + dx]
                else:
                    self.bomb_probs_spliced[dy + 2, dx + 2] = board_codes.OUT_OF_BOUNDS

    def bomb_prob_update(selfb, board, x, y):

        self.bomb_probs_array_splicer(board, x, y)



    def _x_is_in_bounds(self, x):
        return 0 <= x < self.board_width

    def _y_is_in_bounds(self, y):
        return 0 <= y < self.board_height



def random_click(game):
    return game.left_click_square()


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

