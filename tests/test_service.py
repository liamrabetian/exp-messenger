from nameko.testing.services import worker_factory
from temp_messenger.service import HelloService


def test_hello():
    service = worker_factory(HelloService)
    result = service.hello()
    assert result == 'hello!'
