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
        self.board_sliced = np.zeros((5, 5))

    def get_input(self, board):

        if self.response == VICTORY:
            print('You win!')

        elif self.response == GAME_OVER:
            print('You clicked a bomb, you lose')


        super().get_input(board)

        # index_min = np.argmin(self.bomb_probs)
        # y, x = np.unravel_index(index_min, self.bomb_probs.shape)
        #
        # print(y, x)

        y_max, x_max = self._get_probs_argmax()

        if self.bomb_probs[y_max, x_max] == 1:
            func = 'right_click_square'
            x = x_max
            y = y_max
            self.bomb_probs[y, x] = np.nan
            return func, x, y

        #print(self.board_sliced)
        break_loop = False

        for row in range(self.board_height):
            for col in range(self.board_width):
                #print(row, col)

                self.bomb_prob_update(board, col, row)

                if self.bomb_probs[row, col] in [1, 0]:
                    print(self.bomb_probs[row, col], row, col)
                    break_loop = True
                    break
            if break_loop:
                break

        index_min = np.nanargmin(self.bomb_probs)
        y_max, x_max = self._get_probs_argmax()

        if self.bomb_probs[y_max, x_max] == 1:
            func = 'right_click_square'
            x = x_max
            y = y_max
            print(func, x, y, self.bomb_probs[y, x])
            self.bomb_probs[y, x] = np.nan
        else:
            func = 'left_click_square'
            y, x = np.unravel_index(index_min, self.bomb_probs.shape)
            print(func, x, y, self.bomb_probs[y, x])
            self.bomb_probs[y, x] = np.nan

        #print(self.bomb_probs)
        #print(func, x, y)
        return func, x, y

    def set_response(self, response):
        #print(self.response)
        self.response = response


    def bomb_probs_array_splicer(self, board, x, y):
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if self._x_is_in_bounds(x + dx) and self._y_is_in_bounds(y + dy):
                    self.board_sliced[dy + 2, dx + 2] = board[y + dy, x + dx]
                else:
                    self.board_sliced[dy + 2, dx + 2] = board_codes.OUT_OF_BOUNDS

    def bomb_prob_update(self, board, x, y):

        if board[y, x] != board_codes.HIDDEN:
            self.bomb_probs[y, x] = np.nan
            return

        self.bomb_probs_array_splicer(board, x, y)
        #print(self.board_sliced)

        assert board[y, x] == board_codes.HIDDEN
        assert self.board_sliced[2, 2] == board_codes.HIDDEN

        #need to add bomb prob update logic here

        #print(self.board_sliced)
        for row_middle in range(1, 4):
            for col_middle in range(1, 4):

                #print(self.board_sliced[row_middle, col_middle], row_middle, col_middle)

                if (row_middle, col_middle) == (2,2):
                    continue
                elif self.board_sliced[row_middle, col_middle] == board_codes.HIDDEN or self.board_sliced[row_middle, col_middle] == board_codes.OUT_OF_BOUNDS or self.board_sliced[row_middle, col_middle] == board_codes.FLAG:
                    #print(self.board_sliced[row_middle, col_middle], row_middle, col_middle)
                    continue

                hidden_square_count = 0
                flag_count = 0

                self.bomb_probs[y, x] = 0.1

                for row_small in range(-1, 2):
                    for coll_small in range(-1, 2):
                        if self.board_sliced[row_middle + row_small, col_middle + coll_small] == board_codes.HIDDEN:
                            hidden_square_count += 1
                        if self.board_sliced[row_middle + row_small, col_middle + coll_small] == board_codes.FLAG:
                            flag_count += 1

                if hidden_square_count + flag_count == self.board_sliced[row_middle, col_middle]:
                    self.bomb_probs[y, x] = 1
                    return
                elif flag_count == self.board_sliced[row_middle, col_middle]:
                    self.bomb_probs[y, x] = 0
                    return
                else:
                    #print(hidden_square_count/self.board_sliced[row_middle, col_middle])
                    self.bomb_probs[y, x] = max(self.bomb_probs[y, x], (self.board_sliced[row_middle, col_middle] - flag_count)/hidden_square_count)
                    assert self.bomb_probs[y, x] <= 1, (self.bomb_probs, self.bomb_probs[y, x], self.board_sliced[row_middle, col_middle],hidden_square_count, flag_count)

        return

    def _get_probs_argmax(self):
        index_max = np.nanargmax(self.bomb_probs)
        y_max, x_max = np.unravel_index(index_max, self.bomb_probs.shape)

        return y_max, x_max

    def _x_is_in_bounds(self, x):
        return 0 <= x < self.board_width

    def _y_is_in_bounds(self, y):
        return 0 <= y < self.board_height



if __name__ == '__main__':
    pass
    #autosolve()

