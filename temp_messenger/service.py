from nameko.rpc import rpc

class HelloService:

    name = 'hello_service'

    @rpc
    def hello(self):
        return 'hello!'
