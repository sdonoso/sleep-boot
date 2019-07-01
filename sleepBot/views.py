from django.views import View
from django.shortcuts import redirect, render
from rest_framework import viewsets
import datetime
from django.utils import timezone

from .serializers import PersonSerializer, DataSerializer
from .models import Person, Data


class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class DataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class InfoDataPerson(View):
    template = "graph.html"
    context = {}
    def get(self, request, id_person, *args, **kwargs):
        
        today = timezone.now()

        person = Person.objects.get(pk=id_person)
        data = Data.objects.filter(person=person, time_stamp__range=(today, today - datetime.timedelta(days = 7)))

        return render(request, self.template)
