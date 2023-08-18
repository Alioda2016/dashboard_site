from django.contrib import admin

# Register your models here.
from .models import Dataset, Result, Relevant

admin.site.register(Dataset)
admin.site.register(Result)
admin.site.register(Relevant)

