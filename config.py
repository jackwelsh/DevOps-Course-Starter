import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration variables."""

    def __init__(self):
        self.TESTING = os.environ.get('TESTING')
        self.TRELLO_KEY = os.environ.get('TRELLO_KEY')
        self.TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')
        self.TRELLO_BOARD = os.environ.get('TRELLO_BOARD')
