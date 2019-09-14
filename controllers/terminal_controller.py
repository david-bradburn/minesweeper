from controllers.controller_base import ControllerBase

from response_codes import *


class Controller(ControllerBase):
    def get_input(self, board):

        if self.response == VICTORY:
            print('You win!')
            exit()
        elif self.response == GAME_OVER:
            print('You clicked a bomb, you lose')
            exit()

        super().get_input(board)

        right_or_left_click = input("Right or Left click? r/l")
        if right_or_left_click == 'l':
            func = 'left_click_square'
        else:
            func = 'right_click_square'

        x = input_coord_int("x")
        y = input_coord_int("y")


        return func, x, y


def input_coord_int(variable_name):  # type is simply to print to thr user to tell them what coordinate to enter
    try:
        return int(input("Enter {}".format(variable_name)))
    except ValueError:
        print("Please enter an integer")
        return input_coord_int(variable_name)
