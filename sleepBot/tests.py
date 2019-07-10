import datetime

from django.test import Client, TestCase
from django.utils import timezone

from .models import Data, Person


# Create your tests here
class SleepModelTest(TestCase):

    def setUp(self):
        person = Person.objects.create(id_telegram=4, name="juan")
        Data.objects.create(person=person, sleep_hours=8, mood=4)
        Data.objects.create(person=person, sleep_hours=10, mood=11)

    def test_get_person(self):
        person = Person.objects.get(id_telegram=4)
        self.assertEquals(person.name, "juan")
        self.assertEquals(person.creation_date.day, timezone.now().day)  # Antes decia 27

    def test_data(self):
        person = Person.objects.get(id_telegram=4)
        data = Data.objects.filter(person=person)
        self.assertEquals(len(data), 2)
        self.assertEquals(data[0].mood, 4)
        self.assertEquals(data[1].mood, 11)


class CreatePersonTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_create_person(self):
        response = self.client.post("/persons/", {"name": "Jorge", "id_telegram": 101})
        self.assertEquals(response.status_code, 201)

        person = Person.objects.get(id_telegram=101)
        self.assertEquals(person.name, "Jorge")


class CreateDataTest(TestCase):

    def setUp(self):
        self.person = Person.objects.create(id_telegram=100, name="juan")
        self.client = Client()

    def test_create_data(self):
        id_person = self.person.pk
        response = self.client.post("/datas/",
                                    {"person": "/persons/" + str(id_person) + "/", "sleep_hours": 8, "mood": 4})
        self.assertEquals(response.status_code, 201)

        data = Data.objects.get(person=self.person)
        self.assertEquals(data.sleep_hours, 8)


class InfoDataWeek(TestCase):

    def setUp(self):
        self.client = Client()
        self.person = Person.objects.create(id_telegram=20, name="Jorge")
        today = timezone.now()
        data = [{"sleep_hours": 5, "mood": 6}, {"sleep_hours": 8, "mood": 10}, {"sleep_hours": 7, "mood": 9},
                {"sleep_hours": 3, "mood": 2}, {"sleep_hours": 7, "mood": 6}, {"sleep_hours": 10, "mood": 9},
                {"sleep_hours": 8, "mood": 10}, ]
        for i in range(7):
            Data.objects.create(person=self.person, sleep_hours=data[i]['sleep_hours'], mood=data[i]['mood'],
                                time_stamp=today - datetime.timedelta(days=i))

    def test_data_created(self):
        today = timezone.now()
        person = Person.objects.get(id_telegram=self.person.id_telegram)
        data = Data.objects.filter(person=person, time_stamp__range=[today - datetime.timedelta(days=7), today]).order_by('time_stamp')

        self.assertEquals(len(data), 7)

    def test_info_data(self):
        response = self.client.get("/graph/person/" + str(self.person.id_telegram))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'graph.html')
        self.assertContains(response, 'Días respondidos: 7 de 7')
        self.assertContains(response, 'Horas dormidas promedio: 6.9')
        self.assertContains(response, 'Estado de animo promedio: 7.4')
