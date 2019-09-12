import pygame

from displays.displaybase import DisplayBase


class Display(DisplayBase):
    pixels_per_square = 5
    gridline_width = 1

    def __init__(self, game):
        super().__init__(game)

        screenwidth = game.board_width * self.pixels_per_square + (game.board_width - 1) * self.gridline_width
        screenheight = game.board_height * self.pixels_per_square + (game.board_height - 1) * self.gridline_width

        self.screen = pygame.display.set_mode((screenwidth, screenheight))

    def display(self, board):
        pass
