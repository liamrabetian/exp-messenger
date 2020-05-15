from nameko.testing.services import worker_factory
from temp_messenger.service import HelloService, WebServer

# unit test
def test_hello():
    service = worker_factory(HelloService)
    result = service.hello()
    assert result == 'hello!'


# integration test
def test_root_http(web_session, web_config, container_factory):
    web_config['AMQP_URI'] = 'pyamqp://guest:guest@localhost'

    web_server = container_factory(WebServer, web_config)
    hello = container_factory(HelloService, web_config)
    web_server.start()
    hello.start()

    result = web_session.get('/')

    assert result.text == 'hello!'
