__author__ = 'SKuptsov'

from admin.models import Spot
from rest_framework import serializers

class SpotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Spot