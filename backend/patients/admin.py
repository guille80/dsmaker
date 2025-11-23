from django.contrib import admin
from .models import Patient, Study, Series, ImageInstance

admin.site.register(Patient)
admin.site.register(Study)
admin.site.register(Series)
admin.site.register(ImageInstance)
