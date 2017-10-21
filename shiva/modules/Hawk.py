from hawkcatcher import Hawk as HawkCatcher


class Hawk:
    """
    Python Hawk Catcher

    https://hawk.so/docs
    """

    def __init__(self, token):
        self.hawk = HawkCatcher(token)
