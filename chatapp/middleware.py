import json

from django.http import HttpResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health':
            s = {'status': 200,
                 'message': 'OK'}
            return HttpResponse(status=200, content=json.dumps(s),
                                content_type='application/json')
        return self.get_response(request)