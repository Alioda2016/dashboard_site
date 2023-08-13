from django.db import models


# Create your models here.

class Dataset(models.Model):
    text = models.TextField()
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.username


class Result(models.Model):
    text = models.TextField()
    output = models.BooleanField()
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.text
