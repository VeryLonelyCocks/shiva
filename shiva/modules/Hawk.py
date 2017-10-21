from hawkcatcher import Hawk as HawkCatcher


class Hawk:

    def __init__(self, token):
        self.hawk = HawkCatcher(token)
