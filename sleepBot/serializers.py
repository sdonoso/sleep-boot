from rest_framework import serializers
from .models import Person, Data


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Person
        fields = ('name', 'id_telegram')

class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Data
        fields = ('person', 'sleep_hours', 'mood')