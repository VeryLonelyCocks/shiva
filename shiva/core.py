from .modules import Server
from .modules import Database
from .modules import Scheduler
from .modules import Logger, LoggerHandlers
from .modules import Hawk
from .modules import States

from .messengers import Telegram

from .plugins import SelectelCloudStorage
from .plugins import Notifier

class Core:
    """
    Core module will prepare your app
    - get config
    - prepare modules
    - prepare messengers
    - prepare plugins
    """

    def __init__(self, params):
        """
        Initiate Core with startup params.

        :param params dict: config
        """

        self.PARAMS = params

        self.load_modules()
        self.load_messengers()
        self.load_plugins()

    def load_modules(self):

        self.logger = Logger(self).logger

        self.db = Database().get(self.PARAMS['name'])

        """
        Enable loggers
        """
        # LoggerHandlers.add(self, self.logger, ['journal'])
        # LoggerHandlers.add(self, self.logger, ['db'])
        if self.PARAMS.get('hawk'):
            self.hawk = Hawk(self.PARAMS['hawk']).hawk
            LoggerHandlers.add(self, self.logger, ['hawk'])

        self.server = Server(self.PARAMS['port'])
        self.scheduler = Scheduler(self)
        self.states = States(self)

    def load_messengers(self):
        self.telegram = Telegram()

    def load_plugins(self):
        self.selectel = SelectelCloudStorage
        self.notifier = Notifier(self)
