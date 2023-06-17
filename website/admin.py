from django.contrib import admin
from .models import FormTemplate, Form, Question, FormResponse, AudioFile, FormConfig

# Register your models here.
admin.site.register(FormTemplate)
admin.site.register(Form)
admin.site.register(Question)
admin.site.register(FormResponse)
admin.site.register(AudioFile)
admin.site.register(FormConfig)