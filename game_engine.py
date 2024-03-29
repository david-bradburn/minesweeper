import numpy as np

from response_codes import *

import board_codes


class Game:
    def __init__(self, board_width=10, board_height=10, bomb_density=0.1):
        assert isinstance(board_width, int)
        assert isinstance(board_height, int)
        assert isinstance(bomb_density, float)
        assert 0 < bomb_density < 1

        self.board_width = board_width
        self.board_height = board_height
        self.bomb_density = bomb_density

        self._build_board(bomb_density)
        self._vision_mask = np.zeros_like(self._board, dtype='bool')
        self.flag_mask = np.zeros_like(self._board, dtype='bool')

        self._game_over = False

    def get_board(self):
        """
        Returns:
            The game board as visible to the player
        """
        board = np.copy(self._board)
        board = np.where(self._vision_mask, board, board_codes.HIDDEN, )
        board = np.where(self.flag_mask, board_codes.FLAG, board, )
        return board

    ################################################
    # Actions
    ################################################

    def left_click_square(self, x, y):
        if not (self._x_is_in_bounds(x) and self._y_is_in_bounds(y)):
            # Selected square out of bounds
            return INVALID_ARGS
        elif self.flag_mask[y, x]:
            # Selected square is a flag and cannot be clicked
            return INVALID_ARGS

        # Make square visible
        self._vision_mask[y, x] = True
        self.flag_mask[y, x] = False
        value = self._board[y, x]

        if value == 0:
            # If value is zero, clear tiles around this square (recursively)
            for _x, _y in self._get_squares_around(x, y):
                if not self._vision_mask[_y, _x]:
                    game_over = self._game_over
                    _ = self.left_click_square(_x, _y)
                    # Check we have not failed the game
                    assert game_over == self._game_over

        if value == board_codes.BOMB:
            # If bomb set game over
            self._game_over = True

        # Return
        if self._game_over:
            print("GAME_OVER")
            return GAME_OVER

        if self._check_win_condition():
            return VICTORY

        return SUCCESS

    def right_click_square(self, x, y):
        if not (self._x_is_in_bounds(x) and self._y_is_in_bounds(y)):
            # Selected square out of bounds
            return INVALID_ARGS

        if self._vision_mask[y, x]:
            return INVALID_ARGS

        self.flag_mask[y, x] = not self.flag_mask[y, x]
        return SUCCESS

    ################################################
    # Private methods
    ################################################

    def _build_board(self, bomb_density):
        self._board = np.zeros((self.board_height, self.board_width), dtype='int8')
        xx, yy = np.meshgrid(np.arange(self.board_width), np.arange(self.board_height))

        coords = list(zip(np.ravel(xx), np.ravel(yy)))

        for x, y in coords:
            if np.random.random() < bomb_density:
                self._board[y, x] = board_codes.BOMB

        for x, y in coords:
            if self._board[y, x] < board_codes.BOMB:
                self._board[y, x] = self._count_bombs_around(x, y)

        # Calculate once, as this does not change
        self._bomb_position_mask = self._board == board_codes.BOMB

    def _count_bombs_around(self, x, y):
        count = 0
        for _x, _y in self._get_squares_around(x, y):
            if self._board[_y, _x] == board_codes.BOMB:
                count += 1
        return count

    def _get_squares_around(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                test_x = x + dx
                test_y = y + dy
                if self._x_is_in_bounds(test_x) and self._y_is_in_bounds(test_y):
                    yield test_x, test_y

    def _x_is_in_bounds(self, x):
        return 0 <= x < self.board_width

    def _y_is_in_bounds(self, y):
        return 0 <= y < self.board_height

    def _check_win_condition(self):
        return np.all(np.bitwise_xor(self._bomb_position_mask, self._vision_mask))
