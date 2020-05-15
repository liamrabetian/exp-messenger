from werkzeug.wrappers import Response 


def create_html_response(content): 
    headers = {'Content-Type': 'text/html'} 
    return Response(content, status=200, headers=headers) 
