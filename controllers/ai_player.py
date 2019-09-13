"""

This file as an automatic program to solve the minesweeper board

"""

from game_engine import Game

from board_displays import TerminalDisplay


def autosolve():
    game = Game(5, 5)
    display = TerminalDisplay(game.get_board())

    #exit_code =
