from abc import abstractmethod


class DisplayBase:
    @abstractmethod
    def __init__(self, game):
        pass

    @abstractmethod
    def display(self, board):
        pass
