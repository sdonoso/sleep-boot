from django.views import View
from django.shortcuts import redirect, render
from rest_framework import viewsets
import datetime
from django.utils import timezone
from django.http import JsonResponse, HttpResponseNotFound

from .serializers import PersonSerializer, DataSerializer
from .models import Person, Data

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.offline import plot
import plotly as plotly_
plotly_.tools.set_credentials_file(username='jpintoriv', api_key='FEkr4GXDbnI1hhTmRDxg')


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
    def get(self, request, id_telegram, *args, **kwargs):
        
        today = timezone.now()

        person = Person.objects.get(id_telegram=id_telegram)
        data = Data.objects.filter(person=person, time_stamp__range=[today - datetime.timedelta(days = 7), today]).order_by('time_stamp')

        avg_mood = 0
        avg_sleep_hours = 0

        dates = []
        moods = []
        sleep_hours = []
        for value in data:
            avg_mood += value.mood
            avg_sleep_hours += value.sleep_hours

            dates.append(value.time_stamp)
            moods.append(value.mood)
            sleep_hours.append(value.sleep_hours)

        mood_graph = go.Scatter(
            x = dates,
            y = moods,
            mode = 'lines',
            name = 'Estado de ánimo'
        )

        sleep_hours_graph = go.Scatter(
            x = dates,
            y = sleep_hours,
            mode = 'lines',
            name = 'Horas dormidas'
        )
        data_graph = [mood_graph, sleep_hours_graph]

        graph = plot(data_graph, auto_open=False, output_type='div')
        self.context['graph'] = graph

        if(len(data)):
            avg_mood = avg_mood/len(data)
            avg_sleep_hours = avg_sleep_hours/len(data)

        self.context["avg_mood"] = round(avg_mood,1)
        self.context["avg_sleep_hours"] = round(avg_sleep_hours,1)
        self.context['cant_responses'] = len(data)

        return render(request, self.template, self.context)

class DateToday(View):
    def get(self, request, id_telegram, *args, **kwargs):
        try:
            person = Person.objects.get(id_telegram=id_telegram)
        except Person.DoesNotExist:
            return HttpResponseNotFound('Not Registered')
        today = timezone.now()
        data = Data.objects.filter(person=person, time_stamp__day=today.day, time_stamp__year=today.year, time_stamp__month=today.month)
        if len(data) == 0:
            return JsonResponse({'answered_today': False})
        return JsonResponse({'answered_today': True})
