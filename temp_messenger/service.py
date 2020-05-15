from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http

from .dependencies import MessageStore


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


class MessageService:

    name = 'message_service'
    message_store = MessageStore()

    @rpc
    def get_message(self, message_id):
        return self.message_store.get_message(message_id)
