class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your variable logic here
        custom_value = "Hello from custom variable!"
        request.custom_variable = custom_value

        response = self.get_response(request)
        return response