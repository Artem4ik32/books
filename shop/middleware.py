class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Request received")

        response = self.get_response(request)

        print("Response sent")

        return response
