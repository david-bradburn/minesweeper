import colorama

from displays.displaybase import DisplayBase


class Display(DisplayBase):
    color_dict = {
        1: colorama.Fore.BLUE,
        2: colorama.Fore.GREEN,
        3: colorama.Fore.RED,
        4: colorama.Fore.BLACK,
        5: colorama.Fore.MAGENTA,
        6: colorama.Fore.LIGHTBLUE_EX,
        7: colorama.Fore.BLACK,
        8: colorama.Fore.LIGHTYELLOW_EX,
    }

    def display(self, board):
        print("  " + "".join(["{:3}".format(i) for i in range(len(board[0, :]))]))
        for r, row in enumerate(board):
            print(f"{r:2} ", end="")
            for val in row:
                colors = ""
                if val == 0:
                    colors += colorama.Back.WHITE
                    val = "///"
                elif val == 101:
                    colors += colorama.Back.LIGHTWHITE_EX + colorama.Fore.BLACK
                    val = " X "
                elif val == 100:
                    colors += colorama.Back.RED + colorama.Fore.BLACK
                    val = " X "
                elif 1 <= val <= 8:
                    colors += colorama.Back.LIGHTWHITE_EX + self.color_dict[val]
                    val = f" {val} "

                val = str(val)

                assert len(val) <= 3, f"val greater than length 3 {val}"

                print(f"{colors}{val:3s}", end="")
                print(colorama.Back.RESET + colorama.Fore.RESET, end="")
            print("")
