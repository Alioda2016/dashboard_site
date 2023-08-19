from django.contrib import admin

# Register your models here.
from .models import Dataset, Result, Categorical, Relevant

admin.site.register(Dataset)
admin.site.register(Result)
admin.site.register(Categorical)
admin.site.register(Relevant)

