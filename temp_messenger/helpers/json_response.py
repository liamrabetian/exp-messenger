import json

from werkzeug.wrappers import Response


def create_json_response(content):
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(content)
    return Response(json_data, status=200, headers=headers)
