from django.test import TestCase
from datetime import datetime
from .models import Person, Data
from django.utils import timezone


# Create your tests here
class SleepModelTest(TestCase):

    def setUp(self):
        person = Person.objects.create(id_telegram="juanito", name="juan")
        Data.objects.create(person=person, sleep_hours=8, mood=4)
        Data.objects.create(person=person, sleep_hours=10, mood=11)

    def test_get_person(self):
        person = Person.objects.get(id_telegram="juanito")
        self.assertEquals(person.name, "juan")
        self.assertEquals(person.creation_date.day, 27)

    def test_data(self):
        person = Person.objects.get(id_telegram="juanito")
        data = Data.objects.filter(person=person)
        self.assertEquals(len(data),2)
        self.assertEquals(data[0].mood,4)
        self.assertEquals(data[1].mood,11)
