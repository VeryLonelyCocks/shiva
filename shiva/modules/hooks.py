class Hooks:
    """
    Hooks class for Server

    Register hook
    >>> core.server.hooks.add('/mycallbackurl', callbackfunction, {'param1': param1})

    Get hook
    >>> core.server.hooks.get('/mycallbackurl')

    Remove hook
    >>> core.server.hooks.remove('/mycallbackurl')
    """

    List = {}

    def __init__(self):
        pass

    def get(self, uri=''):
        """
        Get hook params by uri

        :param string uri: request uri
        :return dict: hook params
        :return list: all hooks if no uri
        """
        if uri:
            return self.List[uri] or None
        return self.List

    def add(self, uri, processor, params={}):
        """
        Register new hook

        :param string uri: request uri
        :param function processor: callback
        :param dict params: callback params if need
        """
        self.List[uri] = {
            'processor': processor,
            'params': params
        }

    def remove(self, uri):
        """
        Unlink hook by uri

        :param string uri: hook uri
        """
        del self.List[uri]
