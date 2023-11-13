from django.http import HttpResponse


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("origin")
        print(origin)
        if (request.method == "OPTIONS" and "access-control-request-method" in request.headers):
            response = HttpResponse(status=204)
            response["Access-Control-Allow-Origin"] = "true"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
            response["Access-Control-Allow-Headers"] = "X-CSRFToken, Content-Type"
            return response

        print(request.headers)
        response = self.get_response(request)
        print(response)
        response["Access-Control-Allow-Origin"] = origin
        return response
