from django.contrib import admin
from .models import PythonModels, ModelsTypes, ScoresTypes, Tests, TestsModels

admin.site.register(PythonModels)
admin.site.register(ModelsTypes)
admin.site.register(ScoresTypes)
admin.site.register(Tests)
admin.site.register(TestsModels)


# Register your models here.
