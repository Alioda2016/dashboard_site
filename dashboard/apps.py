from django.apps import AppConfig
from . import global_vars
#from keras.models import load_model
import ktrain
from ktrain import text

class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
        import dashboard.global_vars
        global_vars.predictor= ktrain.load_predictor('ar-bert-spamda-model')