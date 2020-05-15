from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http

class HelloService:

    name = 'hello_service'

    @rpc
    def hello(self):
        return 'hello!'


class WebServer:

    name = 'web_server'
    hello_service = RpcProxy('hello_service')

    @http('GET', '/')
    def home(self, request):
        return self.hello_service.hello()
