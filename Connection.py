from Config import Config
from ogame import OGame

class Connection():
    def __init__(self, config: Config):
        self.user = config.user()
        self.password = config.password()
        self.universe = config.universe()
        self.language = config.language()
        self.empire = None

    def connect(self):
        if self.empire is None:
            self.empire = OGame(self.universe, self.user, self.password, language=self.language)

        return self.empire