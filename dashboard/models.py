from django.db import models
from datetime import datetime


# Create your models here.

class Dataset(models.Model):
    text = models.TextField()
    predicted = models.BooleanField(default=False)
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return self.username


class Result(models.Model):
    text = models.TextField()
    output = models.BooleanField()
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateTimeField()
    user_count = models.IntegerField(default=0)  # New field for user count

    def __str__(self):
        return self.username

    def update_user_count(self):
        print(f"Updating user count for username: {self.username}")

        user_false_count = Result.objects.filter(username=self.username, output=False).count()
        self.user_count = user_false_count
        self.save()


class Relevant(models.Model):
    text = models.TextField()
    spam = models.BooleanField()
    relevant = models.BooleanField()
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateTimeField()
    user_count = models.IntegerField(default=0)  # New field for user count

    def __str__(self):
        return self.username + " " + str(self.user_count)

    def update_user_count(self):
        print(f"Updating user count for username: {self.username}")
        user_false_count = Relevant.objects.filter(username=self.username, relevant=False).count()
        self.user_count = user_false_count
        self.save()


class Categorical(models.Model):
    text = models.TextField()
    id = models.CharField(max_length=100, primary_key=True)
    username = models.CharField(max_length=100)
    date = models.DateTimeField()
    category = models.IntegerField()

    def __str__(self):
        return self.username
