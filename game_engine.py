import numpy as np

from display import TerminalDisplay

class Game:
    def __init__(self, board_width=10, board_height=5, bomb_density=0.1):
        assert isinstance(board_width, int)
        assert isinstance(board_height, int)
        assert isinstance(bomb_density, float)
        assert 0 < bomb_density < 1

        self._board_width = board_width
        self._board_height = board_height

        self._build_board(bomb_density)
        self._vision_mask = np.zeros_like(self._board, dtype='bool')

        self._game_over = False

    def _build_board(self, bomb_density):
        self._board = np.zeros((self._board_height, self._board_width), dtype='int8')
        xx, yy = np.meshgrid(np.arange(self._board_width), np.arange(self._board_height))

        coords = list(zip(np.ravel(xx), np.ravel(yy)))

        for x, y in coords:
            if np.random.random() < bomb_density:
                self._board[y, x] = 100

        for x, y in coords:
            if self._board[y, x] < 100:
                self._board[y, x] = self._count_bombs_around(x, y)

    def _count_bombs_around(self, x, y):
        count = 0
        for _x, _y in self._get_squares_around(x, y):
            if self._board[_y, _x] == 100:
                count += 1
        return count

    def _get_squares_around(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                test_x = x + dx
                test_y = y + dy
                if self.x_is_in_bounds(test_x) and self.y_is_in_bounds(test_y):
                    yield test_x, test_y

    def get_board(self):
        board = np.copy(self._board)
        board = np.where(self._vision_mask, board, 101, )
        return board

    def click_square(self, x, y):
        if not (self.x_is_in_bounds(x) and self.y_is_in_bounds(y)):
            # Selected square out of bounds
            return 2

        # Make square visible
        self._vision_mask[y, x] = True
        value = self._board[y, x]

        if value == 0:
            # If value is zero, clear tiles around this square (recursively)
            for _x, _y in self._get_squares_around(x, y):
                if not self._vision_mask[_y, _x]:
                    game_over = self._game_over
                    status_code = self.click_square(_x, _y)
                    # Check we have not failed the game
                    assert game_over == self._game_over

        if value == 100:
            # If bomb set game over
            self._game_over = True

        # Return
        if self._game_over:
            return 1
        return 0

    def x_is_in_bounds(self, x):
        return 0 <= x < self._board_width

    def y_is_in_bounds(self, y):
        return 0 <= y < self._board_height


if __name__ == '__main__':
    game = Game()
    display = TerminalDisplay()
    while True:
        display.display(game.get_board())
        x = int(input("Enter x"))
        y = int(input("Enter y"))
        exit_code = game.click_square(x, y)
        if exit_code == 1:
            print("GAME OVER")
