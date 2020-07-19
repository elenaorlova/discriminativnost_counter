from django.db import models


# Create your models here.


class ModelsTypes(models.Model):
    type_name = models.CharField(max_length=200)
    type_name_ru = models.CharField(max_length=200)

    def __str__(self):
        return self.type_name_ru


class ScoresTypes(models.Model):
    type_name = models.CharField(max_length=200)
    type_name_ru = models.CharField(max_length=200)

    def __str__(self):
        return self.type_name_ru


class Tests(models.Model):
    test_uid = models.CharField(max_length=200)

    def __str__(self):
        return self.test_uid


class PythonModels(models.Model):
    model_file = models.FileField(upload_to='Python_models/')
    model_name = models.CharField(max_length=200)
    type = models.ForeignKey(ModelsTypes, on_delete=models.CASCADE)
    count_params = models.IntegerField()
    enabled_tests = models.ManyToManyField(Tests, through='TestsModels', through_fields=('model', 'test'))
    score_type = models.ForeignKey(ScoresTypes, on_delete=models.CASCADE)
    score = models.FloatField()
    is_universal = models.BinaryField()

    def __str__(self):
        return self.model_name

    def count_params_model(self):  # можно свои делать, но мне пока не нужно
        return self.count_params


class TestsModels(models.Model):
    model = models.ForeignKey(PythonModels, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    def __str__(self):
        string = str(self.test) + ' ' + str(self.model)
        return string
