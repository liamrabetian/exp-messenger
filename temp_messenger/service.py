import json

from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http

from .dependencies import MessageStore, Jinja2
from .helpers import create_html_response, sort_messages_by_expiry


class HelloService:

    name = "hello_service"

    @rpc
    def hello(self):
        return "hello!"


class WebServer:

    name = "web_server"
    hello_service = RpcProxy("hello_service")
    message_service = RpcProxy("message_service")
    templates = Jinja2()

    @http("GET", "/hello")
    def hello(self, request):
        return self.hello_service.hello()

    @http("GET", "/")
    def home(self, request):
        messages = self.message_service.get_all_messages()
        rendered_template = self.templates.render_home(messages)
        html_response = create_html_response(rendered_template)
        return html_response

    @http("POST", "/messages")
    def post_message(self, request):
        data_as_text = request.get_data(as_text=True)

        try:
            data = json.loads(data_as_text)
        except json.JSONDecodeError:
            return 400, "JSON payload expected"

        try:
            message = data["message"]
        except KeyError:
            return 400, "No message given"

        self.message_service.save_message(message)

        return 204, ""


class MessageService:

    name = "message_service"
    message_store = MessageStore()

    @rpc
    def get_message(self, message_id):
        return self.message_store.get_message(message_id)

    @rpc
    def save_message(self, message):
        message_id = self.message_store.save_message(message)
        return message_id

    @rpc
    def get_all_messages(self):
        messages = self.message_store.get_all_messages()
        sorted_messages = sort_messages_by_expiry(messages)
        return sorted_messages
