"""
aiohttp server

Docs: http://aiohttp.readthedocs.io/en/stable/index.html
"""
from aiohttp import web
import asyncio

from .Hooks import Hooks

class Server:
    """
    Easy to use Server Class

    Create Server
    >>> server = Server(port)

    Start Server
    >>> server.run()
    """

    PORT = None

    hooks = Hooks()

    def __init__(self, port):
        """
        Initiate Server with startup params.

        :param port integer: Port for aiohttp web server
        """
        self.PORT = port

    async def callback(self, request):
        """
        Process action on callback
        
        :param request:
        """

        # get request uri
        uri = str(request.rel_url)

        # return 404 if no function on this route
        if not uri in self.hooks.get():
            return web.Response(text='404: Not found', status=404)

        # get hook function and params
        hook = self.hooks.get(uri)
        hook_function = hook['processor']
        hook_params = hook['params']

        # run hook function
        if hook_params:
            callback_response = await hook_function(request, hook_params) or {}
        else:
            callback_response = await hook_function(request) or {}

        # prepare web response
        if callback_response.get('text'):
            callback_response['content_type'] = callback_response.get('content_type', 'text/plain')
            callback_response['charset'] = callback_response.get('charset', 'utf-8')

        response = web.Response(
            body=callback_response.get('body'),
            status=callback_response.get('status', 200),
            headers=callback_response.get('headers'),
            text=callback_response.get('text'),
            content_type=callback_response.get('content_type'),
            charset=callback_response.get('charset')
        )

        return response


    def run(self):
        """
        Run web app on your server
        """
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        app.router.add_resource('/{uri}').add_route('*', self.callback)
        web.run_app(app, port=self.PORT)
