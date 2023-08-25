import ktrain
from ktrain import text
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your variable logic here
        predictor = ktrain.load_predictor('ar-bert-spamda-model')
        request.custom_variable = predictor

        response = self.get_response(request)
        return response