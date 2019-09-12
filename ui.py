from game_engine import Game

from board_displays import TerminalDisplay


def input_int(variable_name):  # type is simply to print to thr user to tell them what coordinate to enter
    try:
        return int(input("Enter {}".format(variable_name)))
    except ValueError:
        print("Please enter an integer")
        return input_int(variable_name)


if __name__ == '__main__':
    game = Game(5, 5)
    display = TerminalDisplay()
    while True:
        display.display(game.get_board())
        x = input_int("x")
        y = input_int("y")
        exit_code = game.click_square(x, y)
        if exit_code == 1:
            print("GAME OVER")
            break
        elif exit_code == 3:
            print("Well done, you've won the game!")
            break
