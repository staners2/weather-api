from django.db import models

class Language(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(null=True)
    prefix = models.TextField(null=True)

class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL, db_constraint=False)
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class Cities(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField(null=True)
    country_code = models.TextField(null=True)

class Weather(models.Model):
    id = models.BigAutoField(primary_key=True)
    city = models.ForeignKey(Cities, null=True, on_delete=models.SET_NULL, db_constraint=False)
    temp = models.IntegerField(null=True)
    description = models.TextField(null=True)
    date = models.DateTimeField()

class Histories(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, db_constraint=False)
    weather = models.ForeignKey(Weather, null=True, on_delete=models.SET_NULL, db_constraint=False)

class Error():
    messages = None

    def __init__(self):
        self.messages = []

    def append(self, message):
        self.messages.append(message)