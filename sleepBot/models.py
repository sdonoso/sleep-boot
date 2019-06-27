from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Person(models.Model):
    name = models.CharField(max_length=150)
    id_telegram = models.CharField(max_length=150)
    creation_date = models.DateTimeField(default=timezone.now)


class Data(models.Model):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    sleep_hours = models.IntegerField()
    mood = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    time_stamp = models.DateTimeField(default=timezone.now)
