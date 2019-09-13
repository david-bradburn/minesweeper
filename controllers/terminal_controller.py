from controllers.controller_base import ControllerBase


class Controller(ControllerBase):
    def get_input(self, board):
        super().get_input(board)

        x = input_coord_int("x")
        y = input_coord_int("y")

        return "left_click_square", x, y


def input_coord_int(variable_name):  # type is simply to print to thr user to tell them what coordinate to enter
    try:
        return int(input("Enter {}".format(variable_name)))
    except ValueError:
        print("Please enter an integer")
        return input_coord_int(variable_name)
