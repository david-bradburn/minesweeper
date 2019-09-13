import pygame
import threading

from displays.displaybase import DisplayBase


class Display(DisplayBase):
    pixels_per_square = 100
    gridline_width = 20
    gridline_color = (50, 50, 50)
    square_hidden_color = (70, 70, 70)
    square_revealed_color = (150, 150, 150)

    text_color = (255, 0, 0)

    colors_dict = {
        1: (0, 0, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (0, 0, 127),
        5: (127, 0, 0),
        6: (100, 100, 255),
        7: (0, 0, 0),
        8: (100, 100, 100),
    }

    def __init__(self, game):
        super().__init__(game)

        pygame.font.init()
        self.font = pygame.font.SysFont('Verdana Bold', int(self.pixels_per_square * 0.8))

        self.screen_width = game.board_width * self.pixels_per_square + (game.board_width - 1) * self.gridline_width
        self.screen_height = game.board_height * self.pixels_per_square + (game.board_height - 1) * self.gridline_width

        self.board_height = game.board_height
        self.board_width = game.board_width

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.board = None

        self.display_thread = threading.Thread(target=self._display_thread)
        self.display_thread.start()

    def display(self, board):
        self.board = board

    def _display_thread(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self._display()

    def _display(self):
        self.draw_gridlines()

        if self.board is not None:
            for x in range(self.board_width):
                for y in range(self.board_height):
                    self.draw_square(x, y, self.board[y, x])

        pygame.display.update()

    def draw_square(self, x, y, square_value):
        # Draw background
        x = x * (self.pixels_per_square + self.gridline_width)
        y = y * (self.pixels_per_square + self.gridline_width)
        w = self.pixels_per_square
        h = self.pixels_per_square
        rect = pygame.Rect(x, y, w, h)

        if square_value == 101:
            pygame.draw.rect(self.screen, self.square_hidden_color, rect)
        else:
            pygame.draw.rect(self.screen, self.square_revealed_color, rect)

        # Draw number/flag etc.
        text = None
        if square_value in [101, 0]:
            pass
        elif 0 < square_value <= 8:
            color = self.colors_dict[square_value]
            text = self.font.render(str(square_value), True, color)
        else:
            color = self.text_color
            text = self.font.render(str(square_value), True, color)

        if text:
            self.screen.blit(text, (x, y))





    def draw_gridlines(self):
        for i in range(self.board_width - 1):
            x = self.pixels_per_square + i * (self.pixels_per_square + self.gridline_width)
            rect = pygame.Rect((x, 0), (self.gridline_width, self.screen_height))
            pygame.draw.rect(self.screen, self.gridline_color, rect)
        for i in range(self.board_width - 1):
            y = self.pixels_per_square + i * (self.pixels_per_square + self.gridline_width)
            rect = pygame.Rect((0, y), (self.screen_width, self.gridline_width))
            pygame.draw.rect(self.screen, self.gridline_color, rect)