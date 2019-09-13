from abc import abstractmethod


class ControllerBase:
    def __init__(self, game):
        self.response = None

    @abstractmethod
    def get_input(self, board):
        """
        Returns:
            action, *args
            The action that the controller wishes to perform on the game,
            and any arguments needed to take that action
        """
        self.response = None  # Clear the response o the previous action taken

    @abstractmethod
    def set_response(self, response):
        """ Set the response given by the game engine to the previous action """
        self.response = response
