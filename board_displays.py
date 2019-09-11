import colorama


class TerminalDisplay:
    def __init__(self):
        pass

    def display(self, board):
        for row in board:
            for val in row:
                colors = ""
                if val == 0:
                    val = "///"
                elif val == 101:
                    val = " X "
                    colors += colorama.Back.WHITE + colorama.Fore.BLACK
                elif val == 100:
                    colors += colorama.Fore.RED
                    val = " B "
                elif 1 <= val <= 8:
                    val = f" {val} "

                val = str(val)

                assert len(val) <= 3, f"val greater than length 3 {val}"

                print(f"{colors}{val:3s}", end="")
                print(colorama.Back.RESET + colorama.Fore.RESET, end="")
            print("")